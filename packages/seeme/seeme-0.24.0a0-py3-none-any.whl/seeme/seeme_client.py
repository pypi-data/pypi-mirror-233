import os
import json
import requests
import zipfile
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
from dotenv import dotenv_values
from .types import *
from typing import List
from pydantic import TypeAdapter

REGISTER_ENDPOINT = 'register'
USERS_ENDPOINT = 'users'
LOGIN_ENDPOINT = 'login'
MODELS_ENDPOINT = 'models'
TRAINING_REQUESTS_ENDPOINT = 'trainingrequests'
JOBS_ENDPOINT = 'jobs'
INFERENCE_ENDPOINT = 'inferences'
DATASETS_ENDPOINT = 'datasets'
VERSIONS_ENDPOINT = 'versions'
LABELS_ENDPOINT = 'labels'
SPLITS_ENDPOINT = 'splits'
ITEMS_ENDPOINT = 'items'
ANNOTATIONS_ENDPOINT = 'annotations'
SHARES_ENDPOINT = 'share'
APPLICATIONS_ENDPOINT = 'applications'
ADD_INFERENCES_ENDPOINT = 'add_inferences'

SUPPORTED_DOWNLOAD_EXTENSIONS = [ "pkl", "mlmodel", "tflite", "onnx", "onnx_int8", "names", "labels", "weights", "cfg", "conversion_cfg" ]



# --- DATASET CONSTANTS ---

DATASET_CONTENT_TYPE_IMAGES = "images"
DATASET_CONTENT_TYPE_TEXT = "text"
DATASET_CONTENT_TYPE_TABULAR = "tabular"
DATASET_CONTENT_TYPE_NER = "ner"

DATASET_FORMAT_FOLDERS = "folders"
DATASET_FORMAT_YOLO = "yolo"
DATASET_FORMAT_CSV = "csv"

DATASET_FORMAT_SPACY_NER = "spacy-ner"

# --- JOB CONSTANTS ---

JOB_TYPE_TRAINING = "training"
JOB_TYPE_VALIDATION = "validation"
JOB_TYPE_CONVERSION = "conversion"

JOB_STATUS_WAITING = "waiting"
JOB_STATUS_STARTED = "started"
JOB_STATUS_FINISHED = "finished"
JOB_STATUS_ERROR = "error"

SEEME_APIKEY = "SEEME_API_KEY"
SEEME_USERNAME = "SEEME_USERNAME"
SEEME_BACKEND = "SEEME_BACKEND"

