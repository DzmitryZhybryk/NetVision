bad_request = {
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid request"
                }
            }
        }
    }
}

forbidden = {
    403: {
        "description": "Not enough privileges",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            }
        }
    }
}

not_found: dict = {
    404: {
        "description": "Resource not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Resource not found"
                }
            }
        }
    }
}

conflict: dict = {
    409: {
        "description": "Resource already exist",
        "content": {
            "application/json": {
                "example": {
                    "detail": "The same data already exist in database"
                }
            }
        }
    }
}

unauthorized: dict = {
    401: {
        "description": "Try get resource like unauthorized user",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Incorrect username or password"
                }
            }
        }
    }
}

external_response_error: dict = {
    202: {
        "description": "Request in process",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Request in process"
                }
            }
        }
    },
    429: {
        "description": "You have reached your usage limit. Upgrade your plan if necessary",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Reached usage limit"
                }
            }
        }
    },
    451: {
        "description": "The person owning the email address asked us directly or indirectly to stop the processing of "
                       "their personal data. For this reason, you shouldn't process it yourself in any way",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Can't processing personal data"
                }
            }
        }
    }
}

get_responses = not_found | bad_request
get_all_response = bad_request
create_responses = conflict | bad_request
update_response = not_found | bad_request | conflict
delete_response = not_found | bad_request
