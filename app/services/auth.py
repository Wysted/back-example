from app.dependencies import settings
from app.core.config import configuration
from app.dependencies import typing
from app.dependencies import jwt, JWTError
from app.dependencies import security
from app.dependencies import exceptions
from app.dependencies import status
from app.dependencies import TokenData
import bcrypt
# FastAPI
from app.dependencies import fastapi
from app.dependencies import context
from datetime import datetime, timedelta
# Services
from app.services.users import users_service
# Interfaces
from app.interfaces.auth import Auth as AuthBody
from app.interfaces.token import TokenRes


schema = security.OAuth2PasswordBearer(
    tokenUrl="token",
)


class Auth():
    TOKEN_DATA_KEY = 'token_data'
    _exception = exceptions.HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )

    async def is_auth(self, token: str = fastapi.Depends(schema)) -> None:
        try:
            # Decodifica el token JWT. Remueve el prefijo 'Bearer', utiliza la clave secreta y el algoritmo de la configuración.
            payload = jwt.decode(
                token.replace('Bearer ', ''),
                settings.JWT_SECRET_KEY,
                algorithms=[configuration.jwt_algotithm],
            )

            # Establece los datos del token en un contexto compartido, creando un objeto TokenData con la información del usuario.
            context.setdefault(
                self.TOKEN_DATA_KEY,
                TokenData(
                    id=payload['id'],
                    sub=payload['sub']
                ),
            )
        except JWTError:
            # Lanza una excepción personalizada si hay un error en la decodificación del token.
            raise self._exception

        return context.data.get(self.TOKEN_DATA_KEY)

    def __create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        # Copia los datos a codificar para no modificar el original.
        to_encode = data.copy()

        # Establece la fecha de expiración del token. Utiliza expires_delta si se proporciona, de lo contrario, un valor por defecto.
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=configuration.access_token_expire_minutes)

        # Actualiza los datos a codificar con la fecha de expiración y un sujeto.
        to_encode.update({'exp': expire, 'sub': "jwtTokenTatto"})

        # Codifica los datos en un token JWT usando la clave secreta y el algoritmo de configuración.
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=configuration.jwt_algotithm,
        )

        # Retorna el token JWT codificado.
        return encoded_jwt

    def decode_token(self, token: str = fastapi.Depends(schema)) -> TokenData:
        # Retorna los datos del token almacenados en el contexto global.
        return context.data.get(self.TOKEN_DATA_KEY)

    def login(self, auth: AuthBody) -> TokenRes:
        user = users_service.get_by_email(auth.email)
        if user is None:
            raise exceptions.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email o contraseña no coinciden',
            )
        is_pass = bcrypt.checkpw(
            bytes(auth.password, 'utf-8'),
            bytes(user.password, 'utf-8'),
        )
        if is_pass is False:
            raise exceptions.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email o contraseña no coinciden',
            )
        # Build token

        return TokenRes(
            token=self.__create_access_token(
                {'id': str(user.id)},
            ),
            user={
                'email': user.email,
                'name': user.name,
                'id': str(user.id),
            },
        )


auth_service = Auth()
