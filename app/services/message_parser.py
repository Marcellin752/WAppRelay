from typing import Any

def extract_messages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """ Extraction of entry messages from Meta webhook payload."""
    messages = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages.extend(value.get("messages" or []))

    return messages