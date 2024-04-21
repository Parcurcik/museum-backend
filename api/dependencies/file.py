from typing import Any, Callable

import numpy as np
from fastapi import File, UploadFile

from api.exceptions import IncorrectFileSizeError, IncorrectFileTypeError, IncorrectImageSizeError
from api.utils.common import bytes2image
from api.utils.types import TupleStr


async def check_file_size(file: UploadFile, max_file_size: float) -> bytes:
    bytes_ = await file.read()
    await file.seek(0)
    file_size = len(bytes_) / 1048576
    if file_size > max_file_size:
        raise IncorrectFileSizeError(file.filename, file_size, max_file_size)
    return bytes_


def get_file_with(
        name: str,
        *args: Any,
        content_types: str | TupleStr | None = None,
        **kwargs: Any,
) -> Callable[[UploadFile], UploadFile]:
    kwargs['alias'] = kwargs.get('alias', name)
    if isinstance(content_types, str):
        content_types = (content_types,)

    def get_file(file: UploadFile | None = File(*args, **kwargs)) -> UploadFile | None:
        if file is None:
            return file
        if content_types is not None and file.content_type not in content_types:
            raise IncorrectFileTypeError(file.filename, file.content_type, content_types)
        return file

    return get_file


def _check_image_size(
        image_name: str,
        image: np.array,
        min_width: int | None = None,
        min_height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        min_aspect_ratio: float | None = None,
        max_aspect_ratio: float | None = None,
) -> None:
    error = IncorrectImageSizeError(
        image_name,
        image.shape[:2][::-1],
        min_width,
        min_height,
        max_width,
        max_height,
        min_aspect_ratio,
        max_aspect_ratio,
    )
    if min_width is not None and image.shape[1] < min_width or image.shape[1] == 0:
        raise error
    if min_height is not None and image.shape[0] < min_height or image.shape[0] == 0:
        raise error
    if max_width is not None and image.shape[1] > max_width:
        raise error
    if max_height is not None and image.shape[0] > max_height:
        raise error
    aspect_ratio = image.shape[0] / image.shape[1]
    if min_aspect_ratio is not None and aspect_ratio < min_aspect_ratio:
        raise error
    if max_aspect_ratio is not None and aspect_ratio > max_aspect_ratio:
        raise error


def get_image_with(
        name: str,
        *args: Any,
        content_types: str | TupleStr | None = None,
        min_width: int | None = None,
        min_height: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        min_aspect_ratio: float | None = None,
        max_aspect_ratio: float | None = None,
        max_file_size: float | None = None,
        **kwargs: Any,
) -> Callable[[UploadFile], UploadFile]:
    kwargs['alias'] = kwargs.get('alias', name)
    if isinstance(content_types, str):
        content_types = (content_types,)

    async def get_image(file: UploadFile | None = File(*args, **kwargs)) -> UploadFile | None:
        if file is None:
            return file
        if (
                content_types is not None
                and file.content_type not in content_types
                or content_types is None
                and not file.content_type.startswith('image/')
        ):
            raise IncorrectFileTypeError(file.filename, file.content_type, content_types or ('image/*',))
        bytes_ = None
        if max_file_size is not None:
            bytes_ = await check_file_size(file, max_file_size)
        need_check_image = (
                min_width is not None
                or min_height is not None
                or max_width is not None
                or max_height is not None
                or min_aspect_ratio is not None
                or max_aspect_ratio is not None
        )
        if not need_check_image:
            return file
        if bytes_ is None:
            bytes_ = await file.read()
            await file.seek(0)
        image = bytes2image(bytes_)
        _check_image_size(
            file.filename, image, min_width, min_height, max_width, max_height, min_aspect_ratio, max_aspect_ratio
        )
        return file

    return get_image