class Client():
  """ 
  Client class to interact with the SeeMe.ai backend, allowing you to manage models, datasets, predictions and training requests.
  
  Parameters:
  ---
  
  username (optional) : the username for the account you want to use;
  apikey (optional) : the API key for the username you want user;
  backend (prefilled): the backend the client communicates with.

  Note: 
  username and apikey are optional but they need to used together in order to be authenticated. Authentication will be used on subsequent requests.
  Alternatively, you can use the login method (see below)
  """
  def __init__(self, username:str=None, apikey:str=None, backend:str=None, env_file:str=".env"):
    self.headers = {}
    self.username = None
    self.apikey = None
    self.backend = None

    config = dotenv_values(env_file)
 
    env_apikey = config[SEEME_APIKEY] if SEEME_APIKEY in config else None
    env_username = config[SEEME_USERNAME] if SEEME_USERNAME in config else None
    env_backend = config[SEEME_BACKEND] if SEEME_BACKEND in config else None

    if env_username is not None and env_apikey is not None:
      self.username = env_username
      self.update_auth_header(env_username, env_apikey)
      self.backend = env_backend

    if username is not None and apikey is not None:
      self.username = username
      self.update_auth_header(username, apikey)

    if env_backend is None:
      self.backend = "https://api.seeme.ai/api/v1/"

    if backend is not None:
      if not backend.endswith("/"):
        backend = backend + "/"
      self.backend = backend
      
    self.endpoints = {
      REGISTER_ENDPOINT: self.crud_endpoint(REGISTER_ENDPOINT),
      LOGIN_ENDPOINT: self.crud_endpoint(LOGIN_ENDPOINT),
      MODELS_ENDPOINT: self.crud_endpoint(MODELS_ENDPOINT),
      TRAINING_REQUESTS_ENDPOINT: self.crud_endpoint(TRAINING_REQUESTS_ENDPOINT),
      JOBS_ENDPOINT: self.crud_endpoint(JOBS_ENDPOINT),
      INFERENCE_ENDPOINT: self.crud_endpoint(INFERENCE_ENDPOINT),
      DATASETS_ENDPOINT: self.crud_endpoint(DATASETS_ENDPOINT),
      APPLICATIONS_ENDPOINT: self.crud_endpoint(APPLICATIONS_ENDPOINT),
      USERS_ENDPOINT: self.crud_endpoint(USERS_ENDPOINT)
    }
    self.applications = list[Application]()
    self.supported_dataset_export_formats = [ DATASET_FORMAT_FOLDERS, DATASET_FORMAT_YOLO, DATASET_FORMAT_CSV, DATASET_FORMAT_SPACY_NER ]
    self.supported_dataset_import_formats = [ DATASET_FORMAT_FOLDERS, DATASET_FORMAT_YOLO, DATASET_FORMAT_CSV, DATASET_FORMAT_SPACY_NER ]

    if self.is_logged_in():
      self.applications = self.get_applications()

  # -- Login / Registration --

  def register(self, username:str, email:str, password:str, firstname:str, name:str):
    """  
    Register a new user with a username, email and password. 
    
    Optionally, you can add a first and last name.
    """
    register_api = self.endpoints[REGISTER_ENDPOINT]

    register_data = Registration(
      username=username, 
      email=email, 
      name=name, 
      firstname=firstname, 
      password=password
    )

    r = requests.post(register_api, data=json.dumps(register_data.model_dump()), headers=self.headers)
 
    registered_user = r.json()

    if "message" in registered_user:
      raise ValueError(registered_user["message"])
    
    return User(**registered_user)

  def login(self, username:str, password:str):
    """ 
    Log in with a username and password.
    
    The username and password will be used to get the API key from the backend. 
    The method will fail if the user is not known, the password is incorrect, or the service cannot be reached.
    """
    login_api = self.endpoints[LOGIN_ENDPOINT]

    login_data = Credentials(username=username, password=password)
    
    logged_in = self.api_post(login_api, login_data)

    logged_in = LoginReply(**logged_in)

    username = logged_in.username
    apikey = logged_in.apikey

    user_id = logged_in.id

    self.update_auth_header(username, apikey)
    self.username = username
    self.user_id = user_id

    self.applications =  self.get_applications()

    return logged_in
      
  def logout(self):
    """ Log out the current user."""
    self.update_auth_header(None, None)

  def get_application_id(self, base_framework="pytorch", framework="", base_framework_version="1.10.0", framework_version="", application="image_classification"):
    """ Returns the application_id for the application you want to deploy:
    
    Parameters
    ---

    base_framework: the base_framework for the application (e.g. "pytorch", ...)
    base_framework_version: the version of the base_framework (e.g. "1.9.0", ...)
    framework: the framework for the application (e.g. "fastai", ...)
    framework_version: the version of the framework (e.g. "2.5.2", ...)
    application: the type of application you want to deply (e.g. "image_classification", "object_detection", "text_classification", "structured")

    Note
    ---

    To get a list of all the supported applications, see the "get_applications" method.
    """
    if len(self.applications) == 0:
      self.applications = self.get_applications()

    for f in self.applications:
      if f.base_framework == base_framework \
        and f.framework == framework \
        and f.base_framework_version == base_framework_version \
        and f.framework_version == framework_version \
        and f.application == application:
          return f.id
    
    for f in self.applications:
      if f.base_framework == base_framework \
        and f.framework == framework \
        and f.base_framework_version in base_framework_version \
        and f.framework_version == framework_version \
        and f.application == application:
          return f.id
    
    err_msg = f"\n\nYour config is not supported:\n\n--- \n\nBase framework: {base_framework} (v{base_framework_version})\nFramework:      {framework} (v{framework_version}) \nApplication:    {application} \n\n---\n\n is not supported.\n\nPlease contact: support@seeme.ai."
      
    raise NotImplementedError(err_msg)
    
  # -- CRUD models --

  def get_models(self):
    self.requires_login()

    models_api = self.endpoints[MODELS_ENDPOINT]

    ta = TypeAdapter(List[Model])
    return ta.validate_python(self.api_get(models_api))

  def create_model(self, model):
    self.requires_login()

    models_api = self.endpoints[MODELS_ENDPOINT]

    return Model(**self.api_post(models_api, model))

  def get_model(self, model_id:str):
    self.requires_login()

    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id

    return  Model(**self.api_get(model_api))

  def update_model(self, model):
    self.requires_login()

    assert model
    assert model.id
    model_api = self.endpoints[MODELS_ENDPOINT] + "/" + model.id
    return Model(**self.api_put(model_api, model))

  def delete_model(self, model_id:str):
    self.requires_login()

    delete_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id

    return self.api_delete(delete_api)

  def upload_model(self, model_id:str, folder:str="data", filename:str="export.pkl"):
    self.requires_login()

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    return ModelVersion(**self.upload(model_upload_api, folder, filename, 'application/octet-stream'))
  
  def upload_logo(self, model_id:str, folder:str="data", filename:str="logo.jpg"):
    self.requires_login()

    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"

    model_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/upload"

    return Model(**self.upload(model_upload_api, folder, filename,  content_type))
  
  def get_logo(self, model):
    self.requires_login()

    logo_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model.id + "/download/logo"
    return self.api_download(logo_endpoint, model.logo)
  
  def download_active_model(self, model, asset_type="pkl", download_folder="."):
    """
      asset_type: mlmodel, tflite, onnx, onnx_int8, pkl, labels, names
    """

    if asset_type not in SUPPORTED_DOWNLOAD_EXTENSIONS:
      raise NotImplementedError

    model_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model.id + "/download/" + asset_type

    extension = asset_type

    if asset_type == "labels":
      extension = "txt"

    name = model.active_version_id +"." + extension

    if asset_type == "conversion_cfg":
      name = model.active_version_id +"_conversion.cfg"
    
    if asset_type == "onnx_int8":
      name = model.active_version_id + "_int8.onnx"

    download_folder = download_folder.rstrip("/")

    os.makedirs(download_folder, exist_ok=True)

    return self.api_download(model_endpoint, f"{download_folder}/{name}")

  def upload(self, url:str, folder:str, filename:str, content_type:str):
    self.requires_login()

    data = MultipartEncoder(
                fields={
                    'file': (filename, open(folder + "/" + filename, 'rb'), content_type)}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return self.api_upload(url, data=data, headers=content_headers)

  # -- CRUD Model Versions

  def get_model_versions(self, model_id):
    self.requires_login()

    model_versions_api = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{VERSIONS_ENDPOINT}"

    ta = TypeAdapter(List[ModelVersion])
    return ta.validate_python(self.api_get(model_versions_api))

  def get_model_version(self, model_id, version_id):
    self.requires_login()

    model_version_api = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{VERSIONS_ENDPOINT}/{version_id}"

    return ModelVersion(**self.api_get(model_version_api))

  def create_model_version(self, model_id, version):
    self.requires_login()

    model_version_api = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{VERSIONS_ENDPOINT}"

    return ModelVersion(**self.api_post(model_version_api, version))
  
  def update_model_version(self, version):
    self.requires_login()

    model_version_api = f"{self.endpoints[MODELS_ENDPOINT]}/{version.model_id}/{VERSIONS_ENDPOINT}/{version.id}"

    return ModelVersion(**self.api_put(model_version_api, version))

  def delete_model_version(self, model_id, version_id):
    self.requires_login()

    model_version_api = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{VERSIONS_ENDPOINT}/{version_id}"

    return ModelVersion(**self.api_delete(model_version_api))

  def upload_model_version(self, version, folder:str="data", filename:str="export.pkl"):

    model_version_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + version.model_id  + "/"+ VERSIONS_ENDPOINT + "/" + version.id + "/upload"

    return ModelVersion(**self.upload(model_version_upload_api, folder, filename, 'application/octet-stream'))

  def upload_model_version_logo(self, model_id, version_id, folder:str="data", filename:str="logo.jpg"):
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"

    model_version_upload_api = self.endpoints[MODELS_ENDPOINT] + "/" + model_id  + "/"+ VERSIONS_ENDPOINT + version_id + "/upload"

    return ModelVersion(**self.upload(model_version_upload_api, folder, filename, content_type))
  
  # Deprecated 
  def download_version(self, version, asset_type):
    print("DEPRECATED: Please use download_model()")
    return self.download_model(version, asset_type)

  def download_model_version(self, model_version, asset_type, download_folder="."):
    """
      asset_type: "pkl", "mlmodel", "tflite", "onnx", "onnx_int8", "names", "labels", "weights", "cfg", "conversion_cfg" 
    """
    return self.download_model(model_version, asset_type, download_folder)
  
  def download_model(self, model_version, asset_type, download_folder="."):
    """
      asset_type: "pkl", "mlmodel", "tflite", "onnx", "onnx_int8", "names", "labels", "weights", "cfg", "conversion_cfg" 
    """

    self.requires_login()

    extension = asset_type

    if asset_type == "labels":
      extension = "txt"

    name = model_version.id +"." + extension

    if asset_type == "conversion_cfg":
      name = model_version.id +"_conversion.cfg"
    
    if asset_type == "onnx_int8":
      name = model_version.id + "_int8.onnx"

    version_endpoint = self.endpoints[MODELS_ENDPOINT] + "/" + model_version.model_id + "/" + VERSIONS_ENDPOINT + "/" + model_version.id + "/download/" + asset_type
    
    download_folder = download_folder.rstrip("/")

    os.makedirs(download_folder, exist_ok=True)
    
    return self.api_download(version_endpoint, f"{download_folder}/{name}")
  
  # -- Share model --
  def share_model(self, model_id, email, send_invite=False):
    self.requires_login()

    share = Share(
      email=email,
      entity_type=MODELS_ENDPOINT,
      entity_id=model_id,
      without_invite= not send_invite
    )

    share_url = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{SHARES_ENDPOINT}"

    return Share(**self.api_post(share_url, share))

  def get_model_shares(self, model_id) -> List[Share]:
    self.requires_login()

    share_url = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{SHARES_ENDPOINT}"

    ta = TypeAdapter(List[Share])
    return ta.validate_python(self.api_get(share_url))

  def delete_model_share(self, model_id, share_id):
    self.requires_login()

    share_url = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{SHARES_ENDPOINT}/{share_id}"

    return self.api_delete(share_url)

  # -- CRUD JOBS --
  def get_jobs(self, application_id="", states=[JOB_STATUS_WAITING, JOB_STATUS_STARTED, JOB_STATUS_FINISHED, JOB_STATUS_ERROR], job_types=[JOB_TYPE_TRAINING]):
    self.requires_login()

    jobs_api = self.endpoints[JOBS_ENDPOINT]


    states_param = ",".join(states)
    jobs_param = ",".join(job_types)

    jobs_api += f"?applicationId={application_id}&status={states_param}&jobType={jobs_param}"

    ta = TypeAdapter(List[Job])

    return ta.validate_python(self.api_get(jobs_api))
  
  def get_job(self, job_id:str) -> Job:
    self.requires_login()

    job_api = self.endpoints[JOBS_ENDPOINT] + "/" + job_id

    return Job(**self.api_get(job_api))
  
  def create_job(self, job) -> Job:
    self.requires_login()

    jobs_api = self.endpoints[JOBS_ENDPOINT]

    return Job(**self.api_post(jobs_api, job))
  
  def update_job(self, job) -> Job:
    self.requires_login()

    jobs_api = self.endpoints[JOBS_ENDPOINT]  + "/" + job.id

    return Job(**self.api_put(jobs_api, job))
  
  def delete_job(self, job_id:str):
    self.requires_login()

    jobs_api = self.endpoints[JOBS_ENDPOINT] + "/" + job_id

    return self.api_delete(jobs_api)

  # -- CRUD Inference --

  def predict(self, model_id:str, item, input_type="image_classification"):
      return self.inference(model_id, item, input_type)

  def inference(self, model_id:str, item, input_type="image_classification"):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + model_id

    if input_type=="image_classification" or input_type=="object_detection" or input_type=="ocr":

      item_name = os.path.basename(item)
      data = MultipartEncoder(
                  fields={
                      'file': (item_name, open(item, 'rb'), 'application/octet-stream')}
                        )

      content_headers = self.headers

      content_headers['Content-Type'] = data.content_type

      return Inference(**self.api_upload(inference_api, data=data, headers=content_headers))
    elif input_type=="text_classification" or input_type=="language_model" or input_type=="ner":
      data = TextInput(input_text=item)

      return Inference(**self.api_post(inference_api, data))
    elif input_type=="structured":
      data = TextInput(input_text=item)

      return Inference(**self.api_post(inference_api, data))
    else:
      raise NotImplementedError

  def version_predict(self, version, item, input_type="image_classification"):
    return self.version_inference(version, item, input_type)

  # Obsolete, will be replaced by version_predict
  def version_inference(self, version, item, input_type="image_classification"):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + version.model_id + "/" + VERSIONS_ENDPOINT + "/" + version.id

    if input_type=="image_classification":

      item_name = os.path.basename(item)
      data = MultipartEncoder(
                  fields={
                      'file': (item_name, open(item, 'rb'), 'application/octet-stream')}
                        )

      content_headers = self.headers

      content_headers['Content-Type'] = data.content_type

      return Inference(**self.api_upload(inference_api, data=data, headers=content_headers))
    elif input_type=="text_classification":
        data = {
          'input_text': item
        }

        return Inference(**self.api_post(inference_api, data))
    elif input_type=="structured":
      data = {
              'input_text': item
      }

      return Inference(**self.api_post(inference_api, data))
    else:
      raise NotImplementedError

  def add_inference(self, model_id:str, inference:Inference):
     self.requires_login()

     add_inference_endpoint = self.endpoints[INFERENCE_ENDPOINT] + "/" + model_id + "/add"

     return Inference(**self.api_post(add_inference_endpoint, inference))

  def add_inference_file(self, inference_id:str, folder:str, filename:str, content_type:str ):
    self.requires_login()

    add_inference_file_endpoint = self.endpoints[INFERENCE_ENDPOINT] + "/" + inference_id + "/upload"

    return Inference(**self.upload(add_inference_file_endpoint, folder, filename, content_type))

  def download_inference_file(self, inference_id:str, filename:str):

    self.requires_login()
    download_inference_endpoint = self.endpoints[INFERENCE_ENDPOINT] + "/" + inference_id + "/download"

    self.api_download(download_inference_endpoint, filename)


  def update_inference(self, inference):
    self.requires_login()

    inference_api = self.endpoints[INFERENCE_ENDPOINT] + "/" + inference.id

    return Inference(**self.api_put(inference_api, inference))

  def get_inferences(self, model_id:str, model_version_ids=[], page_count=0, page_size=25, include_already_added=False, show_hidden=False):
    self.requires_login()

    model_inferences_api = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/{INFERENCE_ENDPOINT}"

    params = {
      "pageCount": page_count, 
      "pageSize": page_size,
      "modelVersionIds": ",".join(model_version_ids),
      "includeAlreadyAdded": include_already_added,
      "showHidden": show_hidden
    }

    ta = TypeAdapter(List[Inference])

    return ta.validate_python(self.api_get(model_inferences_api,  params=params))
  
  def add_inferences(self, dataset_id, dataset_version_id, dataset_split_id, add_inferences):
    self.requires_login()

    add_inferences_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}/{dataset_split_id}/{ADD_INFERENCES_ENDPOINT}"

    return AddInferences(** self.api_post(add_inferences_api, add_inferences))

  def get_inference_stats(self, model_id ):
    self.requires_login()
    inference_stats_endpoint = f"{self.endpoints[MODELS_ENDPOINT]}/{model_id}/stats"

    return self.api_get(inference_stats_endpoint)

  # -- CRUD applicationS --
  def get_applications(self):
    self.requires_login()

    application_api = self.endpoints[APPLICATIONS_ENDPOINT]
    
    ta = TypeAdapter(List[Application])

    return ta.validate_python(self.api_get(application_api))

  # -- CRUD DATASETS --

  def get_datasets(self) -> List[Dataset]:
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]

    ta = TypeAdapter(List[Dataset])

    return ta.validate_python(self.api_get(dataset_api))

  def create_dataset(self, dataset) -> Dataset:
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT]

    ds = self.api_post(dataset_api, dataset)

    return Dataset(**ds)

  def get_dataset(self, dataset_id:str) -> Dataset:
    self.requires_login()

    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset_id

    return Dataset(**self.api_get(dataset_api))

  def update_dataset(self, dataset) -> Dataset:
    self.requires_login()

    assert dataset
    assert dataset.id
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset.id
    return Dataset(**self.api_put(dataset_api, dataset))

  def upload_dataset_logo(self, dataset_id:str, folder:str="data", filename:str="logo.jpg") -> Dataset:
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"

    datasets_upload_api = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset_id  + "/upload"

    return Dataset(**self.upload(datasets_upload_api, folder, filename,  content_type))

  def get_dataset_logo(self, dataset):
    logo_endpoint = self.endpoints[DATASETS_ENDPOINT] + "/" + dataset.id + "/logo"
    return self.api_download(logo_endpoint, dataset.logo)

  def delete_dataset(self, id:str):
    self.requires_login()
    dataset_api = self.endpoints[DATASETS_ENDPOINT] + "/" + id

    return self.api_delete(dataset_api)
  
  # -- Share Dataset --
  def share_dataset(self, dataset_id, email, send_invite=False) -> Share:
    self.requires_login()

    share = Share(
      email=email,
      entity_type= DATASETS_ENDPOINT,
      entity_id= dataset_id,
      without_invite= not send_invite
    )

    share_url = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{SHARES_ENDPOINT}"

    return Share(**self.api_post(share_url, share))

  def create_dataset_version(self, dataset_id, dataset_version):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}"

    return DatasetVersion(**self.api_post(dataset_version_api, dataset_version))

  def get_dataset_versions(self, dataset_id)-> List[DatasetVersion]:
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}"

    ta = TypeAdapter(List[DatasetVersion])
    return ta.validate_python(self.api_get(dataset_version_api))
  
  def get_dataset_version(self, dataset_id, dataset_version_id) -> DatasetVersion:
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}"

    return DatasetVersion(**self.api_get(dataset_version_api))

  def update_dataset_version(self, dataset_id, dataset_version) -> DatasetVersion:
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version.id}"

    return DatasetVersion(**self.api_put(dataset_version_api, dataset_version))

  def duplicate_dataset_version(self, dataset_id, dataset_version_id) -> DatasetVersion:
    duplicate_dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/new"

    return DatasetVersion(**self.api_post(duplicate_dataset_version_api, DatasetVersion()))

  def delete_dataset_version(self, dataset_id, dataset_version):
    self.requires_login()

    dataset_version_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version.id}"

    return self.api_delete(dataset_version_api)
  
  def create_dataset_label(self, dataset_id, dataset_version_id, label) -> Label:
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}"

    return Label(**self.api_post(labels_api, label))

  def get_dataset_labels(self, dataset_id, dataset_version_id) -> List[Label]:
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}"

    ta = TypeAdapter(List[Label])
    return ta.validate_python(self.api_get(labels_api))
  
  def get_dataset_label(self, dataset_id, dataset_version_id, label_id) -> Label:
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}/{label_id}"

    return Label(**self.api_get(labels_api))

  def update_dataset_label(self, dataset_id, dataset_version_id, label) -> Label:
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}/{label.id}"

    return Label(**self.api_put(labels_api, label))

  def delete_dataset_label(self, dataset_id, dataset_version_id, label):
    self.requires_login()

    labels_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}/{label.id}"

    return self.api_delete(labels_api)
  
  def get_label_stats(self, dataset_id, dataset_version_id, split_id) -> List[LabelStat]:
    self.requires_login()

    label_stats_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{LABELS_ENDPOINT}/{SPLITS_ENDPOINT}/{split_id}"
    
    ta = TypeAdapter(List[LabelStat])

    return ta.validate_python( self.api_get(label_stats_api))
  
  def get_stats_for_unlabelled(self, label_stats:List[LabelStat]):
    return self.get_stats_for_label(label_stats, "")

  def get_stats_for_label(self, label_stats:List[LabelStat], label_id:str):
    found_label_stat =  [ l for l in label_stats if l.label_id == label_id]
    return found_label_stat[0]

    #return self.find_item_in_array(label_stats, "label_id", label_id, True)
  
  def create_dataset_split(self, dataset_id, dataset_version_id, split) -> DatasetSplit:
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}"

    return DatasetSplit(**self.api_post(splits_api, split))

  def get_dataset_splits(self, dataset_id, dataset_version_id) -> List[DatasetSplit]:
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}"

    ta = TypeAdapter(List[DatasetSplit])
    return ta.validate_python(self.api_get(splits_api))
  
  def get_dataset_split(self, dataset_id, dataset_version_id, split_id) -> DatasetSplit:
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}/{split_id}"

    return DatasetSplit(**self.api_get(splits_api))

  def update_dataset_split(self, dataset_id, dataset_version_id, split) -> DatasetSplit:
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}/{split.id}"

    return DatasetSplit(**self.api_put(splits_api, split))

  def delete_dataset_split(self, dataset_id, dataset_version_id, split):
    self.requires_login()

    splits_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}/{split.id}"

    return self.api_delete(splits_api)
  
  def get_dataset_items(self, dataset_id, dataset_version_id, params=None) -> List[DatasetItem]:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}"

    ta = TypeAdapter(List[DatasetItem])
    return ta.validate_python(self.api_get(items_api, params=params))

  def create_dataset_item(self, dataset_id, dataset_version_id, item) -> DatasetItem:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}"

    return DatasetItem(**self.api_post(items_api, item))

  def get_dataset_item(self, dataset_id, dataset_version_id, item_id) -> DatasetItem:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}/{item_id}"

    return DatasetItem(**self.api_get(items_api))

  def update_dataset_item(self,  dataset_id, dataset_version_id, item) -> DatasetItem:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}/{item.id}"

    return DatasetItem(**self.api_put(items_api, item))

  def delete_dataset_item(self, dataset_id, dataset_version_id, split_id, item) -> DatasetItem:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{SPLITS_ENDPOINT}/{split_id}/{ITEMS_ENDPOINT}/{item.id}"

    return DatasetItem(**self.api_delete(items_api))

  def upload_dataset_item_image(self, dataset_id, dataset_version_id, item_id, folder, filename) -> DatasetItem:
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}/{item_id}/upload"
    
    if filename.endswith("jpg"):
      content_type="image/jpg"
    elif filename.endswith("jpeg"):
      content_type="image/jpeg"
    elif filename.endswith("png"):
      content_type="image/png"
    else:
      print("Image type not supported")
      return

    data = MultipartEncoder(
                fields={
                    'file': (filename, open(folder + "/" + filename, 'rb'), content_type)}
                       )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return DatasetItem(**self.api_upload(items_api, data=data, headers=content_headers))

  def download_dataset_item_image(self, dataset_id, dataset_version_id, item_id, download_location, thumbnail=False):
    self.requires_login()

    items_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ITEMS_ENDPOINT}/{item_id}/download"
  
    if thumbnail:
      items_api += "?thumbnail=true"

    return self.api_download(items_api, download_location)
  
  def annotate(self, dataset_id, dataset_version_id, annotation) -> Annotation:
    self.requires_login()

    annotation_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ANNOTATIONS_ENDPOINT}"

    return Annotation(**self.api_post(annotation_api, annotation))

  def update_annotation(self, dataset_id, dataset_version_id, annotation) -> Annotation:
    self.requires_login()

    annotation_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ANNOTATIONS_ENDPOINT}/{annotation.id}"

    return Annotation(**self.api_put(annotation_api, annotation))

  def delete_annotation(self, dataset_id, dataset_version_id, annotation_id) -> Annotation:
    self.requires_login()

    annotation_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/{ANNOTATIONS_ENDPOINT}/{annotation_id}"

    return Annotation(**self.api_delete(annotation_api))

  def download_dataset(self, dataset_id, dataset_version_id, split_id="", extract_to_folder="data", download_file="dataset.zip", remove_download_file=True, export_format=""):
    self.requires_login()

    dataset_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/download"

    if split_id != "":
      dataset_api = f"{dataset_api}/{split_id}"

    params = None

    if len(export_format) > 0:
      if export_format not in self.supported_dataset_export_formats:
        print(f"WARNING: Requested export format: '{export_format}' not supported. Returning the default export format.")

    params = {
      "format": export_format
    }

    self.api_download(dataset_api, download_file, params=params)

    with zipfile.ZipFile(download_file, 'r') as zip_ref:
      zip_ref.extractall(extract_to_folder)

    if remove_download_file:
      os.remove(download_file)
    
  def upload_dataset_version(self, dataset_id, dataset_version_id, folder="data", filename="dataset.zip", format="") -> DatasetVersion:
    self.requires_login()

    dataset_api = f"{self.endpoints[DATASETS_ENDPOINT]}/{dataset_id}/{VERSIONS_ENDPOINT}/{dataset_version_id}/upload"

    if len(format) > 0:
      if format in self.supported_dataset_import_formats:
        dataset_api = f"{dataset_api}/{format}"
      else:
        print("Supported import formats")
        print(self.supported_dataset_import_formats)
        raise NotImplementedError()

    content_type="application/x-zip-compressed"

    data = MultipartEncoder(
            fields={
                'file': (filename, open(folder + "/" + filename, 'rb'), content_type)
            }
          )

    content_headers = self.headers

    content_headers['Content-Type'] = data.content_type

    return DatasetVersion(**self.api_upload(dataset_api, data=data, headers=content_headers))

  # Convenience methods

  def get_apikey(self) -> str:
    return self.apikey
  
  def random_color(self):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    rgb = (r,g,b)

    return '#%02x%02x%02x' % rgb

  # Helpers

  def requires_login(self):
    if not self.is_logged_in():
      raise Exception("You need to be logged in for this.")

  def update_applications(self):
    self.applications = self.get_applications()

  def update_auth_header(self, username:str=None, apikey:str=None):
    if username == None or apikey == None:
      del self.headers["Authorization"]
      self.apikey = apikey
      self.user_id = None
      self.username = username
      self.backend = None
      self.applications = List[Application]

      return

    self.apikey = apikey
    
    self.headers = {
      "Authorization": f"{username}:{apikey}"
    }
  
  def is_logged_in(self):
    return "Authorization" in self.headers
  
  def delete_user(self):
    self.requires_login()

    users_api = self.endpoints[USERS_ENDPOINT] + "/" + self.user_id

    self.api_delete(users_api)

    self.logout()

  def crud_endpoint(self, endpoint:str):
    return f"{self.backend}{endpoint}"
  
  def find_value_for_item_name(self, job, item_name, failover=None):
    item = self.find_job_item(job, "name", item_name)

    if item:
      return self.find_value_for_item_key(item)

    return failover
  
  def find_job_item(self, job, item_key, item_value):
    for item in job.items:
      item = item.model_dump()
      if item_key in item:
        if item[item_key] == item_value:
          return item
    
    return None
  
  def find_value_for_item_key(self, item):
      try:
        value = item["value"]
      except:
        item = item.model_dump()
        value = item["value"]

      if item["value_type"] == "number":
        try:
          return int(value)
        except:
          return float(value)
      
      if item["value_type"] == "boolean":
        return True if value == 'true' or value == True else False
      
      return value
  
  def find_item_in_array(self, ar, prop, value, first_item=False, t:BaseModel=None):
    try:
      results = [i for i in ar if i[prop] == value]
    except:
      #ar = ar.model_dump()
      results = [i.model_dump() for i in ar if i.model_dump()[prop] == value]

    if first_item:
      if t:
        return t(**first_item)
      else:
        return results[0]
    
    if t:
      ta = TypeAdapter(t)
      return ta.validate_python(results)
    else:
      return results

  ## CRUD API methods

  def api_get(self, api:str, params=None):
      r = requests.get(api, headers=self.headers, params=params)
      r.raise_for_status()
      return r.json()

  def api_post(self, api:str, data, params=None):
    data = json.dumps(data.model_dump())
    r = requests.post(api, data=data, headers=self.headers)
    r.raise_for_status()
    return r.json()

  def api_upload(self, api:str, data, headers):
    r = requests.post(api, data=data, headers=headers)
    r.raise_for_status()
    return r.json()
  
  def api_put(self, api:str, data):
    data = json.dumps(data.model_dump(), default=str)
    r = requests.put(api, data=data, headers=self.headers)
    r.raise_for_status()
    return r.json()
  
  def api_delete(self, api:str):
    r = requests.delete(api, headers=self.headers)
    r.raise_for_status()
    return r.json()

  def api_download(self, api:str, filename:str, params=None):
    r = requests.get(api, allow_redirects=True, headers=self.headers, params=params)
    r.raise_for_status()
    open(filename, "wb").write(r.content)
