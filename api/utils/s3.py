from aioboto3 import Session
from fastapi import UploadFile

from api.configuration.config import settings


def create_s3_url_by_path(path: str) -> str:
    return '/'.join([settings.S3_URL, settings.S3_BUCKET, path])


async def upload_file_on_s3(path: str, file: UploadFile, public: bool = True) -> None:
    args = {'ContentType': file.content_type}
    if public:
        args['ACL'] = 'public-read'
    session = Session(aws_access_key_id=settings.S3_ACCESS_KEY, aws_secret_access_key=settings.S3_SECRET_KEY)
    async with session.client('s3', endpoint_url=settings.S3_URL) as s3:
        await s3.upload_fileobj(file, settings.S3_BUCKET, path, ExtraArgs=args)
