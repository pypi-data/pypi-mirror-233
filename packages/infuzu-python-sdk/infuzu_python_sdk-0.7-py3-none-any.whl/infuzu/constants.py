"""
constants.py
This module contains constant values used throughout the SDK for making requests
to the associated API and other related operations.
"""

# The header name used to send the authentication token with API requests.
INFUZU_AUTH_TOKEN_HEADER_NAME: str = "I-Auth-Token"

# Default timeout for API requests in seconds.
DEFAULT_REQUEST_TIMEOUT: int = 30

# Base URL for the Clockwise service hosted by Infuzu.
CLOCKWISE_BASE_URL: str = "https://clockwise.infuzu.com/"

# Endpoint to retrieve assignments from the Clockwise service.
CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT: str = "assignment/"

# Endpoint to mark an assignment as completed in the Clockwise service.
CLOCKWISE_ASSIGNMENT_COMPLETE_ENDPOINT: str = "task-completed/"
CLOCKWISE_CREATE_RULE_ENDPOINT: str = "rule/create/"
CLOCKWISE_DELETE_RULE_ENDPOINT: str = "rule/delete/<str:rule_id>/"
CLOCKWISE_RULE_LOGS_ENDPOINT: str = "rule/logs/<str:rule_id>/"
