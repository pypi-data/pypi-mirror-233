PART_SCHEMAS: dict[str, dict] = {
    "legal": {
        "type": "object",
        "properties": {
            "terms_of_service": {"type": "string"},
            "privacy_policy": {"type": "string"},
        },
        "required": ["terms_of_service", "privacy_policy"],
    },
    "auth": {},
    "app_launch": {
        "type": "object",
        "properties": {
            "app_version": {
                "type": "object",
                "properties": {
                    "required": {"type": "string"},
                    "latest": {"type": "string"},
                },
                "required": ["required", "latest"],
            },
        },
        "required": ["app_version"],
    },
}

DEFAULT_SCHEMA = {
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": True,
}
