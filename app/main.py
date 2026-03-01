from app.scraper import fetch_articles
from app.filter import is_potential_deal
from app.extractor import extract_article_text
from app.llm_parser import parse_deal_with_llm
from app.digest import save_digest
from app.logger import log_info, log_error
from app.validator import validate_output


def run_pipeline():
    print("\n🚀 Starting Pharma Deal Pipeline...\n")
    log_info("Pipeline started.")

    articles = fetch_articles()
    print(f"📰 Fetched {len(articles)} articles.")

    if not articles:
        print("❌ No articles fetched.")
        return

    filtered = [a for a in articles if is_potential_deal(a)]
    print(f"🔎 Filtered down to {len(filtered)} potential deal articles.")

    if not filtered:
        print("⚠ No articles passed keyword filtering.")
        return

    deals = []
    processed_count = 0

    for article in filtered:
        print(f"\n📌 Processing: {article['title']}")
        processed_count += 1

        text = extract_article_text(article["link"])

        if not text:
            print("   ❌ Extraction failed. Skipping.")
            continue

        print("   ✅ Article extracted.")

        structured = parse_deal_with_llm(text, article["link"])

        if not structured:
            print("   ❌ LLM parsing failed.")
            continue

        print("   🤖 LLM parsed successfully.")

        if structured.get("is_deal") and validate_output(structured):
            print("   💰 Confirmed Deal Found!")
            deals.append(structured)
        else:
            print("   ℹ Not a confirmed or valid deal.")

    if deals:
        print(f"\n🎯 Total confirmed deals found: {len(deals)}")
        save_digest(deals)
    else:
        print("\n⚠ No confirmed deals extracted today.")

    log_info(f"Pipeline completed. Processed {processed_count} articles.")
    print("\n✅ Pipeline finished.\n")


if __name__ == "__main__":
    run_pipeline()