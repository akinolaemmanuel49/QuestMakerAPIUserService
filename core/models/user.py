from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from quest_maker_api_shared_library.custom_types import PydanticObjectId


class Organization(BaseModel):
    id: PydanticObjectId = Field(alias='id')
    name: str
    description: Optional[str]
    ownerId: PydanticObjectId = Field(alias='ownerId')
    createdAt: str
    updatedAt: str


class UserCreate(BaseModel):
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
    userType: str = 'regular'
    auth_id: PydanticObjectId = Field(alias='auth_id')


class UserUpdate(BaseModel):
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    # roleIds: Optional[List[PydanticObjectId]] = []
    # organizationIds: Optional[List[PydanticObjectId]] = []
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []


class UserResponse(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
    userType: str
    auth_id: PydanticObjectId = Field(alias='auth_id')
    createdAt: str
    updatedAt: str


class UserInDB(BaseModel):
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
    userType: str
    auth_id: PydanticObjectId = Field(alias='auth_id')
    createdAt: str
    updatedAt: str
