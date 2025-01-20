import jwt
from config import config_manager
from datetime import timedelta, datetime, timezone
from application.interface.jwt_security import JWTSecurityInterface


class JWTSecurity(JWTSecurityInterface):
    def encode_jwt(
        self,
        payload: dict,
        expire_timedelta: timedelta | None = None,
        private_key: str = config_manager.jwt_settings.private_key.read_text(),
        algorithm: str = config_manager.jwt_settings.alghoritm
        ):
        
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        
        if expire_timedelta:
            expire_time = now + expire_timedelta
        else:
            expire_time = now + timedelta(minutes=15)
        
        to_encode.update(
            iat=now,
            exp=expire_time
        )
        encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
        return encoded
        
    
    def decode_jwt(
        self,
        jwt_token: str,
        public_key: str = config_manager.jwt_settings.public_key.read_text(),
        algoritm: str = config_manager.jwt_settings.alghoritm,
        ):
        
        decoded = jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algoritm])
        return decoded
        