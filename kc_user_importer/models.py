
from typing import Optional
from pydantic import BaseModel, Field, computed_field


class User(BaseModel):
    """
    A Microsoft AD USER from Users/bulk_download
    """

    userPrincipalName: str
    displayName: str
    surname: str
    mail: str
    givenName: str
    id: str
    userType: str
    jobTitle: str
    department: str
    accountEnabled: bool
    usageLocation: str
    streetAddress: str
    state: str
    country: str
    officeLocation: str
    city: str
    postalCode: str
    telephoneNumber: str
    mobilePhone: str
    alternateEmailAddress: str
    ageGroup: str
    consentProvidedForMinor: str
    legalAgeGroupClassification: str
    companyName: str
    creationType: str
    directorySynced: str
    invitationState: str
    identityIssuer: str
    createdDateTime: str


class GroupUserInfo(BaseModel):
    """
    A Microsoft AD USER from Groups/bulk_download
    """
    id: str
    userPrincipalName: str
    displayName: str
    objectType: str
    userType: str
    isUser: bool
    isGroup: bool
    isGuest: bool

    @computed_field
    @property
    def email(self) -> str:
        email = self.userPrincipalName
        email = email.split("#", 1)[0] if "#" in email else email
        email = email.rsplit("_", maxsplit=1)
        if len(email) == 1:
            return email[0]
        return "@".join(email)


class UserRepresentation(BaseModel):
    """
    Keycloak v1.2 UserRepresentation Schema
    """
    id: Optional[str] = None
    username: str
    createdTimestamp: Optional[int] = None
    totp: Optional[bool] = None
    email: str
    firstName: str
    lastName: str
    enabled: bool = Field(default=True)
    emailVerified: bool = Field(default=False)
    attributes: Optional[dict] = Field(default={})
    groups: Optional[list] = []
    disableCredentialTypes: Optional[list] = []
    requiredActions: Optional[list] = []
    notBefore: Optional[int] = 0
    access: Optional[dict] = {}
