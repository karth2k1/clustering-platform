"""File management API endpoints"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import DataFileResponse, DataFileListResponse, FileUploadResponse
from app.services.file_service import FileService
from app.models import FileType, ProcessingStatus, UploadMethod
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/api/files", tags=["files"])


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    device_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Upload a file (CSV or JSON)"""
    try:
        # Read file content
        content = await file.read()
        
        # Process file
        data_file, error = FileService.process_file(
            db=db,
            file_content=content,
            original_filename=file.filename,
            device_id=device_id,
            upload_method=UploadMethod.MANUAL
        )
        
        if error:
            raise HTTPException(status_code=400, detail=error)
        
        return FileUploadResponse(
            file_id=data_file.id,
            filename=data_file.filename,
            status=data_file.processing_status.value,
            message="File uploaded successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/upload-multiple", response_model=List[FileUploadResponse])
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    device_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Upload multiple files"""
    results = []
    errors = []
    
    for file in files:
        try:
            content = await file.read()
            data_file, error = FileService.process_file(
                db=db,
                file_content=content,
                original_filename=file.filename,
                device_id=device_id,
                upload_method=UploadMethod.MANUAL
            )
            
            if error:
                errors.append(f"{file.filename}: {error}")
            else:
                results.append(FileUploadResponse(
                    file_id=data_file.id,
                    filename=data_file.filename,
                    status=data_file.processing_status.value,
                    message="File uploaded successfully"
                ))
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    if errors:
        # Return partial success with errors
        pass  # Could include errors in response
    
    return results


@router.get("", response_model=DataFileListResponse)
def list_files(
    device_id: Optional[str] = Query(None),
    file_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List files with optional filters"""
    # Convert string enums
    file_type_enum = FileType[file_type] if file_type else None
    status_enum = ProcessingStatus[status] if status else None
    
    skip = (page - 1) * page_size
    files, total = FileService.list_files(
        db=db,
        device_id=device_id,
        file_type=file_type_enum,
        status=status_enum,
        skip=skip,
        limit=page_size
    )
    
    return DataFileListResponse(
        files=[DataFileResponse.model_validate(f) for f in files],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{file_id}", response_model=DataFileResponse)
def get_file(file_id: str, db: Session = Depends(get_db)):
    """Get file details"""
    data_file = FileService.get_file(db, file_id)
    if not data_file:
        raise HTTPException(status_code=404, detail="File not found")
    return DataFileResponse.model_validate(data_file)


@router.delete("/{file_id}")
def delete_file(file_id: str, db: Session = Depends(get_db)):
    """Delete a file"""
    success = FileService.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted successfully"}


@router.get("/{file_id}/download")
def download_file(file_id: str, db: Session = Depends(get_db)):
    """Download original file"""
    data_file = FileService.get_file(db, file_id)
    if not data_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = FileService.get_file_path_for_download(data_file)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=str(file_path),
        filename=data_file.original_filename,
        media_type="application/octet-stream"
    )

