import enum
from datetime import datetime
from types import GenericAlias
from typing import Any
from uuid import UUID

import aiohttp  # type: ignore
from loguru import logger
from pydantic import BaseModel, parse_obj_as
from sqlmodel import SQLModel

from app.core.config import ExecutionMode, settings
from app.services.utils.token_refresher import refresh_shared_secret



async def make_request(method: HTTPMethods, url: str, request_data: Any, unauthorized_counter: int = 0) -> Any:
    request_args = {
        'headers': {
            'Authorization': f'bearer {settings.CUSTOMER_ACCESS_TOKEN}',
            'Content-type': 'text/plain',
        },
    }

    if method in [HTTPMethods.GET, HTTPMethods.DELETE]:
        if isinstance(request_data, str):
            url = url + request_data
        elif request_data:
            request_args['params'] = {key: value for key, value in request_data.items() if value is not None}
    elif method is HTTPMethods.POST:
        if isinstance(request_data, dict) and isinstance(list(request_data.values())[0], list):
            request_args['json'] = list(request_data.values())[0]
        else:
            request_args['json'] = request_data
        request_args['headers']['Content-type'] = 'application/json'
    else:
        request_args['json'] = request_data
        request_args['headers']['Content-type'] = 'application/json'

    try:
        async with aiohttp.request(
            method=method.value,  # noqa
            url=url,
            **request_args,
        ) as response:
            logger.info(f'Request was send [{method.value}] {url}. Status: {response.status}')
            if response.status == 404:
                return None
            elif response.status == 401:
                refresh_shared_secret()
                if unauthorized_counter == 2:
                    return None

                return await make_request(method, url, request_data, unauthorized_counter + 1)
            return await response.json()
    except Exception as e:
        logger.error(e)


def get_request_value(kwarg_key: str, kwarg_value: Any) -> Any:
    if isinstance(kwarg_value, (SQLModel, BaseModel)):
        return convert_values(kwarg_value.dict(exclude_unset=True, exclude_none=True))

    elif isinstance(kwarg_value, dict):
        return kwarg_value

    elif isinstance(kwarg_value, list) and kwarg_value and isinstance(kwarg_value[0], (SQLModel, BaseModel)):
        return {kwarg_key: [convert_values(value.dict(exclude_unset=True, exclude_none=True)) for value in kwarg_value]}

    elif isinstance(kwarg_value, list):
        return {kwarg_key: kwarg_value}

    return str(kwarg_value)


def convert_value(value: Any) -> Any:
    if isinstance(value, enum.Enum):
        return value.value
    elif isinstance(value, datetime):
        return value.isoformat()[:-3]
    elif isinstance(value, (SQLModel, BaseModel)):
        return convert_values(value.dict(exclude_unset=True, exclude_none=True))
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, dict):
        return convert_values(value)
    elif isinstance(value, UUID):
        return str(value)
    elif isinstance(value, list):
        return [convert_value(v) for v in value]
    return value


def convert_values(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {key: convert_value(value) for key, value in kwargs.items()}


def prepare_request(kwargs: dict[str, Any]) -> Any:
    kwargs.pop('db', None)
    kwargs.pop('session', None)

    if len(kwargs) == 0:
        pass
    elif len(kwargs) == 1:
        kwargs = get_request_value(*kwargs.popitem())
    return convert_values(kwargs) if isinstance(kwargs, dict) else kwargs


async def send_request(  # type: ignore
    method: HTTPMethods, url: str, response_model: Any | None = None, **kwargs
) -> Any:
    request_data = prepare_request(kwargs)
    result = await make_request(method, url, request_data)

    if isinstance(response_model, GenericAlias):
        if not result:
            return []
    elif isinstance(result, str):
        return result
    elif isinstance(response_model, SQLModel):
        if not result or not result.get('details'):
            return None
    else:
        if not result:
            return None
    if response_model:
        return parse_obj_as(response_model, result)

    return result
