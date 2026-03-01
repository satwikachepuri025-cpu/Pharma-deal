#  Pharma Deal Intelligence Pipeline

### Automated LLM-Powered Pharma Deal Extraction System


## Overview

This project implements an automated data pipeline that detects pharmaceutical business deals from industry news sources using an LLM.

The system:

* Ingests RSS feeds from major pharma news websites
* Scrapes full article content (with Cloudflare bypass support)
* Uses an LLM to extract structured deal information
* Stores confirmed deals in JSON format
* Generates a daily pharma deal digest
* Supports automated scheduling

The architecture is modular and designed to resemble a lightweight production-grade pipeline.


## High-Level Architecture


                ┌──────────────────┐
                │   RSS Feeds      │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  RSS Ingestion   │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │  Article Fetcher │
                └─────────┬────────┘
                          │
                          ▼
          ┌────────────────────────────────┐
          │  Scraper Layer                 │
          │  - cloudscraper (primary)      │
          │  - Playwright (fallback)       │
          └─────────┬──────────────────────┘
                    │
                    ▼
          ┌────────────────────────────────┐
          │   Text Extraction Layer        │
          │   - HTML parsing               │
          │   - Content cleaning           │
          └─────────┬──────────────────────┘
                    │
                    ▼
          ┌────────────────────────────────┐
          │   LLM Parsing Layer            │
          │   - DeepSeek Chat API          │
          │   - Structured JSON output     │
          └─────────┬──────────────────────┘
                    │
                    ▼
          ┌────────────────────────────────┐
          │   Deal Classification          │
          │   - is_deal boolean            │
          └─────────┬──────────────────────┘
                    │
                    ▼
          ┌────────────────────────────────┐
          │   Storage + Digest Generator   │
          └────────────────────────────────┘



## RSS Ingestion

**Module:** `rss_fetcher.py`
**Library:** `feedparser`

Responsibilities:

* Poll RSS feeds from pharma news sources
* Normalize article metadata
* Limit article count per run
* Pass candidate articles downstream

Using RSS reduces unnecessary scraping and improves efficiency.

## Scraping Layer (403 / Cloudflare Resilient)

**Module:** `scraper.py`

Primary scraping:

* `cloudscraper`

Fallback:

* `Playwright` headless browser

Fallback triggers:

* HTTP 403 response
* Cloudflare “Attention Required” page
* Empty or extremely short HTML response

This layered strategy improves reliability across modern news websites.

## Text Extraction

* Removes HTML tags
* Extracts readable article content
* Cleans boilerplate noise
* Truncates long text to control LLM token usage

This ensures stable and cost-efficient LLM calls.


##  LLM-Based Structured Extraction

**Module:** `llm_parser.py`
**API:** DeepSeek Chat Completions

The LLM performs:

* Deal classification (deal vs non-deal)
* Structured entity extraction
* Summarization

### Enforced Output Schema

```json
{
  "company_a": "",
  "company_b": "",
  "deal_type": "",
  "deal_value": "",
  "deal_summary": "",
  "is_deal": true,
  "article_url": ""
}
```

If the article does not describe a deal:

```json
{
  "is_deal": false
}
```

Key design decisions:

* Structured JSON output enforced via API
* Avoids regex-based extraction
* LLM handles semantic reasoning

## Storage Layer

**Module:** `storage.py`

* Saves confirmed deals as JSON
* Persists results per run
* Enables historical record building

This design allows easy migration to a database later.

## Daily Digest

**Module:** `digest.py`

* Aggregates confirmed deals
* Formats human-readable summary
* Prints structured daily digest

Example output:


--- DAILY PHARMA DEAL DIGEST ---

Company A ↔ Company B
Deal Type | Deal Value
Summary...

##  Scheduler

**Module:** `scheduler.py`
**Library:** `schedule`

Supports:

### Production Mode

```bash
schedule.every().day.at("09:00").do(run_pipeline)
```

### Testing Mode

```bash
schedule.every(1).minutes.do(run_pipeline)
```

Run scheduler:

```bash
python -m app.scheduler
```

Run pipeline once:

```bash
python -m app.main
```

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/satwikachepuri025-cpu/Pharma-deal.git
cd scrapper_pipeline
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers

```bash
playwright install
```

### Configure Environment Variables

Create a `.env` file in the project root:

```bash
DEEPSEEK_API_KEY=your_api_key_here
```

## Project Structure
```

SCRAPPER_PIPELINE/
│
├── app/
│   ├── config.py
│   ├── digest.py
│   ├── extractor.py
│   ├── filter.py
│   ├── llm_parser.py
│   ├── logger.py
│   ├── main.py
│   ├── scheduler.py
│   ├── scraper.py
│   ├── validator.py
│
├── logs/
│   └── pipeline.log
│
├── output/
├── venv/
├── .env
├── README.md
└── requirements.txt
```

## Scalability Opportunities

Future improvements could include:

* PostgreSQL / SQLite integration
* Docker containerization
* Parallel scraping
* Deduplication logic
* Email delivery for digest
* Monitoring & alerting
* Confidence scoring for deals

The modular architecture enables incremental scaling without major refactoring.

## Design Philosophy

This system avoids:

* Hardcoded scraping rules per website
* Regex-based deal extraction
* Manual tagging logic

Instead, it leverages:

* RSS for structured ingestion
* Resilient scraping layer
* LLM-based semantic extraction
* Structured JSON contracts

This reflects a modern AI-assisted data pipeline approach.

## Technical Stack

* Python 3.9+
* requests
* feedparser
* beautifulsoup4
* cloudscraper
* playwright
* python-dotenv
* schedule
* DeepSeek Chat API

## What This Demonstrates

* Real-world web scraping challenges
* Cloudflare mitigation techniques
* LLM structured output enforcement
* Modular pipeline design
* Automated scheduling
* Production-style separation of concerns