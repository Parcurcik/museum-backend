import json
from datetime import datetime, timedelta
from inspect import iscoroutinefunction
from typing import Any, AsyncGenerator, Awaitable, Callable, Iterable, List, Set, Tuple, TypeVar

import cv2
import numpy as np

from fastapi import Request
from starlette.responses import StreamingResponse

from .types import DictStrAny, TupleAny, TupleStr

_T = TypeVar('_T')
_IterableT = Iterable[_T]
_ListT = List[_T]
_SetT = Set[_T]


def format_datetime_with_timezone(value: datetime) -> str:
    ekt_time = value + timedelta(hours=5)
    return ekt_time.strftime("%Y-%m-%d %H:%M:%S")


def format_datetime(value: datetime) -> str:
    return value.strftime("%d.%m.%Y %H:%M")


def all_in(params: _IterableT, data: _IterableT) -> bool:
    return all(p in data for p in params)


def any_in(params: _IterableT, data: _IterableT) -> bool:
    return any(p in data for p in params)


def bytes2image(bytes_: bytes, is_color: bool = True) -> np.array:
    return cv2.imdecode(np.frombuffer(bytes_, np.uint8), cv2.IMREAD_UNCHANGED if is_color else cv2.IMREAD_GRAYSCALE)


def now() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)


async def call_function(func_: Callable, *args: Any, **kwargs: Any) -> Any:
    # we don't use coroutine decorator, so we use iscoroutinefunction from inspect package, not from asyncio package
    if iscoroutinefunction(func_):
        return await func_(*args, **kwargs)
    return func_(*args, **kwargs)


def get_difference(old_data: _IterableT, new_data: _IterableT) -> Tuple[_SetT, _SetT, _SetT]:
    old_data_set = set(old_data)
    new_data_set = set(new_data)
    to_add_data = new_data_set.difference(old_data_set)
    to_update_data = old_data_set.intersection(new_data_set)
    to_delete_data = old_data_set.difference(new_data_set)
    return to_add_data, to_update_data, to_delete_data


def get_values_from_dict(data: DictStrAny, keys: TupleStr) -> TupleAny:
    return tuple(data[key] for key in keys)


def split_seq_into_two_lists(values: _IterableT, good_values: _IterableT) -> Tuple[_ListT, _ListT]:
    good_values = set(good_values)
    good, bad = [], []
    for value in values:
        if value in good_values:
            good.append(value)
        else:
            bad.append(value)
    return good, bad


async def log_request_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]
) -> StreamingResponse:
    response = await call_next(request)
    url = request.url.path + (f'?{request.url.query}' if len(request.url.query) > 0 else '')
    log_message = f'\ttime: {now()}\n\tmethod: {request.method} {url}\n'
    state = request.state

    if not hasattr(state, 'request_body') or state.request_body is None:
        log_message += '\tbody: null\n'
    else:
        log_message += f'\tbody: {state.request_body}\n'
    if response.status_code < 400:
        log_message += f'\tstatus: success {response.status_code}'
        print(log_message)
        return response
    else:
        response_body = []
        async for chunk in response.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(response.charset)
            response_body.append(chunk)
        response_json = json.loads(b''.join(response_body))
        log_message += f'\tstatus: failed {response.status_code}\n\tresponse: {response_json}'
        print(log_message)

        async def body_stream() -> AsyncGenerator[bytes, None]:
            for chunk_stream in response_body:
                yield chunk_stream

        return StreamingResponse(status_code=response.status_code, content=body_stream(), media_type='application/json')
