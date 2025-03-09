import jwt
from config import config_manager
from datetime import timedelta, datetime, timezone
from application.interface.security.jwt_security import JWTSecurityProtocol


class JWTSecurity(JWTSecurityProtocol):
    """Сервис для работы с JWT токенами"""
    def encode_jwt(
        self,
        payload: dict,
        expire_timedelta: timedelta | None = None,
        private_key: str = config_manager.jwt.PRIVATE_KEY.read_text(),
        algorithm: str = config_manager.jwt.ALGORITHM
        ):
        """Кодирует JWT токен"""
        
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
        encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
        return encoded
    
    def decode_jwt(
        self,
        jwt_token: str,
        public_key: str = config_manager.jwt.PUBLIC_KEY.read_text(),
        algoritm: str = config_manager.jwt.ALGORITHM,
        ):
        """Декодирует JWT токен"""  
        decoded = jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algoritm])
        return decoded
