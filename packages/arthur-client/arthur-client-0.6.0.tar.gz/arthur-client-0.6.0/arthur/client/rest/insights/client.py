from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.insights.models import (
    Insight,
    InsightPatch,
    InsightUpdateResponse,
    ModelInsightCount,
    PaginatedInsightGroupCounts,
    PaginatedInsights,
)


PATH_PREFIX = "/api"


class ArthurInsightsClient:
    """
    A Python client to interact with the Arthur Insights API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurInsightsClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_all_insight_counts_by_model(
        self,
        status: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[ModelInsightCount]:
        """
        Retrieves insight counts by model id for all active models in the current organization

        If a model has no insights that fit the search criteria, the model_id will not be included in the response.

        :param status:
        :param start_time:
        :param end_time:
        """

        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/insights/model_counts", params=params, validation_response_code=200
        )
        return List[ModelInsightCount](**parsed_resp)

    def get_paginated_model_insights(
        self,
        model_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        status: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> PaginatedInsights:
        """
        Retrieve a paginated list of insights for the specific model

        :param model_id:
        :param page:
        :param page_size:
        :param sort:
        :param start_time:
        :param end_time:
        :param status:
        :param batch_id:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if status is not None:
            params["status"] = status
        if batch_id is not None:
            params["batch_id"] = batch_id

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/insights",
            params=params,
            validation_response_code=200,
        )
        return PaginatedInsights(**parsed_resp)

    def update_model_insights_status(
        self, model_id: str, json_body: InsightPatch
    ) -> InsightUpdateResponse:
        """
        Update the status of the insights for a specific model

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/insights",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return InsightUpdateResponse(**parsed_resp)

    def get_insight_group_counts(
        self,
        model_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> PaginatedInsightGroupCounts:
        """
        Retrieve a paginated list of insight groups for this model

        Each group contains a key (batch_id for batch models or window_start for streaming models), a group timestamp, and a count of the number of insights that belong to the group.

        :param model_id:
        :param page:
        :param page_size:
        :param sort:
        :param status:
        :param batch_id:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort
        if status is not None:
            params["status"] = status
        if batch_id is not None:
            params["batch_id"] = batch_id

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/insights/group_counts",
            params=params,
            validation_response_code=200,
        )
        return PaginatedInsightGroupCounts(**parsed_resp)

    def get_model_insight_by_id(self, model_id: str, insight_id: str) -> Insight:
        """
        Retrieve insight for the specific model and insight id

        :param model_id:
        :param insight_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/insights/{insight_id}", validation_response_code=200
        )
        return Insight(**parsed_resp)

    def update_insight_status(
        self, model_id: str, insight_id: str, json_body: InsightPatch
    ) -> InsightUpdateResponse:
        """
        Update the status of the insight for a specific model and insight id

        :param model_id:
        :param insight_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/insights/{insight_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return InsightUpdateResponse(**parsed_resp)
