from typing import Optional, Any, Union, Dict, List, Tuple
from http import HTTPStatus
from requests.cookies import RequestsCookieJar
from requests import Response

# import http client
from arthur.client.http.requests import HTTPClient

from arthur.client.rest.alerts.models import (
    AlertNotificationConfiguration,
    AlertNotificationConfigurationUpdate,
    AlertRequest,
    AlertResponse,
    AlertRulePatch,
    AlertRuleRequest,
    AlertRulesSort,
    AlertSummaryConfiguration,
    AlertSummaryConfigurationUpdate,
    AlertSummaryNotificationConfiguration,
    AlertSummaryNotificationConfigurationUpdate,
    BulkAlertUpdateResponse,
    EmailNotificationBody,
    NewAlertNotificationConfiguration,
    NewAlertSummaryConfiguration,
    NewAlertSummaryNotificationConfiguration,
    PaginatedAlertNotificationConfigurationsResponse,
    PaginatedAlertResponse,
    PaginatedAlertRuleResponse,
    PaginatedAlertSummaryConfigurationsResponse,
    PaginatedAlertSummaryNotificationConfigurationsResponse,
)


PATH_PREFIX = "/api"


class ArthurAlertsClient:
    """
    A Python client to interact with the Arthur Alerts API
    """

    def __init__(self, http_client: HTTPClient):
        """
        Create a new ArthurAlertsClient from an HTTPClient

        :param http_client: the :class:`~arthurai.client.http.requests.HTTPClient` to use for underlying requests
        """
        self.http_client = http_client
        self.http_client.set_path_prefix(PATH_PREFIX)

    def get_alert_counts(
        self,
        model_id: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        group_by_date: Optional[bool] = None,
        severity: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
    ) -> Response:
        """
        get alert counts, grouped by models, and optionally grouped by day

        :param model_id:
        :param start_time:
        :param end_time:
        :param group_by_date:
        :param severity:
        :param status:
        """

        params: Dict[str, Any] = {}
        if model_id is not None:
            params["model_id"] = model_id
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if group_by_date is not None:
            params["group_by_date"] = group_by_date
        if severity is not None:
            params["severity"] = severity
        if status is not None:
            params["status"] = status

        raw_resp: Response = self.http_client.get(  # type: ignore
            f"/v3/alerts/model_counts",
            params=params,
            validation_response_code=200,
            return_raw_response=True,
        )
        return raw_resp

    def get_paginated_alerts(
        self,
        model_id: Optional[List[str]] = None,
        metric: Optional[str] = None,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        batch_id: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        alert_rule_id: Optional[str] = None,
    ) -> PaginatedAlertResponse:
        """
        Returns paginated alerts

        For organization-scoped users this will return alerts within their organization. For global users, this will return alerts in all organizations.

        :param model_id:
        :param metric:
        :param status:
        :param severity:
        :param start_time:
        :param end_time:
        :param batch_id:
        :param page:
        :param page_size:
        :param sort: Must be supplied in the format [column_name] to denote asc sort by this column OR -[column_name] to denote desc sort by this column
        :param alert_rule_id:
        """

        params: Dict[str, Any] = {}
        if model_id is not None:
            params["model_id"] = model_id
        if metric is not None:
            params["metric"] = metric
        if status is not None:
            params["status"] = status
        if severity is not None:
            params["severity"] = severity
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if batch_id is not None:
            params["batch_id"] = batch_id
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort
        if alert_rule_id is not None:
            params["alert_rule_id"] = alert_rule_id

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alerts", params=params, validation_response_code=200
        )
        return PaginatedAlertResponse(**parsed_resp)

    def get_alert_by_id(self, alert_id: str) -> AlertResponse:
        """
        Retrieve a specific alert object

        :param alert_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alerts/{alert_id}", validation_response_code=200
        )
        return AlertResponse(**parsed_resp)

    def update_alert_status(
        self, alert_id: str, json_body: AlertRequest
    ) -> AlertResponse:
        """
        Update alert status for a specific alert id

        :param alert_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/alerts/{alert_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=204,
        )
        return AlertResponse(**parsed_resp)

    def send_email_notification_for_alert(
        self,
        alert_id: str,
        json_body: EmailNotificationBody,
        configuration_id: Optional[str] = None,
        manual_trigger: Optional[bool] = None,
    ) -> Response:
        """
        Sends an email notification for the given alert to the configured users and integrations

        :param alert_id:
        :param json_body:
        :param configuration_id:
        :param manual_trigger:
        """

        params: Dict[str, Any] = {}
        if configuration_id is not None:
            params["configuration_id"] = configuration_id
        if manual_trigger is not None:
            params["manual_trigger"] = manual_trigger

        raw_resp: Response = self.http_client.post(  # type: ignore
            f"/v3/alerts/{alert_id}/notifications",
            json=json_body.dict(by_alias=True, exclude_none=True),
            params=params,
            validation_response_code=200,
            return_raw_response=True,
        )
        return raw_resp

    def get_paginated_alert_notification_configurations(
        self,
        user_id: Optional[str] = None,
        model_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PaginatedAlertNotificationConfigurationsResponse:
        """
        Returns paginated notification configurations

        :param user_id:
        :param model_id:
        :param page:
        :param page_size:
        """

        params: Dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        if model_id is not None:
            params["model_id"] = model_id
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_notification_configurations",
            params=params,
            validation_response_code=200,
        )
        return PaginatedAlertNotificationConfigurationsResponse(**parsed_resp)

    def create_alert_notification_configuration(
        self, json_body: NewAlertNotificationConfiguration
    ) -> AlertNotificationConfiguration:
        """
        Creates a new alert notification configuration

        :param json_body: a new alert notification configuration to create
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/alert_notification_configurations",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return AlertNotificationConfiguration(**parsed_resp)

    def get_alert_notification_configuration_by_id(
        self, configuration_id: str
    ) -> AlertNotificationConfiguration:
        """
        Returns an alert notification configuration

        :param configuration_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_notification_configurations/{configuration_id}",
            validation_response_code=200,
        )
        return AlertNotificationConfiguration(**parsed_resp)

    def delete_alert_notification_configuration(
        self, configuration_id: str
    ) -> Response:
        """
        Deletes an alert notification configuration

        :param configuration_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/alert_notification_configurations/{configuration_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def update_alert_notification_configuration(
        self, configuration_id: str, json_body: AlertNotificationConfigurationUpdate
    ) -> AlertNotificationConfiguration:
        """
        Updates an alert notification configuration

        :param configuration_id:
        :param json_body: The fields to update in the AlertNotificationConfiguration object
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/alert_notification_configurations/{configuration_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return AlertNotificationConfiguration(**parsed_resp)

    def get_paginated_model_alert_rules(
        self,
        model_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[AlertRulesSort] = None,
        severity: Optional[str] = None,
        include_alert_metadata: Optional[bool] = None,
    ) -> PaginatedAlertRuleResponse:
        """
        Retrieve a paginated list of alert rules for the specific model

        :param model_id:
        :param page:
        :param page_size:
        :param sort:
        :param severity:
        :param include_alert_metadata:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if sort is not None:
            params["sort"] = sort.value
        if severity is not None:
            params["severity"] = severity
        if include_alert_metadata is not None:
            params["include_alert_metadata"] = include_alert_metadata

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/models/{model_id}/alert_rules",
            params=params,
            validation_response_code=200,
        )
        return PaginatedAlertRuleResponse(**parsed_resp)

    def create_model_alert_rule(
        self, model_id: str, json_body: AlertRuleRequest
    ) -> AlertRuleRequest:
        """
        Post a single alert rule for a specific model

        :param model_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/models/{model_id}/alert_rules",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return AlertRuleRequest(**parsed_resp)

    def delete_model_alert_rule(self, model_id: str, alert_rule_id: str) -> Response:
        """
        Archives the specified alert rule

        :param model_id:
        :param alert_rule_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/models/{model_id}/alert_rules/{alert_rule_id}",
            validation_response_code=201,
            return_raw_response=True,
        )
        return raw_resp

    def update_model_alert_rule(
        self, model_id: str, alert_rule_id: str, json_body: AlertRulePatch
    ) -> AlertRuleRequest:
        """
        Update the fields included in the request for the alert rule

        Note that the only fields that can be updated via this endpoint are name, bound, threshold, severity, lookback_period, subsequent_alert_wait_time, and enabled.

        :param model_id:
        :param alert_rule_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/alert_rules/{alert_rule_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return AlertRuleRequest(**parsed_resp)

    def update_alerts_for_model_alert_rule(
        self, model_id: str, alert_rule_id: str, json_body: AlertRequest
    ) -> BulkAlertUpdateResponse:
        """
        Bulk update all alerts for an alert rule

        :param model_id:
        :param alert_rule_id:
        :param json_body:
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/models/{model_id}/alert_rules/{alert_rule_id}/bulk_alerts",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return BulkAlertUpdateResponse(**parsed_resp)

    def get_paginated_alert_summary_notifications(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> PaginatedAlertSummaryConfigurationsResponse:
        """
        Returns paginated alert summary configurations for the requesting user's organization

        :param page:
        :param page_size:
        """

        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_summary_configurations",
            params=params,
            validation_response_code=200,
        )
        return PaginatedAlertSummaryConfigurationsResponse(**parsed_resp)

    def create_alert_summary_configuration(
        self, json_body: NewAlertSummaryConfiguration
    ) -> AlertSummaryConfiguration:
        """
        Creates a new alert summary configuration

        :param json_body: a new alert summary configuration to create
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/alert_summary_configurations",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return AlertSummaryConfiguration(**parsed_resp)

    def get_alert_summary_notification_by_id(
        self, configuration_id: str
    ) -> AlertSummaryConfiguration:
        """
        Returns the alert summary configuration

        :param configuration_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}",
            validation_response_code=200,
        )
        return AlertSummaryConfiguration(**parsed_resp)

    def delete_alert_summary_configuration(self, configuration_id: str) -> Response:
        """
        Deletes an alert summary configuration

        :param configuration_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def update_alert_summary_configuration(
        self, configuration_id: str, json_body: AlertSummaryConfigurationUpdate
    ) -> AlertSummaryConfiguration:
        """
        Updates an alert summary configuration

        :param configuration_id:
        :param json_body: the updated AlertSummaryConfiguration object
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return AlertSummaryConfiguration(**parsed_resp)

    def get_paginated_alert_summary_subscribers_by_id(
        self, configuration_id: str
    ) -> PaginatedAlertSummaryNotificationConfigurationsResponse:
        """
        Returns a collection of subscribers of an alert summary

        :param configuration_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}/subscribers",
            validation_response_code=200,
        )
        return PaginatedAlertSummaryNotificationConfigurationsResponse(**parsed_resp)

    def create_new_alert_summary_subscriber(
        self, configuration_id: str, json_body: NewAlertSummaryNotificationConfiguration
    ) -> AlertSummaryNotificationConfiguration:
        """
        Creates a new subscriber of an alert summary

        :param configuration_id:
        :param json_body: Tells us where and how to deliver an alert summary
        """

        parsed_resp: Dict[str, Any] = self.http_client.post(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}/subscribers",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=201,
        )
        return AlertSummaryNotificationConfiguration(**parsed_resp)

    def get_notification_configuration_for_alert_summary_subscriber_by_id(
        self, configuration_id: str, subscriber_id: str
    ) -> AlertSummaryNotificationConfiguration:
        """
        Returns the notification configuration for a subscriber of an alert summary

        :param configuration_id:
        :param subscriber_id:
        """

        parsed_resp: Dict[str, Any] = self.http_client.get(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}/subscribers/{subscriber_id}",
            validation_response_code=200,
        )
        return AlertSummaryNotificationConfiguration(**parsed_resp)

    def delete_notification_configuration_for_alert_summary_subscriber(
        self, configuration_id: str, subscriber_id: str
    ) -> Response:
        """
        Deletes the notification configuration for a subscriber of an alert summary

        :param configuration_id:
        :param subscriber_id:
        """

        raw_resp: Response = self.http_client.delete(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}/subscribers/{subscriber_id}",
            validation_response_code=204,
            return_raw_response=True,
        )
        return raw_resp

    def update_notification_configuration_for_alert_summary_subscriber(
        self,
        configuration_id: str,
        subscriber_id: str,
        json_body: AlertSummaryNotificationConfigurationUpdate,
    ) -> AlertSummaryNotificationConfiguration:
        """
        Updates the notification configuration of a subscriber of an alert summary

        :param configuration_id:
        :param subscriber_id:
        :param json_body: the updated AlertSummaryNotificationConfiguration object
        """

        parsed_resp: Dict[str, Any] = self.http_client.patch(  # type: ignore
            f"/v3/alert_summary_configurations/{configuration_id}/subscribers/{subscriber_id}",
            json=json_body.dict(by_alias=True, exclude_none=True),
            validation_response_code=200,
        )
        return AlertSummaryNotificationConfiguration(**parsed_resp)
