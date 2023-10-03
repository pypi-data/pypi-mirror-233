import enum
from datetime import datetime
from types import GenericAlias
from typing import Any, Dict
from uuid import UUID

import aiohttp  # type: ignore
from loguru import logger
from pydantic import BaseModel, parse_obj_as
from sqlmodel import SQLModel
from ariksa_policy_cli.app.core.settings import settings
import requests
from ariksa_policy_cli.app.schemas.resource import HTTPMethods
import os
import jwt

class SendRequest():
    def __init__(self, shared_secret: str):
        self.tenant, self.stack, self.secret = shared_secret.split("::")
        self.org_id: str = ''
        self.refresh_shared_secret()


    def refresh_shared_secret(self) -> float | int | None:  # type: ignore
        # tenant, stack, secret = self.shared_secret.split("::")  # type: ignore[union-attr]
        url = f'https://{self.stack}.{settings.SERVER_DOMAIN}/sso/realms/{self.tenant}/protocol/openid-connect/token'
        data = {'client_id': 'offline', 'client_secret': self.secret, 'grant_type': 'client_credentials'}
        try:
            token_response = requests.post(
                url=url,
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
            ).json()
            self.access_token = token_response.get('access_token')
            return token_response.get('expires_in') * 2 / 3  # type: ignore[no-any-return]
        except Exception as e:
            logger.error(e)

    async def make_request(self, method: HTTPMethods, url: str, request_data: Any, unauthorized_counter: int = 0) -> Any:
        request_args = {
            'headers': {
                'Authorization': f'bearer {self.access_token}',
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
                    self.refresh_shared_secret()
                    if unauthorized_counter == 2:
                        return None

                    return await self.make_request(method, url, request_data, unauthorized_counter + 1)
                return await response.json()
        except Exception as e:
            logger.error(e)


    def get_request_value(self, kwarg_key: str, kwarg_value: Any) -> Any:
        if isinstance(kwarg_value, (SQLModel, BaseModel)):
            return self.convert_values(kwarg_value.dict(exclude_unset=True, exclude_none=True))

        elif isinstance(kwarg_value, dict):
            return kwarg_value

        elif isinstance(kwarg_value, list) and kwarg_value and isinstance(kwarg_value[0], (SQLModel, BaseModel)):
            return {kwarg_key: [self.convert_values(value.dict(exclude_unset=True, exclude_none=True)) for value in kwarg_value]}

        elif isinstance(kwarg_value, list):
            return {kwarg_key: kwarg_value}

        return str(kwarg_value)


    def convert_value(self, value: Any) -> Any:
        if isinstance(value, enum.Enum):
            return value.value
        elif isinstance(value, datetime):
            return value.isoformat()[:-3]
        elif isinstance(value, (SQLModel, BaseModel)):
            return self.convert_values(value.dict(exclude_unset=True, exclude_none=True))
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, dict):
            return self.convert_values(value)
        elif isinstance(value, UUID):
            return str(value)
        elif isinstance(value, list):
            return [self.convert_value(v) for v in value]
        return value


    def convert_values(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        return {key: self.convert_value(value) for key, value in kwargs.items()}


    def prepare_request(self, kwargs: dict[str, Any]) -> Any:
        kwargs.pop('db', None)
        kwargs.pop('session', None)

        if len(kwargs) == 0:
            pass
        elif len(kwargs) == 1:
            kwargs = self.get_request_value(*kwargs.popitem())
        return self.convert_values(kwargs) if isinstance(kwargs, dict) else kwargs
    
    def get_url(self, resource: str):
        return f'https://{self.stack}.{settings.SERVER_DOMAIN}/{settings.API_V1_STR}/{resource}'

    async def send_request(  # type: ignore
        self, method: HTTPMethods, resource: str, response_model: Any | None = None, **kwargs
    ) -> Any:
        url = self.get_url(resource=resource)
        request_data = self.prepare_request(kwargs)
        result = await self.make_request(method, url, request_data)

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