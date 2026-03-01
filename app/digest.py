import os
import json
import pandas as pd
from app.config import MAX_DEALS


def save_digest(deals):

    os.makedirs("output", exist_ok=True)

    valid_deals = [d for d in deals if d and d["is_deal"]]
    unique = {}

    for deal in valid_deals:
        # Order-independent deduplication
        key = tuple(sorted([deal["company_a"], deal["company_b"]]))
        if key not in unique:
            unique[key] = deal

    final_deals = list(unique.values())[:MAX_DEALS]

    # JSON
    with open("output/deals.json", "w") as f:
        json.dump(final_deals, f, indent=4)

    # CSV
    df = pd.DataFrame(final_deals)
    df.to_csv("output/deals.csv", index=False)

    # HTML
    df.to_html("output/deals.html", index=False)

    print("\n--- DAILY PHARMA DEAL DIGEST ---\n")
    for deal in final_deals:
        print(f"{deal['company_a']} ↔ {deal['company_b']}")
        print(f"{deal['deal_type']} | {deal['deal_value']}")
        print(f"{deal['deal_summary']}")
        print("-" * 50)