"""Notebook API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NotebookCreateRequest, NotebookCreateResponse, NotebookSessionResponse
from app.services.notebook_service import NotebookService

router = APIRouter(prefix="/api/notebooks", tags=["notebooks"])


@router.post("/create", response_model=NotebookCreateResponse)
def create_notebook(request: NotebookCreateRequest, db: Session = Depends(get_db)):
    """Create a notebook from a data file"""
    session, notebook_url, error = NotebookService.create_notebook(
        db=db,
        data_file_id=request.data_file_id
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return NotebookCreateResponse(
        session_id=session.id,
        notebook_url=notebook_url
    )


@router.get("/{session_id}", response_model=NotebookSessionResponse)
def get_notebook_session(session_id: str, db: Session = Depends(get_db)):
    """Get notebook session details"""
    session = NotebookService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Notebook session not found")
    return NotebookSessionResponse.model_validate(session)

