from datetime import date
from decimal import Decimal
from typing import Optional
from sqlalchemy import Numeric
from sqlmodel import SQLModel, Field, Relationship


class Location(SQLModel, table=True):
    """Location model - geographic information."""
    
    __tablename__ = "location"

    location_id: Optional[int] = Field(default=None, primary_key=True)
    city: Optional[str] = Field(default=None, max_length=255)
    locality: Optional[str] = Field(default=None, max_length=255)
    city_district: Optional[str] = Field(default=None, max_length=255)
    street: Optional[str] = Field(default=None, max_length=255)
    full_address: Optional[str] = Field(default=None, max_length=500)
    latitude: Optional[Decimal] = Field(default=None, sa_column=Numeric(9, 6))
    longitude: Optional[Decimal] = Field(default=None, sa_column=Numeric(9, 6))

    # Relationship
    listings: list["Listing"] = Relationship(back_populates="location")


class Building(SQLModel, table=True):
    """Building model - building details."""
    
    __tablename__ = "building"

    building_id: Optional[int] = Field(default=None, primary_key=True)
    year_built: Optional[int] = Field(default=None)
    building_type: Optional[str] = Field(default=None, max_length=100)
    floor: Optional[int] = Field(default=None)

    # Relationship
    listings: list["Listing"] = Relationship(back_populates="building")


class Owner(SQLModel, table=True):
    """Owner model - owner information."""
    
    __tablename__ = "owner"

    owner_id: Optional[int] = Field(default=None, primary_key=True)
    owner_type: Optional[str] = Field(default=None, max_length=50)
    contact_name: Optional[str] = Field(default=None, max_length=255)
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    contact_email: Optional[str] = Field(default=None, max_length=255)

    # Relationship
    listings: list["Listing"] = Relationship(back_populates="owner")


class Features(SQLModel, table=True):
    """Features model - property features."""
    
    __tablename__ = "features"

    features_id: Optional[int] = Field(default=None, primary_key=True)
    has_basement: Optional[bool] = Field(default=None)
    has_parking: Optional[bool] = Field(default=None)
    kitchen_type: Optional[str] = Field(default=None, max_length=100)
    window_type: Optional[str] = Field(default=None, max_length=100)
    ownership_type: Optional[str] = Field(default=None, max_length=100)
    equipment: Optional[str] = Field(default=None)

    # Relationship
    listings: list["Listing"] = Relationship(back_populates="features")


class Listing(SQLModel, table=True):
    """Listing model - real estate listings."""
    
    __tablename__ = "listing"

    listing_id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="location.location_id")
    building_id: int = Field(foreign_key="building.building_id")
    owner_id: int = Field(foreign_key="owner.owner_id")
    features_id: int = Field(foreign_key="features.features_id")
    rooms: Optional[int] = Field(default=None)
    area: Optional[Decimal] = Field(default=None, sa_column=Numeric(6, 2))
    price_total_zl: Optional[Decimal] = Field(default=None, sa_column=Numeric(12, 2))
    price_sqm_zl: Optional[Decimal] = Field(default=None, sa_column=Numeric(12, 2))
    price_per_sqm_detailed: Optional[Decimal] = Field(default=None, sa_column=Numeric(12, 2))
    date_posted: Optional[date] = Field(default=None)
    photo_count: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    description_text: Optional[str] = Field(default=None)

    # Relationships
    location: Location = Relationship(back_populates="listings")
    building: Building = Relationship(back_populates="listings")
    owner: Owner = Relationship(back_populates="listings")
    features: Features = Relationship(back_populates="listings")
