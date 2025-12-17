"""Device management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceDeleteRequest
from app.services.device_service import DeviceService
from app.services.webapi_client import get_api_client

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.post("", response_model=DeviceResponse)
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device"""
    # Check if device name already exists
    existing = DeviceService.get_device_by_name(db, device_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Device with this name already exists")
    
    device = DeviceService.create_device(db, device_data)
    return DeviceResponse.model_validate(device)


@router.get("", response_model=List[DeviceResponse])
def list_devices(active_only: bool = False, db: Session = Depends(get_db)):
    """List all devices"""
    devices = DeviceService.list_devices(db, active_only=active_only)
    return [DeviceResponse.model_validate(d) for d in devices]


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """Get device details"""
    device = DeviceService.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceResponse.model_validate(device)


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: str,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """Update device"""
    device = DeviceService.update_device(db, device_id, device_data)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceResponse.model_validate(device)


@router.delete("/{device_id}")
def delete_device(
    device_id: str,
    delete_request: DeviceDeleteRequest,
    db: Session = Depends(get_db)
):
    """Delete device with option to save or delete associated files"""
    success, file_count = DeviceService.delete_device(
        db,
        device_id,
        save_data_files=delete_request.save_data_files
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    
    action = "saved" if delete_request.save_data_files else "deleted"
    return {
        "message": f"Device deleted successfully. {file_count} files {action}.",
        "files_affected": file_count
    }


@router.post("/{device_id}/sync")
def sync_device(device_id: str, db: Session = Depends(get_db)):
    """Manually sync data from device via WebAPI"""
    device = DeviceService.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if not device.is_active:
        raise HTTPException(status_code=400, detail="Device is not active")
    
    # Get API client
    client = get_api_client(db, device_id)
    if not client:
        raise HTTPException(status_code=400, detail="API client not available for this device")
    
    # Fetch data (device-specific logic)
    if device.device_type.lower() == "intersight":
        from app.services.webapi_client import IntersightAPIClient
        if isinstance(client, IntersightAPIClient):
            data, error = client.fetch_alarms()
        else:
            data, error = client.fetch_data()
    else:
        data, error = client.fetch_data()
    
    if error:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {error}")
    
    # Process and save fetched data
    import json
    from app.services.file_service import FileService
    from datetime import datetime
    
    # Convert data to JSON string
    json_content = json.dumps(data, default=str)
    
    # Create filename
    filename = f"{device.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Process file
    data_file, file_error = FileService.process_file(
        db=db,
        file_content=json_content.encode('utf-8'),
        original_filename=filename,
        device_id=device_id,
        upload_method=UploadMethod.API
    )
    
    if file_error:
        raise HTTPException(status_code=500, detail=f"Error saving fetched data: {file_error}")
    
    # Update device last sync
    DeviceService.update_last_sync(db, device_id)
    
    return {
        "message": "Device synced successfully",
        "file_id": data_file.id,
        "records_fetched": len(data) if data else 0
    }

