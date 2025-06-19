from typing import BinaryIO
from urllib.parse import urljoin
from uuid import uuid4
import json
import aioboto3
from botocore.exceptions import ClientError


class S3ImageStorage:
    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        acccess_key: str,
        secret_key: str
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.access_key = acccess_key
        self.secret_key = secret_key
        
    async def ensure_bucket(self):
        session = aioboto3.Session()
        
        async with session.client(
            service_name="s3",
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
                        "Resource": "arn:aws:s3:::product-bucket-images/*"
                        }
                    ]
                }
                await s3.put_bucket_policy(Bucket=self.bucket_name, Policy=json.dumps(policy))
            
        
    async def upload(self, image_file: BinaryIO, file_name: str) -> str:
        s3_key = f"{uuid4()}_{file_name}"
        session = aioboto3.Session()
        
        async with session.client(
            service_name="s3",
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
