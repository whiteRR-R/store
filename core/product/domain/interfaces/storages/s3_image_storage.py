from typing import Any, Protocol

class S3ImageStorageProtocol(Protocol):
    async def upload(self, staging_path, file_name) -> str:
        """Upload image"""
        pass
    
    async def delete(self, url: str) -> None:
        """Delete image"""
        pass
