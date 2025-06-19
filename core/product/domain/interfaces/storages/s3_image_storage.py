from typing import Any, Protocol, BinaryIO


class S3ImageStorageProtocol(Protocol):
    async def upload(self, staging_path: BinaryIO, file_name: str) -> str:
        """Upload image"""
        pass
