from sqlalchemy.orm import Session
from models.auth import User, UserRole
from typing import Optional


def is_admin(user: User) -> bool:
    """Check if user is an admin"""
    return user.role == UserRole.ADMIN


def is_organizer(user: User) -> bool:
    """Check if user is an organizer"""
    return user.role == UserRole.ORGANIZER


def is_admin_or_organizer(user: User) -> bool:
    """Check if user is admin or organizer"""
    return user.role in [UserRole.ADMIN, UserRole.ORGANIZER]


def can_manage_institution(user: User, institution_id: int) -> bool:
    """Check if user can manage a specific institution"""
    if is_admin(user):
        return True
    if user.institution_id == institution_id and is_organizer(user):
        return True
    return False
