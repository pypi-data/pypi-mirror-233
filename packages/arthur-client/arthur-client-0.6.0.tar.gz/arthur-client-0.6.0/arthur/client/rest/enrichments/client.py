from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.enrichments.models import (
    AnomalyDetectionEnrichmentConfiguration,
    AnomalyDetectionEnrichmentResponse,
    BiasConstraintEnum,
    BiasMitigationEnrichmentConfiguration,
    BiasMitigationEnrichmentResponse,
    EnrichmentsRequest,
    EnrichmentsResponse,
    ExplainabilityEnrichmentMultipartRequestBody,
    ExplainabilityEnrichmentRequest,
    ExplainabilityEnrichmentResponse,
    ExplainabilityResultOnDemand,
    ExplainabilityResultWhatIf,
    FindHotspotsResponse,
    HotspotsEnrichmentConfiguration,
    HotspotsEnrichmentResponse,
    PaginatedBiasMitigationCurves,
    WhatIfRequest,
)


PATH_PREFIX = "/api"


class ArthurEnrichmentsClient:
    """
    A Python client to interact with the Arthur Enrichments API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurEnrichmentsClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_bias_mitigation_curves(
        self,
        model_id: str,
        attribute_id: Optional[str] = None,
        constraint: Optional[List[BiasConstraintEnum]] = None,
        attribute_value: Optional[List[str]] = None,
        continuous_value: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PaginatedBiasMitigationCurves:
        """
        Retrieve Bias Mitigation curves for a specified model and query parameters

        :param model_id:
        :param attribute_id:
        :param constraint:
        :param attribute_value:
        :param continuous_value:
        :param page:
        :param page_size:
        """

        params: Dict[str, Any] = {}
        if attribute_id is not None:
            params["attribute_id"] = attribute_id
        if constraint is not None:
            params["constraint"] = constraint
        if attribute_value is not None:
            params["attribute_value"] = attribute_value
        if continuous_value is not None:
            params["continuous_value"] = continuous_value
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/bias_mitigation/curves",
            params=params,
            validation_response_code=200,
        )
        return PaginatedBiasMitigationCurves(**parsed_resp)

    def get_enrichment_configuration(self, model_id: str) -> EnrichmentsResponse:
        """
        Gets the enrichment configurations for a model

        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments", validation_response_code=200
        )
        return EnrichmentsResponse(**parsed_resp)

    def update_enrichment_config(
        self,
        model_id: str,
        json_body: EnrichmentsRequest,
        multipart_data: ExplainabilityEnrichmentMultipartRequestBody,
    ) -> Response:
        """
        Updates the enrichment configuration for a model

        :param model_id:
        :param json_body: Configures multiple enrichments. A multipart/form-data body with at least a `configuration` JSON body. If explainability is being enabled for the first time, artifacts must be supplied.
        :param multipart_data: When setting up explainability, a config must always be provided. The explainability enrichment artifact files may be provided all together, but a config must be provided as well, regardless of whether the config has already been set.
        """

        raw_resp: Response = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/enrichments",
            json=json_body.dict(by_alias=True, exclude_none=True),
            files=multipart_data.dict(by_alias=True, exclude_none=True),
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def get_anomaly_detection_config(
        self, model_id: str
    ) -> AnomalyDetectionEnrichmentResponse:
        """


        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/anomaly_detection",
            validation_response_code=200,
        )
        return AnomalyDetectionEnrichmentResponse(**parsed_resp)

    def update_anomaly_detection_config(
        self, model_id: str, json_body: AnomalyDetectionEnrichmentConfiguration
    ) -> Response:
        """
        Enable or disable anomaly_detection for a model

        :param model_id:
        :param json_body:
        """

        raw_resp: Response = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/enrichments/anomaly_detection",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def get_bias_mitigation_config(
        self, model_id: str
    ) -> BiasMitigationEnrichmentResponse:
        """


        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/bias_mitigation",
            validation_response_code=200,
        )
        return BiasMitigationEnrichmentResponse(**parsed_resp)

    def update_bias_mitigation_config(
        self, model_id: str, json_body: BiasMitigationEnrichmentConfiguration
    ) -> Response:
        """
        Enable or disable bias_mitigation for a model

        :param model_id:
        :param json_body:
        """

        raw_resp: Response = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/enrichments/bias_mitigation",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def get_hotspots_config(self, model_id: str) -> HotspotsEnrichmentResponse:
        """
        Get hotspot enrichment config for a model

        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/hotspots", validation_response_code=200
        )
        return HotspotsEnrichmentResponse(**parsed_resp)

    def update_hotspots_config(
        self, model_id: str, json_body: HotspotsEnrichmentConfiguration
    ) -> Response:
        """
        Enable or disable hotspots for a model

        :param model_id:
        :param json_body:
        """

        raw_resp: Response = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/enrichments/hotspots",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def find_hotspots(
        self,
        model_id: str,
        metric: str,
        threshold: float,
        date: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> FindHotspotsResponse:
        """
        Find hotspots for a model using the given metric and threshold

        For batch models, supply batch_id, for streaming models, supply a date. Cannot supply both date and batch.

        :param model_id:
        :param metric:
        :param threshold:
        :param date:
        :param batch_id:
        """

        params: Dict[str, Any] = {"metric": metric, "threshold": threshold}
        if date is not None:
            params["date"] = date
        if batch_id is not None:
            params["batch_id"] = batch_id

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/hotspots/find",
            params=params,
            validation_response_code=200,
        )
        return FindHotspotsResponse(**parsed_resp)

    def get_explainability_config(
        self, model_id: str
    ) -> ExplainabilityEnrichmentResponse:
        """


        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/enrichments/explainability",
            validation_response_code=200,
        )
        return ExplainabilityEnrichmentResponse(**parsed_resp)

    def update_explainability_config(
        self,
        model_id: str,
        json_body: ExplainabilityEnrichmentRequest,
        multipart_data: ExplainabilityEnrichmentMultipartRequestBody,
    ) -> Response:
        """
        Configure explainability for a model

        :param model_id:
        :param json_body: Configures explainability. A multipart/form-data body with at least a `configuration` JSON body. If explainability is being enabled for the first time, artifacts must be supplied.
        :param multipart_data: When setting up explainability, a config must always be provided. The explainability enrichment artifact files may be provided all together, but a config must be provided as well, regardless of whether the config has already been set.
        """

        raw_resp: Response = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/enrichments/explainability",
            json=json_body.dict(by_alias=True, exclude_none=True),
            files=multipart_data.dict(by_alias=True, exclude_none=True),
            validation_response_code=202,
            return_raw_response=True,
        )
        return raw_resp

    def explain_inference(
        self,
        model_id: str,
        partner_inference_id: str,
        algorithm: Optional[str] = "lime",
        n_samples: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> ExplainabilityResultOnDemand:
        """
        Fetches an on-demand inference explanation

        Each time this endpoint is called a new explanation for the given inferences is generated.

        :param model_id:
        :param partner_inference_id:
        :param algorithm:
        :param n_samples:
        :param page:
        :param page_size:
        :param sort: Must be supplied in the format [column_name] to denote asc sort by this column OR -[column_name] to denote desc sort by this column
        """

        params: Dict[str, Any] = {}
        if algorithm is not None:
            params["algorithm"] = algorithm
        if n_samples is not None:
            params["n_samples"] = n_samples
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/inferences/{partner_inference_id}/explanation",
            params=params,
            validation_response_code=200,
        )
        return ExplainabilityResultOnDemand(**parsed_resp)

    def what_if(
        self, model_id: str, json_body: WhatIfRequest
    ) -> ExplainabilityResultWhatIf:
        """
        Retrieve the prediction and explanation for an inference

        Only valid for models with input type equal to Tabular.

        :param model_id:
        :param json_body: Inference model pipeline input to get explanation for
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/what_if",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return ExplainabilityResultWhatIf(**parsed_resp)
