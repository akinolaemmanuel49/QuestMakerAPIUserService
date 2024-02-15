from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from quest_maker_api_shared_library.token_manager import TokenManager
from quest_maker_api_shared_library.custom_types import PydanticObjectId

from core.config.env import Env
from core.models.user import UserCreate, UserResponse, UserUpdate
from core.services.user import UserService

users = APIRouter()
bearer = HTTPBearer()
service = UserService()
env = Env()
token_manager = TokenManager(key=env.JWT_SECRET_KEY.get_secret_value(),
                             jwt_expiration_time_in_minutes=env.JWT_EXPIRATION_TIME_IN_MINUTES,)


@users.post('/', status_code=HTTPStatus.CREATED)
# Create new user
def create_user(data: UserCreate, token: HTTPAuthorizationCredentials = Security(bearer)) -> Optional[PydanticObjectId]:
    try:
        id = service.create(data=data)
    except HTTPException:
        raise HTTPException(
            status_code=400, detail="Invalid request or unauthorized access")
    payload = token_manager.decode_token(token=token.credentials)
    if payload:
        scope = str(payload['scope'])
        if 'access_token' in scope.split():
            if str(data.auth_id) == str(payload['sub']):
                return id
            else:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized access")


# Fetch a user
@users.get('/')
def read_user(token: HTTPAuthorizationCredentials = Security(bearer)) -> UserResponse:
    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = str(payload['sub'])
        return service.read(auth_id=auth_id)
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


# Update a user
@users.put('/', status_code=HTTPStatus.OK)
def update_user(data: Union[UserUpdate, Dict[str, Any]], token: HTTPAuthorizationCredentials = Security(bearer)):
    if isinstance(data, UserUpdate):
        data = data.model_dump(exclude_unset=True)

    payload = token_manager.decode_token(token=token.credentials)
    auth_id = str(payload['sub'])

    try:
        valid = service.update(auth_id=auth_id, data=data)
    except HTTPException:
        raise HTTPException(
            status_code=400, detail="Invalid request or unauthorized access")

    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        if valid:
            return 'Successfully updated'
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


# Fetch all users
@users.post('/list/')
def fetch_users(organization_ids: Optional[List[PydanticObjectId]], role_ids: Optional[List[PydanticObjectId]], token: HTTPAuthorizationCredentials = Security(bearer)):
    payload = token_manager.decode_token(token=token.credentials)
    scope = payload['scope']
    if 'access_token' in scope.split():
        auth_id = payload['sub']
        return service.read_all(auth_id=auth_id, organization_ids=organization_ids, role_ids=role_ids)
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


# Delete a user
@users.delete('/', status_code=HTTPStatus.NO_CONTENT)
def delete_user(token: HTTPAuthorizationCredentials = Security(bearer)):
    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = str(payload['sub'])
        service.delete(auth_id=auth_id)
        return 'Successfully deleted'
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})
