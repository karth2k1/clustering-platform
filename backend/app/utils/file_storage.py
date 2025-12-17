"""File storage utilities"""
import shutil
from pathlib import Path
from typing import Tuple, Optional
import uuid
from datetime import datetime
from app.config import settings


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with timestamp and UUID"""
    file_ext = Path(original_filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{file_ext}"


def save_uploaded_file(file_content: bytes, original_filename: str, device_id: Optional[str] = None) -> Tuple[str, Path]:
    """
    Save uploaded file to storage
    
    Returns:
        Tuple of (stored_filename, file_path)
    """
    # Generate unique filename
    stored_filename = generate_unique_filename(original_filename)
    
    # Create device-specific subdirectory if device_id provided
    if device_id:
        device_dir = settings.UPLOAD_DIR / device_id
        device_dir.mkdir(parents=True, exist_ok=True)
        file_path = device_dir / stored_filename
    else:
        file_path = settings.UPLOAD_DIR / stored_filename
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    return stored_filename, file_path


def get_file_path(filename: str, device_id: Optional[str] = None) -> Path:
    """Get full path to stored file"""
    if device_id:
        return settings.UPLOAD_DIR / device_id / filename
    return settings.UPLOAD_DIR / filename


def delete_file(filename: str, device_id: Optional[str] = None) -> bool:
    """Delete file from storage"""
    try:
        file_path = get_file_path(filename, device_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def delete_device_files(device_id: str) -> int:
    """Delete all files associated with a device"""
    try:
        device_dir = settings.UPLOAD_DIR / device_id
        if device_dir.exists():
            file_count = len(list(device_dir.iterdir()))
            shutil.rmtree(device_dir)
            return file_count
        return 0
    except Exception:
        return 0


def move_device_files_to_general(device_id: str) -> int:
    """Move device files to general upload directory"""
    try:
        device_dir = settings.UPLOAD_DIR / device_id
        if not device_dir.exists():
            return 0
        
        file_count = 0
        for file_path in device_dir.iterdir():
            if file_path.is_file():
                new_path = settings.UPLOAD_DIR / file_path.name
                # Handle name conflicts
                if new_path.exists():
                    new_path = settings.UPLOAD_DIR / generate_unique_filename(file_path.name)
                shutil.move(str(file_path), str(new_path))
                file_count += 1
        
        # Remove empty device directory
        if device_dir.exists():
            device_dir.rmdir()
        
        return file_count
    except Exception:
        return 0


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes"""
    return file_path.stat().st_size if file_path.exists() else 0

