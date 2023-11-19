# FastAPI
from app.core.config import configuration
from app.services.users import users_service
from app.dependencies import auth_service
from app.dependencies import TokenData
from app.interfaces.user import User, UserUpdate
from app.dependencies import Res
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
# JWT
# Services
# Settings

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/users',
)


@router.post(
    '',
    response_model=Res[str],
    response_description='El ID del dato insertado',
)
async def register(user: User):
    inserted_user = users_service.register(user)

    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'success': True,
            'body': str(inserted_user),
        },
    )


@router.get(
    '',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth)],

)
async def get(tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    data_user = users_service.get_by_id(tokenData.id)
    return responses.JSONResponse(

        status_code=200,
        content={
            'success': True,
            'body': {
                "name" : data_user.name,
                "email" : data_user.email
            },
        }
    )


@router.patch(
    '/update',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth)],

)
async def update(userUpdate: UserUpdate, tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    users_service.update(userUpdate, tokenData)
    return responses.JSONResponse(
        status_code=200,
        content={
            'success': True,
            'body': "Usuario actualizado con exito",
        }
    )
