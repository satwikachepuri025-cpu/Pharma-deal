import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


def parse_deal_with_llm(article_text, source_url=None):

    article_text = article_text[:4000]

    prompt = f"""
You are a pharma deal analyst.

Return JSON:

{{
  "company_a": "",
  "company_b": "",
  "deal_type": "",
  "deal_value": "",
  "deal_summary": "",
  "is_deal": true,
  "article_url": "{source_url or ''}"
}}

If not a deal, set is_deal=false and explain in summary.
"""

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)

        if response.status_code != 200:
            print("❌ DeepSeek error:", response.text)

            # Fallback JSON so pipeline continues
            return {
                "company_a": "",
                "company_b": "",
                "deal_type": "",
                "deal_value": "",
                "deal_summary": "LLM call failed: " + response.text,
                "is_deal": False,
                "article_url": source_url or ""
            }

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except Exception as e:
            print("❌ JSON parse error:", e)
            return {
                "company_a": "",
                "company_b": "",
                "deal_type": "",
                "deal_value": "",
                "deal_summary": "LLM returned invalid JSON",
                "is_deal": False,
                "article_url": source_url or ""
            }

    except Exception as e:
        print("❌ Request error:", e)
        return {
            "company_a": "",
            "company_b": "",
            "deal_type": "",
            "deal_value": "",
            "deal_summary": "Request exception: " + str(e),
            "is_deal": False,
            "article_url": source_url or ""
        }