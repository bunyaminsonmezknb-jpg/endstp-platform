"""
User Model
Database model for users (students, coaches, admins)
"""

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum


class UserRole(enum.Enum):
    """User roles"""
    STUDENT = "student"
    COACH = "coach"
    ADMIN = "admin"
    INSTITUTION = "institution"


class SubscriptionTier(enum.Enum):
    """Subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    MEDIUM = "medium"
    PREMIUM = "premium"
    INSTITUTION = "institution"


class User:
    """
    User model
    
    Represents all user types (students, coaches, admins, institutions)
    """
    
    __tablename__ = "users"
    
    # Primary Key (same as Supabase auth.users.id)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    
    # Role and subscription
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    subscription_tier = Column(SQLEnum(SubscriptionTier), nullable=False, default=SubscriptionTier.FREE)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    # test_records = relationship("TestRecord", back_populates="user")
    # topic_test_results = relationship("TopicTestResult", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role.value})>"
    
    @property
    def full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email