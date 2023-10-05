from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.model_groups.models import (
    ModelGroupResponse,
    ModelGroupUpdateRequest,
    PaginatedModelGroupResponse,
    PaginatedModelGroupVersionsResponse,
)
from arthur.client.rest.models.models import ModelExpand, ModelObject


PATH_PREFIX = "/api"


class ArthurModelGroupsClient:
    """
    A Python client to interact with the Arthur Model Groups API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurModelGroupsClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_paginated_model_groups(
        self,
        include_archived: Optional[bool] = False,
        expand: Optional[ModelExpand] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> PaginatedModelGroupResponse:
        """
        Returns a paginated response of all the model groups within an organization

        :param include_archived:
        :param expand:
        :param page:
        :param page_size:
        :param sort: Must be supplied in the format [column_name] to denote asc sort by this column OR -[column_name] to denote desc sort by this column
        """

        params: Dict[str, Any] = {}
        if include_archived is not None:
            params["include_archived"] = include_archived
        if expand is not None:
            params["expand"] = expand.value
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/model_groups", params=params, validation_response_code=200
        )
        return PaginatedModelGroupResponse(**parsed_resp)

    def get_model_group_by_id(self, model_group_id: str) -> ModelGroupResponse:
        """
        Retrieve a specific model group object

        :param model_group_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/model_groups/{model_group_id}", validation_response_code=200
        )
        return ModelGroupResponse(**parsed_resp)

    def archive_model_group(self, model_group_id: str) -> Response:
        """
        Archives all the models within the model group asynchronously

        :param model_group_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/model_groups/{model_group_id}",
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def update_model_group(
        self, model_group_id: str, json_body: ModelGroupUpdateRequest
    ) -> ModelGroupResponse:
        """
        Updates an existing model group object

        :param model_group_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/model_groups/{model_group_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return ModelGroupResponse(**parsed_resp)

    def get_model_versions_of_model_group_by_id(
        self,
        model_group_id: str,
        expand: Optional[List[ModelExpand]] = None,
        sequence_num: Optional[float] = None,
    ) -> PaginatedModelGroupVersionsResponse:
        """
        Retrieve model versions of a specific model group object

        :param model_group_id:
        :param expand:
        :param sequence_num:
        """

        params: Dict[str, Any] = {}
        if expand is not None:
            params["expand"] = expand
        if sequence_num is not None:
            params["sequence_num"] = sequence_num

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/model_groups/{model_group_id}/versions",
            params=params,
            validation_response_code=200,
        )
        return PaginatedModelGroupVersionsResponse(**parsed_resp)

    def get_latest_model_version_of_model_group_by_id(
        self, model_group_id: str
    ) -> ModelObject:
        """
        Retrieve the latest model version of a specific model group object

        :param model_group_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/model_groups/{model_group_id}/versions/latest",
            validation_response_code=200,
        )
        return ModelObject(**parsed_resp)
