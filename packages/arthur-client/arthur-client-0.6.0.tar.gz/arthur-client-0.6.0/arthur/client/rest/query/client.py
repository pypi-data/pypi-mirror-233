from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.query.models import (
    DataDriftResponse,
    DataDriftTableRequest,
    DataDriftTableResponse,
    DistributionsRequest,
    QueryResult,
)
from arthur.client.rest.common.models import DataDriftRequest, QueryRequest


PATH_PREFIX = "/api"


class ArthurQueryClient:
    """
    A Python client to interact with the Arthur Query API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurQueryClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def query(
        self,
        model_id: str,
        json_body: QueryRequest,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> QueryResult:
        """
        This endpoint takes a query request in the body and returns inferences and metrics for the model's inferences

        Please see the \"Query Guide\" linked above for more information.

        :param model_id:
        :param json_body:
        :param page:
        :param page_size:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/query",
            json=json_body.dict(by_alias=True, exclude_none=True),
            params=params,
            validation_response_code=200,
        )
        return QueryResult(**parsed_resp)

    def query_data_drift(
        self, model_id: str, json_body: DataDriftRequest
    ) -> DataDriftResponse:
        """
        This endpoint takes a data drift query request and returns data drift values

        For example queries, see the \"Query Guide\" under the API section.

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/query/data_drift",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return DataDriftResponse(**parsed_resp)

    def query_psi_bucket_table(
        self, model_id: str, json_body: DataDriftTableRequest
    ) -> DataDriftTableResponse:
        """
        This endpoint takes a data drift table query request and returns raw psi bucket values

        For example queries, see the \"Query Guide\" under the API section.

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/query/data_drift_psi_bucket_calculation_table",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return DataDriftTableResponse(**parsed_resp)

    def query_distributions(
        self, model_id: str, json_body: DistributionsRequest
    ) -> QueryResult:
        """
        This endpoint takes in attributes that should correspond to x and y values and optional additional values and filters and returns scatterplot data

        It buckets the x attribute, then buckets the y attribute and returns the values specified in the request that fall within each bucket.

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/query/distributions",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return QueryResult(**parsed_resp)
