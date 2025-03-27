from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Person(Base):
    __tablename__ = 'persons'
    
    person_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    type = Column(String(20)) # Herency discriminator (patient/contact)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }