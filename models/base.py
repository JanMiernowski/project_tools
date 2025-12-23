from sqlmodel import SQLModel

# Base for Alembic migrations - SQLModel provides metadata
# Models should inherit from SQLModel with table=True
# For Alembic: use SQLModel.metadata (accessed via Base.metadata)
Base = SQLModel

