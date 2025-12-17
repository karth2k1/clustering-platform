"""Database models"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum as PyEnum
from app.database import Base


def generate_uuid():
    """Generate UUID string"""
    return str(uuid.uuid4())


class FileType(PyEnum):
    """File type enumeration"""
    CSV = "CSV"
    JSON = "JSON"


class UploadMethod(PyEnum):
    """Upload method enumeration"""
    MANUAL = "MANUAL"
    API = "API"


class ProcessingStatus(PyEnum):
    """Processing status enumeration"""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class NotebookStatus(PyEnum):
    """Notebook session status"""
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"


class Device(Base):
    """Device model for managing data sources"""
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    device_type = Column(String, nullable=False)  # e.g., "Intersight", "Custom"
    api_endpoint = Column(String, nullable=True)
    api_key_encrypted = Column(BLOB, nullable=True)  # Encrypted API key
    configuration = Column(JSON, nullable=True)  # Additional configuration
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    data_files = relationship("DataFile", back_populates="device", cascade="all, delete-orphan")


class DataFile(Base):
    """Data file model"""
    __tablename__ = "data_files"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String, nullable=False)  # Stored filename
    original_filename = Column(String, nullable=False)  # Original upload filename
    file_path = Column(String, nullable=False)  # Path relative to upload directory
    file_type = Column(SQLEnum(FileType), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    device_id = Column(String, ForeignKey("devices.id"), nullable=True)
    upload_method = Column(SQLEnum(UploadMethod), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    processing_status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING)
    metadata = Column(JSON, nullable=True)  # File metadata (columns, shape, etc.)
    error_message = Column(Text, nullable=True)  # Error message if processing failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    device = relationship("Device", back_populates="data_files")
    clustering_results = relationship("ClusteringResult", back_populates="data_file", cascade="all, delete-orphan")
    notebook_sessions = relationship("NotebookSession", back_populates="data_file", cascade="all, delete-orphan")


class ClusteringResult(Base):
    """Clustering result model"""
    __tablename__ = "clustering_results"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    data_file_id = Column(String, ForeignKey("data_files.id"), nullable=False)
    algorithm = Column(String, nullable=False)  # e.g., "HDBSCAN", "K-Means"
    parameters = Column(JSON, nullable=True)  # Algorithm parameters
    cluster_labels = Column(JSON, nullable=False)  # Cluster labels array
    metrics = Column(JSON, nullable=True)  # Clustering metrics
    visualization_path = Column(String, nullable=True)  # Path to saved visualization
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    data_file = relationship("DataFile", back_populates="clustering_results")


class NotebookSession(Base):
    """Notebook session model"""
    __tablename__ = "notebook_sessions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    data_file_id = Column(String, ForeignKey("data_files.id"), nullable=False)
    notebook_path = Column(String, nullable=False)  # Path to notebook file
    kernel_id = Column(String, nullable=True)  # Jupyter kernel ID
    status = Column(SQLEnum(NotebookStatus), default=NotebookStatus.CREATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    data_file = relationship("DataFile", back_populates="notebook_sessions")

