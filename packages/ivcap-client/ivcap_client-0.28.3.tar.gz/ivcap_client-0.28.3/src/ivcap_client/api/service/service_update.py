from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.service_description_t import ServiceDescriptionT
from ...models.service_status_rt import ServiceStatusRT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    json_body: ServiceDescriptionT,
    force_create: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["force-create"] = force_create

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/1/services/{id}".format(
            id=id,
        ),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ServiceStatusRT.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterValue.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
    force_create: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """update service

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Voluptatem sit..
        force_create (Union[Unset, None, bool]): Create if not already exist Example: True.
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
        force_create=force_create,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
    force_create: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """update service

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Voluptatem sit..
        force_create (Union[Unset, None, bool]): Create if not already exist Example: True.
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        force_create=force_create,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
    force_create: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """update service

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Voluptatem sit..
        force_create (Union[Unset, None, bool]): Create if not already exist Example: True.
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
        force_create=force_create,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
    force_create: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """update service

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Voluptatem sit..
        force_create (Union[Unset, None, bool]): Create if not already exist Example: True.
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
            force_create=force_create,
        )
    ).parsed
