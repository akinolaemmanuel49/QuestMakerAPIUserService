from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from quest_maker_api_shared_library.custom_types import PydanticObjectId

from core.config.database import UserDatabase
from core.models.user import UserCreate, UserInDB, UserResponse, UserUpdate
from core.config.env import Env


env = Env()
db = UserDatabase()


class UserService:
    def create(self, data: UserCreate):
        try:
            # Load data into UserInDB container
            user = UserInDB(
                email=data.email,
                firstName=data.firstName,
                lastName=data.lastName,
                roles=data.roles,
                organizations=data.organizations,
                userType=data.userType,
                auth_id=str(data.auth_id),
                createdAt=str(datetime.utcnow()),
                updatedAt=str(datetime.utcnow())
            )

            # Convert the UserInDB container into a dict
            user_dict = user.model_dump()
            if user_dict.get('organizations'):
                for organization in user_dict['organizations']:
                    organization['id'] = ObjectId(organization['id'])
                    organization['ownerId'] = ObjectId(organization['ownerId'])
            if user_dict.get('roles'):
                for role in user_dict['roles']:
                    role['id'] = ObjectId(role['id'])
                    role['organizationId'] = ObjectId(role['organizationId'])

            # Create a new user instance in database collection
            document = db.user_collection.insert_one(user_dict)

            # Return new user instance _id
            return document.inserted_id

        except DuplicateKeyError:
            raise ValueError(
                'A user with this email or auth_id already exists')

        except Exception as e:
            raise e

    def read(self, auth_id: PydanticObjectId):
        try:
            document = db.user_collection.find_one(
                {'auth_id': ObjectId(auth_id)})

            # Convert ObjectId's to strings
            document['_id'] = str(document['_id'])
            document['auth_id'] = str(document['auth_id'])
            if document['organizations']:
                for organization in document['organizations']:
                    organization['id'] = str(organization['id'])
            if document['roles']:
                for role in document['roles']:
                    role['id'] = str(role['id'])
            document = UserResponse(**document)
            return document
        except Exception as e:
            raise e

    def read_all(self, auth_id: PydanticObjectId, organization_ids: Optional[List[PydanticObjectId]], role_ids: Optional[List[PydanticObjectId]]):
        result: List[UserResponse] = []
        query = {}

        user = self.read(auth_id=auth_id)

        if organization_ids:
            # Check if the user is a member of the requested organizations
            if not all(organization_id in user.organizations for organization_id in user.organizations):
                raise ValueError('Unauthorized access to organizations')
            query['organizations']['id'] = {'$in': organization_ids}

        if role_ids:
            query['roles']['id'] = {'$in': role_ids}

        try:
            # document = db.user_collection.find_one({'_id': ObjectId(auth_id)})
            documents = db.user_collection.find(query)
            # Iterate through documents
            for document in documents:
                # Convert ObjectId's to string
                document['_id'] = str(document['_id'])
                document['auth_id'] = str(document['auth_id'])
                if document['organizations']:
                    for organization in document['organizations']:
                        organization['id'] = str(organization['id'])
                        organization['ownerId'] = str(organization['ownerId'])
                if document['roles']:
                    for role in document['roles']:
                        role['_id'] = str(role['_id'])
                        role['organizationId'] = str(role['organizationId'])
                document = UserResponse(**document)
                result.append(document)
            return result
        except Exception as e:
            raise e

    def update(self, auth_id: PydanticObjectId, data: Union[UserUpdate, Dict[str, Any]]):
        try:
            if isinstance(data, UserUpdate):
                data = data.model_dump(exclude_unset=True)
            # Update and convert date in updatedAt field to string
            data['updatedAt'] = str(datetime.utcnow())
            if data.get('organizations'):
                for organization in data['organizations']:
                    organization['id'] = ObjectId(organization['id'])
                    organization['ownerId'] = ObjectId(organization['ownerId'])
            if data.get('roles'):
                for role in data['roles']:
                    role['_id'] = ObjectId(role['_id'])
                    role['organizationId'] = ObjectId(role['organizationId'])

            # Find and update a user instance
            db.user_collection.update_one(
                {'auth_id': ObjectId(auth_id)}, {'$set': data})
            return True
        except Exception as e:
            raise e

    def delete(self, auth_id: PydanticObjectId):
        try:
            db.user_collection.delete_one({'auth_id': ObjectId(auth_id)})
        except Exception as e:
            raise e
