from typing import List, Optional
from pydantic import BaseModel, Field
from quest_maker_api_shared_library.custom_types import PydanticObjectId


class UserCreate(BaseModel):
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str = 'regular'
    auth_id: PydanticObjectId = Field(alias='auth_id')


class UserUpdate(BaseModel):
    email: Optional[str] =  None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []


class UserResponse(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str
    auth_id: PydanticObjectId = Field(alias='auth_id')
    createdAt: str
    updatedAt: str


class UserInDB(BaseModel):
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str
    auth_id: PydanticObjectId = Field(alias='auth_id')
    createdAt: str
    updatedAt: str
