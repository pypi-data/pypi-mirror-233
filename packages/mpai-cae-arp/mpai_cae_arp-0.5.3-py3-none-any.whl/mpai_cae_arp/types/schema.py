"""Classes for the API informations."""

from pydantic import BaseModel, ConfigDict, Field


class Contact(BaseModel):
    """Contact information for the owners of the API.

    Attributes
    ----------
    name : str
        Name of the contact person.
    email : str
        Email of the contact person.

    """

    name: str = Field(..., description="Name of the contact person.")
    email: str = Field(..., description="Email of the contact person.")
    model_config = ConfigDict(  # type: ignore
        json_schema_extra={"example": {"name": "John Doe", "email": "email@email.com"}},
    )


class License(BaseModel):
    """License information for the API.

    Attributes
    ----------
    name : str
        Name of the license.
    url : str
        URL of the license.

    """

    name: str = Field(..., description="Name of the license.")
    url: str = Field(..., description="URL of the license.")
    model_config = ConfigDict(
        json_schema_extra={  # type: ignore
            "example": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
        },
    )


class Info(BaseModel):
    """Information about the API.

    Attributes
    ----------
    title : str
        The title of the API.
    description : str
        A short description of the API.
    version : str
        The version of the API.
    contact : Contact
        Contact information for the owners of the API.
    license_info : License
        License information for the API.

    """

    title: str = Field(..., description="The title of the API.")
    description: str = Field(..., description="A short description of the API.")
    version: str = Field(..., description="The version of the API.")
    contact: Contact = Field(
        ...,
        description="Contact information for the owners of the API.",
    )
    license_info: License = Field(..., description="License information for the API.")
    model_config = ConfigDict(  # type: ignore
        json_schema_extra={
            "example": {
                "title": "API title",
                "description": "A very nice API",
                "version": "0.1.0",
                "contact": {
                    "name": "John Doe",
                    "email": "example@example.com",
                },
                "license_info": {
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT",
                },
            },
        },
    )
