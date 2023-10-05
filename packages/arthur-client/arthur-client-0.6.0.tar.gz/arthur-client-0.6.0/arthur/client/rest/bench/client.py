from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.bench.models import (
    CreateRunRequest,
    CreateRunResponse,
    HallucinationCheckRequest,
    HallucinationCheckResponse,
    PaginatedGetRunResponse,
    PaginatedGetRunsForTestSuiteResponse,
    PaginatedGetTestSuiteResponse,
    PaginatedGetTestSuitesResponse,
    TestSuiteRequest,
    TestSuiteResponse,
    TestSuiteSummaryResponse,
)


PATH_PREFIX = "/api"


class ArthurBenchClient:
    """
    A Python client to interact with the Arthur Bench API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurBenchClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_test_suites(
        self,
        name: Optional[str] = None,
        sort: Optional[str] = None,
        scoring_method: Optional[str] = None,
    ) -> PaginatedGetTestSuitesResponse:
        """
                Gets test suites

                Sort by latest run by default.
        If `name` query parameter is provided, filter on test suite name.

                :param name:
                :param sort:
                :param scoring_method:
        """

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if sort is not None:
            params["sort"] = sort
        if scoring_method is not None:
            params["scoring_method"] = scoring_method

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/bench/test_suites", params=params, validation_response_code=200
        )
        return PaginatedGetTestSuitesResponse(**parsed_resp)

    def create_test_suite(self, json_body: TestSuiteRequest) -> TestSuiteResponse:
        """
        Creates a new test suite from reference data using specified scoring_method for scoring

        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/bench/test_suites",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return TestSuiteResponse(**parsed_resp)

    def get_test_suite(self, test_suite_id: str) -> PaginatedGetTestSuiteResponse:
        """
        Get reference data for an existing test suite

        :param test_suite_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}", validation_response_code=200
        )
        return PaginatedGetTestSuiteResponse(**parsed_resp)

    def delete_test_suite(self, test_suite_id: str) -> Response:
        """
        Deletes test suite

        Is idempotent.

        :param test_suite_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def get_summary_statistics(
        self,
        test_suite_id: str,
        run_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> TestSuiteSummaryResponse:
        """
        Get pagianted summary statistics of a test suite

        Defaults to page size of 5.

        :param test_suite_id:
        :param run_id:
        :param page:
        :param page_size:
        """

        params: Dict[str, Any] = {}
        if run_id is not None:
            params["run_id"] = run_id
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}/runs/summary",
            params=params,
            validation_response_code=200,
        )
        return TestSuiteSummaryResponse(**parsed_resp)

    def get_runs_for_test_suite(
        self, test_suite_id: str, sort: Optional[str] = None
    ) -> PaginatedGetRunsForTestSuiteResponse:
        """
        Get runs for a particular test suite (identified by test_suite_id)

        :param test_suite_id:
        :param sort:
        """

        params: Dict[str, Any] = {}
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}/runs",
            params=params,
            validation_response_code=200,
        )
        return PaginatedGetRunsForTestSuiteResponse(**parsed_resp)

    def create_new_test_run(
        self, test_suite_id: str, json_body: CreateRunRequest
    ) -> CreateRunResponse:
        """
        Creates a new test run with model version / associated metadata


        :param test_suite_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}/runs",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return CreateRunResponse(**parsed_resp)

    def get_test_run(
        self,
        test_suite_id: str,
        test_run_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[bool] = None,
    ) -> PaginatedGetRunResponse:
        """
        Get a test run with input, output, and reference data

        :param test_suite_id:
        :param test_run_id:
        :param page:
        :param page_size:
        :param sort:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}/runs/{test_run_id}",
            params=params,
            validation_response_code=200,
        )
        return PaginatedGetRunResponse(**parsed_resp)

    def delete_a_test_run(self, test_suite_id: str, test_run_id: str) -> Response:
        """
        Deletes a test run

        Is idempotent.

        :param test_suite_id:
        :param test_run_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/bench/test_suites/{test_suite_id}/runs/{test_run_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def score_a_response_for_hallucination_given_a_context(
        self, json_body: HallucinationCheckRequest
    ) -> HallucinationCheckResponse:
        """
        Score a response for hallucination given a context

        Return True if the response contains a hallucination and False otherwise

        :param json_body: Model generated response and context used to determine whether the response is a hallucination
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/bench/scoring/hallucination",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return HallucinationCheckResponse(**parsed_resp)
