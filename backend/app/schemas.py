"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class FileTypeEnum(str, Enum):
    CSV = "CSV"
    JSON = "JSON"


class UploadMethodEnum(str, Enum):
    MANUAL = "MANUAL"
    API = "API"


class ProcessingStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class NotebookStatusEnum(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"


# Device Schemas
class DeviceBase(BaseModel):
    name: str
    device_type: str
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: str
    is_active: bool
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# DataFile Schemas
class DataFileBase(BaseModel):
    original_filename: str
    file_type: FileTypeEnum
    device_id: Optional[str] = None


class DataFileResponse(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_path: str
    file_type: FileTypeEnum
    file_size: int
    device_id: Optional[str] = None
    upload_method: UploadMethodEnum
    upload_timestamp: datetime
    processing_status: ProcessingStatusEnum
    file_metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DataFileListResponse(BaseModel):
    files: List[DataFileResponse]
    total: int
    page: int
    page_size: int


# Clustering Schemas
class ClusteringResultResponse(BaseModel):
    id: str
    data_file_id: str
    algorithm: str
    parameters: Optional[Dict[str, Any]] = None
    cluster_labels: List[int]
    metrics: Optional[Dict[str, Any]] = None
    visualization_path: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ClusteringRequest(BaseModel):
    data_file_id: str
    algorithm: Optional[str] = None  # If None, auto-select
    parameters: Optional[Dict[str, Any]] = None


# Notebook Schemas
class NotebookSessionResponse(BaseModel):
    id: str
    data_file_id: str
    notebook_path: str
    kernel_id: Optional[str] = None
    status: NotebookStatusEnum
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class NotebookCreateRequest(BaseModel):
    data_file_id: str


class NotebookCreateResponse(BaseModel):
    session_id: str
    notebook_url: str


# Device Deletion Schemas
class DeviceDeleteRequest(BaseModel):
    save_data_files: bool = Field(
        default=True,
        description="If True, keep data files but remove device association. If False, delete all data files."
    )


# File Upload Response
class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    status: str
    message: str

