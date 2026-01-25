from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.auth import User, UserRole
from models.institution import Institution
from schemas.institution import InstitutionCreate, InstitutionResponse, InstitutionUpdate
from schemas.auth import UserCreate, UserResponse, UserUpdate
from dependencies import get_current_user_required as get_current_user
from security.admin_service import is_admin
from security.auth_service import get_password_hash, get_user_by_email, get_user_by_username

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require admin role"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.post("/institutions", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
async def create_institution(
    name: str = Form(...),
    address: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    contact_phone: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create a new institution (Admin only)"""
    # Auto-generate code from name (e.g., "University of Sports" -> "UOS")
    # If code exists, append a number
    base_code = "".join([word[0].upper() for word in name.split() if word])
    code = base_code
    counter = 1
    
    while db.query(Institution).filter(Institution.code == code).first():
        code = f"{base_code}{counter}"
        counter += 1
        
    logo_url = None
    if logo:
        # Save uploaded file
        import shutil
        import os
        from datetime import datetime
        
        # Create unique filename
        file_ext = os.path.splitext(logo.filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"inst_{code}_{timestamp}{file_ext}"
        file_path = f"static/uploads/{filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)
            
        logo_url = f"/static/uploads/{filename}"
    
    db_institution = Institution(
        name=name,
        code=code,
        address=address,
        contact_email=contact_email,
        contact_phone=contact_phone,
        description=description,
        logo_url=logo_url,
        is_active=True
    )
    
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)
    
    return db_institution


@router.get("/institutions", response_model=List[InstitutionResponse])
async def list_institutions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List all institutions (Admin only)"""
    institutions = db.query(Institution).offset(skip).limit(limit).all()
    return institutions


@router.get("/institutions/{institution_id}", response_model=InstitutionResponse)
async def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get institution by ID (Admin only)"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    return institution


@router.patch("/institutions/{institution_id}", response_model=InstitutionResponse)
async def update_institution(
    institution_id: int,
    institution_update: InstitutionUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update an institution (Admin only)"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    # Check if code is being updated and if it conflicts
    if institution_update.code and institution_update.code != institution.code:
        existing = db.query(Institution).filter(Institution.code == institution_update.code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Institution code already exists"
            )
    
    update_data = institution_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(institution, field, value)
    
    db.commit()
    db.refresh(institution)
    return institution


@router.delete("/institutions/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete an institution (Admin only)"""
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    db.delete(institution)
    db.commit()
    return None


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Create a new user (Admin only)"""
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        institution_id=user_data.institution_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List all users (Admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Get user by ID (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Update a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is being updated and if it conflicts
    if user_update.email and user_update.email != user.email:
        existing = get_user_by_email(db, user_update.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being updated and if it conflicts
    if user_update.username and user_update.username != user.username:
        existing = get_user_by_username(db, user_update.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle password update separately
    if 'password' in update_data:
        password = update_data.pop('password')
        if password:
            user.hashed_password = get_password_hash(password)
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting yourself
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    return None
