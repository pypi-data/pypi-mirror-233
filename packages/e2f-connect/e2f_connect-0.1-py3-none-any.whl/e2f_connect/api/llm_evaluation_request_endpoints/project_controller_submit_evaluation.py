from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.evaluation_request_dto import EvaluationRequestDto
from ...types import Response


def _get_kwargs(
    *,
    multipart_data: EvaluationRequestDto,
) -> Dict[str, Any]:
    pass

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": "/api/v1/project",
        "files": multipart_multipart_data,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.CREATED:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return None
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: EvaluationRequestDto,
) -> Response[Any]:
    """Submit Evaluation Request

     Submit an evaluation request with the following body:
            <ul>
            <li><strong>Dataset</strong>: Location of the dataset in one of the following formats: GCP
    link or S3 bucket location.</li>
            <li><strong>Project name</strong>: Project name to use for reference.</li>
            <li><strong>Metrics</strong>: Metrics can be selected from the list of the provided well-
    known metrics or submitted by the user. Description is required for every new user-submitted
    metric.</li>
            <li><strong>Domain (optional)</strong>: Can be optionally specified if the dataset requires
    specific domain expertise. You can choose the domain  from the provided list (see get domains
    endpoint) or enter your custom domain.</li>
            <li><strong>Due Date</strong>: Due date of the evaluation.</li>
            <li><strong>Language</strong>: Language of the dataset.</li>
            <li><strong>Requester Name</strong>.</li>
            <li><strong>Requester Email</strong>.</li>
            </ul>
            All fields are required unless stated otherwise.

    Args:
        multipart_data (EvaluationRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: EvaluationRequestDto,
) -> Response[Any]:
    """Submit Evaluation Request

     Submit an evaluation request with the following body:
            <ul>
            <li><strong>Dataset</strong>: Location of the dataset in one of the following formats: GCP
    link or S3 bucket location.</li>
            <li><strong>Project name</strong>: Project name to use for reference.</li>
            <li><strong>Metrics</strong>: Metrics can be selected from the list of the provided well-
    known metrics or submitted by the user. Description is required for every new user-submitted
    metric.</li>
            <li><strong>Domain (optional)</strong>: Can be optionally specified if the dataset requires
    specific domain expertise. You can choose the domain  from the provided list (see get domains
    endpoint) or enter your custom domain.</li>
            <li><strong>Due Date</strong>: Due date of the evaluation.</li>
            <li><strong>Language</strong>: Language of the dataset.</li>
            <li><strong>Requester Name</strong>.</li>
            <li><strong>Requester Email</strong>.</li>
            </ul>
            All fields are required unless stated otherwise.

    Args:
        multipart_data (EvaluationRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        multipart_data=multipart_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
