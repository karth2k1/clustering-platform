"""File processing service"""
import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Optional, Tuple
from app.models import DataFile, FileType, UploadMethod, ProcessingStatus
from app.utils.file_storage import save_uploaded_file, get_file_path, get_file_size
from app.utils.json_parser import parse_json_file, parse_json_content, extract_file_metadata
from app.config import settings, UPLOAD_DIR


class FileService:
    """Service for handling file operations"""
    
    @staticmethod
    def validate_file(file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
        """Validate uploaded file"""
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        
        # Check file size
        if len(file_content) > settings.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE / (1024*1024):.0f}MB"
        
        return True, None
    
    @staticmethod
    def process_file(
        db: Session,
        file_content: bytes,
        original_filename: str,
        device_id: Optional[str] = None,
        upload_method: UploadMethod = UploadMethod.MANUAL
    ) -> Tuple[Optional[DataFile], Optional[str]]:
        """Process and store uploaded file"""
        try:
            # Validate file
            is_valid, error = FileService.validate_file(file_content, original_filename)
            if not is_valid:
                return None, error
            
            # Determine file type
            file_ext = Path(original_filename).suffix.lower()
            file_type = FileType.JSON if file_ext == ".json" else FileType.CSV
            
            # Save file
            stored_filename, file_path = save_uploaded_file(file_content, original_filename, device_id)
            file_size = get_file_size(file_path)
            
            # Create database record
            data_file = DataFile(
                filename=stored_filename,
                original_filename=original_filename,
                file_path=str(file_path.relative_to(UPLOAD_DIR)),
                file_type=file_type,
                file_size=file_size,
                device_id=device_id,
                upload_method=upload_method,
                processing_status=ProcessingStatus.PENDING
            )
            
            db.add(data_file)
            db.flush()  # Get the ID
            
            # Process file to extract metadata
            try:
                if file_type == FileType.JSON:
                    df, parse_error = parse_json_file(file_path)
                else:
                    df, parse_error = pd.read_csv(file_path), None
                
                if parse_error:
                    data_file.processing_status = ProcessingStatus.FAILED
                    data_file.error_message = parse_error
                    db.commit()
                    return data_file, parse_error
                
                # Extract metadata
                metadata = extract_file_metadata(df)
                data_file.file_metadata = metadata
                data_file.processing_status = ProcessingStatus.COMPLETED
                
            except Exception as e:
                data_file.processing_status = ProcessingStatus.FAILED
                data_file.error_message = str(e)
            
            db.commit()
            return data_file, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error processing file: {str(e)}"
    
    @staticmethod
    def get_file(db: Session, file_id: str) -> Optional[DataFile]:
        """Get file by ID"""
        return db.query(DataFile).filter(DataFile.id == file_id).first()
    
    @staticmethod
    def list_files(
        db: Session,
        device_id: Optional[str] = None,
        file_type: Optional[FileType] = None,
        status: Optional[ProcessingStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[list[DataFile], int]:
        """List files with filters"""
        query = db.query(DataFile)
        
        if device_id:
            query = query.filter(DataFile.device_id == device_id)
        if file_type:
            query = query.filter(DataFile.file_type == file_type)
        if status:
            query = query.filter(DataFile.processing_status == status)
        
        total = query.count()
        files = query.order_by(DataFile.created_at.desc()).offset(skip).limit(limit).all()
        
        return files, total
    
    @staticmethod
    def delete_file(db: Session, file_id: str) -> bool:
        """Delete file and its database record"""
        data_file = FileService.get_file(db, file_id)
        if not data_file:
            return False
        
        try:
            # Delete physical file
            from app.utils.file_storage import delete_file
            delete_file(data_file.filename, data_file.device_id)
            
            # Delete database record (cascade will handle related records)
            db.delete(data_file)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
    
    @staticmethod
    def get_file_path_for_download(data_file: DataFile) -> Path:
        """Get full path to file for download"""
        return get_file_path(data_file.filename, data_file.device_id)
    
    @staticmethod
    def update_file_device_association(db: Session, file_id: str, device_id: Optional[str]) -> bool:
        """Update device association for a file"""
        data_file = FileService.get_file(db, file_id)
        if not data_file:
            return False
        
        try:
            data_file.device_id = device_id
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

