from pydantic import BaseModel, Field, ConfigDict


class LocationResponse(BaseModel):
    """Response model for location details."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "location_id": 1,
                "city": "Warszawa",
                "locality": "Śródmieście",
                "city_district": "Śródmieście Północne",
                "street": "Marszałkowska",
                "full_address": "Marszałkowska 1, 00-001 Warszawa",
                "latitude": 52.2297,
                "longitude": 21.0122,
            }
        }
    )

    location_id: int = Field(..., description="Unique identifier of the location")
    city: str | None = Field(None, description="City name")
    locality: str | None = Field(None, description="Locality or neighborhood")
    city_district: str | None = Field(None, description="City district")
    street: str | None = Field(None, description="Street name")
    full_address: str | None = Field(None, description="Full address string")
    latitude: float | None = Field(None, description="Latitude coordinate")
    longitude: float | None = Field(None, description="Longitude coordinate")


