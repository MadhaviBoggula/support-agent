from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):

    name: str = Field(
        min_length=1
    )

    age: int = Field(
        gt=0,
        lt=120
    )

    mobile: str = Field(
        min_length=10,
        max_length=20
    )

    location: str = Field(
        min_length=1
    )


class UserProfileUpdate(BaseModel):

    name: str | None = None

    age: int | None = Field(
        default=None,
        gt=0,
        lt=120
    )

    mobile: str | None = None

    location: str | None = None