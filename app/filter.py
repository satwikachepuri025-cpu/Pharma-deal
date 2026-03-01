DEAL_KEYWORDS = [
    "acquisition",
    "acquire",
    "merger",
    "agreement",
    "collaboration",
    "partnership",
    "licensing",
    "license",
    "investment",
    "joint venture",
    "production agreement"
]


def is_potential_deal(article):
    text = (article["title"] + " " + article["summary"]).lower()

    for keyword in DEAL_KEYWORDS:
        if keyword in text:
            return True

    return False