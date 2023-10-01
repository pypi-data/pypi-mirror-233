from pydantic import BaseModel, NonNegativeInt 
from typing import List, Optional

# -- Base Classes --

class Base(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class NameBase(Base):
    name: Optional[str] = None
    description: Optional[str] = ""


class Metric(NameBase):
    model_version_id: Optional[str] = None
    value: Optional[float] = 0.0

# -- Shares --

class Shareable(NameBase):
    user_id: Optional[str] = None
    notes: Optional[str] = None
    has_logo: Optional[bool] = False
    logo: Optional[str] = ""
    public: Optional[bool] = False
    shared_with_me: Optional[bool] = False

class Share(Base):
    email: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    without_invite: Optional[bool] = True

# -- Models --

class Model(Shareable):
    active_version_id: Optional[str] = ""
    can_inference: Optional[bool] = False
    kind: Optional[str] = ""
    config: Optional[str] = ""
    application_id: Optional[str] = ""
    has_ml_model: Optional[bool] = False
    has_onnx_model: Optional[bool] = False
    has_onnx_int8_model: Optional[bool] = False
    has_tflite_model: Optional[bool] = False
    has_labels_file: Optional[bool] = False
    auto_convert: Optional[bool] = True
    privacy_enabled: Optional[bool] = False


class ModelVersion(NameBase):
    model_id: Optional[str] = ""
    accuracy: Optional[float] = 0
    user_id: Optional[str] = ""
    can_inference: Optional[bool] = False
    has_logo: Optional[bool] = False
    config: Optional[str] = ""
    application_id: Optional[str] = None
    version: Optional[str] = ""
    version_number: Optional[int] = None
    has_ml_model: Optional[bool] = False
    has_onnx_model: Optional[bool] = False
    has_onnx_int8_model: Optional[bool] = False
    has_tflite_model: Optional[bool] = False
    has_labels_file: Optional[bool]= False
    dataset_id: Optional[str] = ""
    dataset_version_id: Optional[str] = ""
    job_id: Optional[str] = ""
    metrics: Optional[List[Metric]] = []

# -- Datasets --

class Label(NameBase):
    user_id: Optional[str] = ""
    version_id: Optional[str] = None
    color: Optional[str] = ""
    index: Optional[int] = 0
    shortcut: Optional[str] = ""


class LabelStat(Base):
    label_id: Optional[str] = ""
    split_id: Optional[str] = ""
    count: Optional[NonNegativeInt] = 0
    annotation_count: Optional[NonNegativeInt] = 0
    item_count: Optional[NonNegativeInt] = 0


class Annotation(Base):
    label_id: Optional[str] = ""
    item_id: Optional[str] = ""
    split_id: Optional[str] = ""
    coordinates: Optional[str] = ""
    user_id: Optional[str] = ""


class DatasetSplit(NameBase):
    user_id: Optional[str] = ""
    version_id: Optional[str] = ""


class DatasetItem(NameBase):
    user_id: Optional[str] = ""
    text: Optional[str] = ""
    splits: Optional[List[DatasetSplit]] = []
    annotations: Optional[List[Annotation]] = []
    extension: Optional[str] = ""


class DatasetVersion(NameBase):
    labels: Optional[List[Label]] = ""
    user_id: Optional[str] = ""
    dataset_id: Optional[str] = ""
    splits: Optional[List[DatasetSplit]] = []
    default_split: Optional[str] = ""
    config: Optional[str] = ""


class Dataset(Shareable):
    versions: Optional[List[DatasetVersion]] = []
    multi_label: Optional[bool] = False
    default_splits: Optional[bool] = False
    content_type: Optional[str] = ""


# -- Jobs --

class JobItem(NameBase):
    job_id: Optional[str] = None
    default_value: Optional[str] = ""
    value_type: Optional[str] = ""
    label: Optional[str] = ""
    value: Optional[str] = ""


class Job(NameBase):
    job_type: Optional[str] = "" #enum?
    application_id: Optional[str] = ""
    status: Optional[str] = "" # enum?
    status_message: Optional[str] = ""
    user_id: Optional[str] = ""
    cpu_start_time: Optional[str] = ""
    cpu_end_time: Optional[str] = ""
    gpu_start_time: Optional[str] = ""
    gpu_end_time: Optional[str] = ""
    agent_name: Optional[str] = ""
    dataset_id: Optional[str] = ""
    dataset_version_id: Optional[str] = ""
    model_id: Optional[str] = ""
    model_version_id: Optional[str] = ""
    start_model_id: Optional[str] = ""
    start_model_version_id: Optional[str] = ""
    items: Optional[List[JobItem]] = []


# -- Login --

class Registration(BaseModel):
    username: Optional[str]
    email: Optional[str]
    name: Optional[str]
    firstname: Optional[str]
    password: Optional[str]


class Credentials(BaseModel):
    username: Optional[str]
    password: Optional[str]


class LoginReply(BaseModel):
    id: Optional[str]
    username: Optional[str]
    name: Optional[str]
    email: Optional[str]
    firstname: Optional[str]
    apikey: Optional[str]


class RegistrationError(BaseModel):
    message: Optional[str]
    severity: Optional[str]
    registration: Optional[Registration]


class User(Base):
    username: Optional[str]
    email: Optional[str]
    name: Optional[str]
    firstname: Optional[str]
    apikey: Optional[str]

# -- Inferences --

class TextInput(BaseModel):
    input_text: Optional[str]

class InferenceItem(Base):
    prediction: Optional[str]  = ""
    confidence: Optional[float] = 0.0
    inference_id: Optional[str] = ""
    coordinates: Optional[str] = ""


class Inference(NameBase):
    prediction: Optional[str] = "" # deprecated
    confidence: Optional[float] = 0.0# deprecated
    model_id: Optional[str] = ""
    model_version_id: Optional[str] = ""
    extension: Optional[str] = ""
    user_id: Optional[str] = ""
    error_reported: Optional[bool] = False
    error: Optional[str] = ""
    application_id: Optional[str] = ""
    inference_host: Optional[str] = ""
    inference_time: Optional[str] = ""
    end_to_end_time: Optional[str] = ""
    dataset_item_id: Optional[str] = ""
    result: Optional[str] = ""
    inference_items: Optional[List[InferenceItem]] = []
    hidden: Optional[bool] = False
    privacy_enabled: Optional[bool] = False
    config: Optional[str] = ""


class AddInferences(BaseModel):
    keep_annotations: bool = True
    inferences: List[Inference] = []

# -- Applications --


class Application(NameBase):
    base_framework: Optional[str]
    base_framework_version: Optional[str]
    framework: Optional[str]
    framework_version: Optional[str]
    application: Optional[str]
    inference_host: Optional[str]
    can_convert_to_onnx: Optional[bool]
    can_convert_to_tensorflow: Optional[bool]
    can_convert_to_tflite: Optional[bool]
    continual_training: Optional[bool]
    has_embedding_support: Optional[bool]
    has_labels_file: Optional[bool]
    inference_extensions: Optional[str]