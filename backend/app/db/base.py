from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

# Create a naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

# Add common attributes to all models
class BaseModel:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower() 