REQUIRED_FIELDS = [
    "company_a",
    "company_b",
    "deal_type",
    "deal_value",
    "deal_summary",
    "is_deal",
    "article_url"
]

def validate_output(data):
    if not isinstance(data, dict):
        return False

    for field in REQUIRED_FIELDS:
        if field not in data:
            return False

    if not isinstance(data["is_deal"], bool):
        return False

    return True