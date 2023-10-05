from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.metrics.models import (
    MetricEvaluationRequest,
    MetricEvaluationResponse,
    MetricRequest,
    MetricResponse,
    MetricTypeEnum,
    PaginatedModelMetricsResponse,
)


PATH_PREFIX = "/api"


class ArthurMetricsClient:
    """
    A Python client to interact with the Arthur Metrics API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurMetricsClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_paginated_metrics_deprecated(
        self,
        model_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        expand: Optional[List[Any]] = None,
        default: Optional[bool] = None,
        type: Optional[List[MetricTypeEnum]] = None,
        sort: Optional[str] = None,
    ) -> PaginatedModelMetricsResponse:
        """
        Fetches the stored metrics associated with this model

        This may include default Arthur metrics as well as custom metrics associated with the model.

        :param model_id:
        :param page:
        :param page_size:
        :param expand:
        :param default:
        :param type:
        :param sort: Must be supplied in the format [column_name] to denote asc sort by this column OR -[column_name] to denote desc sort by this column
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if expand is not None:
            params["expand"] = expand
        if default is not None:
            params["default"] = default
        if type is not None:
            params["type"] = type
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/metrics",
            params=params,
            validation_response_code=200,
        )
        return PaginatedModelMetricsResponse(**parsed_resp)

    def create_metric_for_model_deprecated(
        self, model_id: str, json_body: MetricRequest
    ) -> MetricResponse:
        """
        Creates a new custom metric for the model

        :param model_id:
        :param json_body: A Metric containing a template query and parameter definitions
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/metrics",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return MetricResponse(**parsed_resp)

    def get_metric_for_model_by_id_deprecated(
        self, model_id: str, metric_id: str
    ) -> MetricResponse:
        """
        Fetches a metric by id

        :param model_id:
        :param metric_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/metrics/{metric_id}", validation_response_code=200
        )
        return MetricResponse(**parsed_resp)

    def update_metric_for_model_deprecated(
        self, model_id: str, metric_id: str, json_body: MetricRequest
    ) -> MetricResponse:
        """
        Updates a metric

        :param model_id:
        :param metric_id:
        :param json_body: A Metric containing a template query and parameter definitions
        """

        parsed_resp: Dict[str, Any] = self.http_client.put(  # type: ignore
            f"/v3/models/{model_id}/metrics/{metric_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return MetricResponse(**parsed_resp)

    def delete_metric_for_model_deprecated(
        self, model_id: str, metric_id: str
    ) -> Response:
        """
        Deletes a metric

        Note that if any alerts are associated with this metric then they will automatically be disabled.

        :param model_id:
        :param metric_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/models/{model_id}/metrics/{metric_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def evaluate_metric_for_model_deprecated(
        self, model_id: str, metric_id: str, json_body: MetricEvaluationRequest
    ) -> MetricEvaluationResponse:
        """
        Evaluate the metric on the provided parameters, filters, and groups

        :param model_id:
        :param metric_id:
        :param json_body: The arguments to use when evaluating a metric
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/metrics/{metric_id}/result",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return MetricEvaluationResponse(**parsed_resp)

    def get_paginated_metrics(
        self,
        model_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        expand: Optional[List[Any]] = None,
        default: Optional[bool] = None,
        type: Optional[List[MetricTypeEnum]] = None,
        sort: Optional[str] = None,
    ) -> PaginatedModelMetricsResponse:
        """
        Fetches the stored metrics associated with this model

        This may include default Arthur metrics as well as custom metrics associated with the model.

        :param model_id:
        :param page:
        :param page_size:
        :param expand:
        :param default:
        :param type:
        :param sort: Must be supplied in the format [column_name] to denote asc sort by this column OR -[column_name] to denote desc sort by this column
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if expand is not None:
            params["expand"] = expand
        if default is not None:
            params["default"] = default
        if type is not None:
            params["type"] = type
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v4/models/{model_id}/metrics",
            params=params,
            validation_response_code=200,
        )
        return PaginatedModelMetricsResponse(**parsed_resp)

    def create_metric_for_model(
        self, model_id: str, json_body: MetricRequest
    ) -> MetricResponse:
        """
        Creates a new custom metric for the model

        :param model_id:
        :param json_body: A Metric containing a template query and parameter definitions
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v4/models/{model_id}/metrics",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return MetricResponse(**parsed_resp)

    def get_metric_for_model_by_id(
        self, model_id: str, metric_id: str
    ) -> MetricResponse:
        """
        Fetches a metric by id

        :param model_id:
        :param metric_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v4/models/{model_id}/metrics/{metric_id}", validation_response_code=200
        )
        return MetricResponse(**parsed_resp)

    def update_metric_for_model(
        self, model_id: str, metric_id: str, json_body: MetricRequest
    ) -> MetricResponse:
        """
        Updates a metric

        :param model_id:
        :param metric_id:
        :param json_body: A Metric containing a template query and parameter definitions
        """

        parsed_resp: Dict[str, Any] = self.http_client.put(  # type: ignore
            f"/v4/models/{model_id}/metrics/{metric_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return MetricResponse(**parsed_resp)

    def delete_metric_for_model(self, model_id: str, metric_id: str) -> Response:
        """
        Deletes a metric

        Note that if any alerts are associated with this metric then they will automatically be disabled.

        :param model_id:
        :param metric_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v4/models/{model_id}/metrics/{metric_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def evaluate_metric_for_model(
        self, model_id: str, metric_id: str, json_body: MetricEvaluationRequest
    ) -> MetricEvaluationResponse:
        """
        Evaluate the metric on the provided parameters, filters, and groups

        :param model_id:
        :param metric_id:
        :param json_body: The arguments to use when evaluating a metric
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v4/models/{model_id}/metrics/{metric_id}/result",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return MetricEvaluationResponse(**parsed_resp)
