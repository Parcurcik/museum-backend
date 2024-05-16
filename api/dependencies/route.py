from fastapi import Request
from starlette.datastructures import UploadFile


async def memorize_request_body(request: Request) -> None:
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        request.state.request_body = None
    else:
        match content_type.split(';', 1)[0]:
            case 'application/json':
                try:
                    request_body = await request.json()
                except Exception as e:
                    print(f"Error while trying to log users request {e}")
                    request_body = None
            case 'multipart/form-data':
                request_body = dict(await request.form())
                for key, value in request_body.items():
                    if isinstance(value, UploadFile):
                        request_body[key] = 'file'
            case 'application/x-www-form-urlencoded':
                request_body = dict(await request.form())
            case _:
                request_body = None
        request.state.request_body = request_body
