from typing import BinaryIO
import aioboto3
from botocore.exceptions import ClientError
from uuid import uuid4
from urllib.parse import urljoin
import json


class S3ImageStorage:
    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        access_key: str,
        secret_key: str
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = aioboto3.Session()
        
    async def ensure_bucket(self):
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        ) as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket_name)
            except ClientError:
                await s3.create_bucket(Bucket=self.bucket_name)
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "AllowPublicRead",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                        }
                    ]
                }
                await s3.put_bucket_policy(
                    Bucket=self.bucket_name, 
                    Policy=json.dumps(policy)
                )

    async def upload(self, image_file: BinaryIO, file_name: str) -> str:
        s3_key = f"{uuid4()}_{file_name}"
        
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        ) as s3:
            await s3.upload_fileobj(
                Fileobj=image_file,
                Bucket=self.bucket_name,
                Key=s3_key,
                ExtraArgs={
                    "ContentType": "image/png",
                    "ACL": "public-read"
                }
            )
            url = urljoin(f"{self.endpoint_url}/", f"{self.bucket_name}/{s3_key}")
            return url

    async def delete(self, url: str) -> None:
        base_url = f"{self.endpoint_url.rstrip('/')}/{self.bucket_name}/"
        s3_key = url.replace(base_url, "", 1)
            
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        ) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
