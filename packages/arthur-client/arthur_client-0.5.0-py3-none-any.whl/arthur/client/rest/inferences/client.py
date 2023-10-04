from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.inferences.models import (
    BatchResponse,
    ClosedRequest,
    DatasetResponse,
    FileInferenceData,
    ImageInferenceEnum,
    InferencesResponse,
    NewInference,
    ParquetDataResponse,
    PartnerIdInferenceGroundTruth,
    QueryResult,
    ReferenceDataRequest,
    ReferenceDatasetResponse,
    SageMakerDataResponse,
    SageMakerInferenceData,
    SuccessResponse,
)


PATH_PREFIX = "/api"


class ArthurInferencesClient:
    """
    A Python client to interact with the Arthur Inferences API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurInferencesClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def send_inferences(
        self, model_id: str, json_body: List["NewInference"]
    ) -> InferencesResponse:
        """
        Saves new inferences

        :param model_id:
        :param json_body: New inferences to save
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences",
            json=[x.dict(by_alias=True, exclude_none=True) for x in json_body],
            validation_response_code=207,
        )
        return InferencesResponse(**parsed_resp)

    def update_inference_ground_truths(
        self, model_id: str, json_body: List["PartnerIdInferenceGroundTruth"]
    ) -> InferencesResponse:
        """
        Updates inferences with ground truth data

        :param model_id:
        :param json_body: List of inference ground truth data
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/inferences",
            json=[x.dict(by_alias=True, exclude_none=True) for x in json_body],
            validation_response_code=207,
        )
        return InferencesResponse(**parsed_resp)

    def send_inference_file(
        self, model_id: str, multipart_data: FileInferenceData
    ) -> ParquetDataResponse:
        """
        Uploads a parquet file containing inferences or a parquet file containing ground truth

        Either inference_data or ground_truth_data must be included in the request. After an initial validation, inferences are uploaded asynchronously. Failed inferences will result in an email alert. For image models, include images in the image_data field of the form. See the request body schema for more details.

        :param model_id:
        :param multipart_data: File containing inferences to bulk upload and optional batch_id OR file containing ground truth data. Either inferences.parquet or ground_truths.parquet must be included in the request.
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/file",
            files=multipart_data.dict(by_alias=True, exclude_none=True),
            validation_response_code=207,
        )
        return ParquetDataResponse(**parsed_resp)

    def send_sagemaker_data(
        self, model_id: str, multipart_data: SageMakerInferenceData
    ) -> SageMakerDataResponse:
        """
        Accepts a SageMaker Data Capture JSONL file containing inferences

        The form-data key \"inference_data\" must be included in the request and map to a SageMaker Data Capture file. After an initial validation, inferences are uploaded asynchronously. Failed inferences will result in an email alert. See the request body schema for more details.

        :param model_id:
        :param multipart_data: File containing SageMaker Data Capture JSONL to bulk upload.
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/inferences/integrations/sagemaker_data_capture",
            files=multipart_data.dict(by_alias=True, exclude_none=True),
            validation_response_code=207,
        )
        return SageMakerDataResponse(**parsed_resp)

    def get_inference(self, model_id: str, partner_inference_id: str) -> QueryResult:
        """
        Retrieve inference by partner inference id

        :param model_id:
        :param partner_inference_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/inferences/query/{partner_inference_id}",
            validation_response_code=200,
        )
        return QueryResult(**parsed_resp)

    def get_inference_image(
        self, model_id: str, image_id: str, type: ImageInferenceEnum
    ) -> Response:
        """
        Retrieve inference image files

        Type=raw_image will return the original uploaded image. Type=resized_image will return the image resized to your model's input size. Type=thumbnail will return a thumbnail sized version of the image. Type=lime_explanation will return a JSON file of lime region mapping and lime segment mask.

        :param model_id:
        :param image_id:
        :param type:
        """

        params: Dict[str, Any] = {"type": type.value}

        raw_resp: Response = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/inferences/images/{image_id}",
            params=params,
            validation_response_code=None,
            return_raw_response=True,
        )
        return raw_resp

    def get_datasets(self, model_id: str) -> List[DatasetResponse]:
        """
        get_datasets

        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/datasets", validation_response_code=200
        )
        return List[DatasetResponse](**parsed_resp)

    def get_batch_information(self, model_id: str, batch_id: str) -> BatchResponse:
        """
        Returns the batch information for a model

        :param model_id:
        :param batch_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/batches/{batch_id}", validation_response_code=200
        )
        return BatchResponse(**parsed_resp)

    def close_batch(
        self, model_id: str, batch_id: str, json_body: ClosedRequest
    ) -> SuccessResponse:
        """
        Closes a batch

        Closing transitions the dataset from \"started\" to \"uploaded\" and kicks off processing.

        :param model_id:
        :param batch_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/batches/{batch_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return SuccessResponse(**parsed_resp)

    def get_model_reference_data_info(self, model_id: str) -> ReferenceDatasetResponse:
        """
        Returns the reference data information for a model

        :param model_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/reference_data", validation_response_code=200
        )
        return ReferenceDatasetResponse(**parsed_resp)

    def update_model_reference_data(
        self, model_id: str, multipart_data: ReferenceDataRequest
    ) -> ParquetDataResponse:
        """
        Uploads a parquet file containing reference set data

        After an initial validation, rows are uploaded asynchronously. Failed rows will result in an email alert. For image models, include images in the image_data field of the form. See the request body schema for more details.

        :param model_id:
        :param multipart_data: Reference set data to upload.
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/reference_data",
            files=multipart_data.dict(by_alias=True, exclude_none=True),
            validation_response_code=207,
        )
        return ParquetDataResponse(**parsed_resp)

    def close_model_reference_data(
        self, model_id: str, json_body: ClosedRequest
    ) -> SuccessResponse:
        """
        Closes a reference dataset

        Closing transitions the dataset from \"started\" to \"uploaded\" and kicks off processing.

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/reference_data",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return SuccessResponse(**parsed_resp)
