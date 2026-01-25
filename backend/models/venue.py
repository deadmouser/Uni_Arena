from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Venue(BaseModel):
    __tablename__ = "venues"
    
    name = Column(String, nullable=False, index=True)
    address = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=True)
    facilities = Column(Text, nullable=True)  # JSON string or comma-separated
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    # Relationships
    institution = relationship("Institution", back_populates="venues")
    matches = relationship("Match", back_populates="venue")
