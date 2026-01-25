from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Institution(BaseModel):
    __tablename__ = "institutions"
    
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)  # Institution code/abbreviation
    address = Column(Text, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)  # URL/path to institution logo
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="institution")
    sports = relationship("Sport", back_populates="institution")
    teams = relationship("Team", back_populates="institution")
    venues = relationship("Venue", back_populates="institution")
    tournaments = relationship("Tournament", back_populates="institution")
