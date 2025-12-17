"""Device management service"""
from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from app.models import Device, DataFile
from app.schemas import DeviceCreate, DeviceUpdate
from app.utils.encryption import encrypt_data, decrypt_data


class DeviceService:
    """Service for managing devices"""
    
    @staticmethod
    def create_device(db: Session, device_data: DeviceCreate) -> Device:
        """Create a new device"""
        device = Device(
            name=device_data.name,
            device_type=device_data.device_type,
            api_endpoint=device_data.api_endpoint,
            api_key_encrypted=encrypt_data(device_data.api_key) if device_data.api_key else None,
            configuration=device_data.configuration,
            is_active=True
        )
        
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
    
    @staticmethod
    def get_device(db: Session, device_id: str) -> Optional[Device]:
        """Get device by ID"""
        return db.query(Device).filter(Device.id == device_id).first()
    
    @staticmethod
    def get_device_by_name(db: Session, name: str) -> Optional[Device]:
        """Get device by name"""
        return db.query(Device).filter(Device.name == name).first()
    
    @staticmethod
    def list_devices(db: Session, active_only: bool = False) -> List[Device]:
        """List all devices"""
        query = db.query(Device)
        if active_only:
            query = query.filter(Device.is_active == True)
        return query.order_by(Device.created_at.desc()).all()
    
    @staticmethod
    def update_device(db: Session, device_id: str, device_data: DeviceUpdate) -> Optional[Device]:
        """Update device"""
        device = DeviceService.get_device(db, device_id)
        if not device:
            return None
        
        if device_data.name is not None:
            device.name = device_data.name
        if device_data.device_type is not None:
            device.device_type = device_data.device_type
        if device_data.api_endpoint is not None:
            device.api_endpoint = device_data.api_endpoint
        if device_data.api_key is not None:
            device.api_key_encrypted = encrypt_data(device_data.api_key)
        if device_data.configuration is not None:
            device.configuration = device_data.configuration
        if device_data.is_active is not None:
            device.is_active = device_data.is_active
        
        db.commit()
        db.refresh(device)
        return device
    
    @staticmethod
    def delete_device(
        db: Session,
        device_id: str,
        save_data_files: bool = True
    ) -> Tuple[bool, int]:
        """
        Delete device
        
        Args:
            db: Database session
            device_id: Device ID to delete
            save_data_files: If True, keep files but remove device association. If False, delete all files.
        
        Returns:
            Tuple of (success, files_affected_count)
        """
        device = DeviceService.get_device(db, device_id)
        if not device:
            return False, 0
        
        # Get count of associated files
        file_count = db.query(DataFile).filter(DataFile.device_id == device_id).count()
        
        try:
            if save_data_files:
                # Remove device association from files
                db.query(DataFile).filter(DataFile.device_id == device_id).update(
                    {DataFile.device_id: None}
                )
                # Move files from device directory to general directory
                from app.utils.file_storage import move_device_files_to_general
                move_device_files_to_general(device_id)
            else:
                # Delete all associated files
                files = db.query(DataFile).filter(DataFile.device_id == device_id).all()
                for file in files:
                    from app.services.file_service import FileService
                    FileService.delete_file(db, file.id)
            
            # Delete device
            db.delete(device)
            db.commit()
            
            return True, file_count
        except Exception:
            db.rollback()
            return False, 0
    
    @staticmethod
    def get_device_api_key(device: Device) -> Optional[str]:
        """Get decrypted API key for device"""
        if device.api_key_encrypted:
            return decrypt_data(device.api_key_encrypted)
        return None
    
    @staticmethod
    def update_last_sync(db: Session, device_id: str) -> bool:
        """Update device last sync timestamp"""
        from datetime import datetime
        device = DeviceService.get_device(db, device_id)
        if not device:
            return False
        
        device.last_sync = datetime.utcnow()
        db.commit()
        return True

