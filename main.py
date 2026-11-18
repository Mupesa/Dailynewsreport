"""
Main orchestrator for Daily News & Intelligence Report.
Fetches feeds, calls Gemini AI, delivers executive email, and records learning memory.
"""

import os
import sys
import json
from datetime import datetime

from src.fetcher import fetch_all_categories
from src.memory import MemoryEngine
from src.intelligence import generate_daily_briefing
from src.mailer import send_email


def main():
    print("=" * 60)
    print("🚀 Starting Daily Morning Intelligence Orchestrator")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # 1. Initialize Memory & Configuration
    memory = MemoryEngine(history_file="history.json", config_file="config.json")
    config = memory.config

    recipient_email = os.environ.get("RECIPIENT_EMAIL") or config.get("recipient_email", "anesumupesa@gmail.com")
    recipient_name = config.get("recipient_name", "Anesu")
    categories_cfg = config.get("categories", {})

    today_theme = memory.get_todays_theme()
    memory_context = memory.get_memory_context_for_prompt()

    print(f"👤 Briefing for: {recipient_name} ({recipient_email})")
    print(f"💡 Today's Curiosity Theme: {today_theme}")
    print(f"🧠 Intelligence Level: Tier {memory.history.get('evolution_level', 1)}")

    # 2. Fetch Live News Across Categories
    print("\n📡 Fetching live news feeds...")
    raw_data = fetch_all_categories(categories_cfg)
    total_articles = sum(len(c["articles"]) for c in raw_data.values())
    print(f"✓ Collected {total_articles} high-signal headlines across {len(raw_data)} categories.")

    # 3. Call Gemini AI for Synthesis & Analysis
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is missing!")
        sys.exit(1)

    print("\n🤖 Calling Gemini AI for synthesis and intelligence curation...")
    briefing_data = generate_daily_briefing(raw_data, memory_context, today_theme, api_key)
    markdown_report = briefing_data["markdown"]
    fact_hook = briefing_data["fact_hook"]

    print("✓ Intelligence briefing generated successfully.")

    # 4. Save Archive File
    date_slug = datetime.now().strftime("%Y-%m-%d")
    archive_dir = "archive"
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, f"{date_slug}.md")

    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)
    print(f"✓ Daily report archived to: {archive_path}")

    # 5. Output to GitHub Step Summary if running in GitHub Actions
    gh_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary_path:
        try:
            with open(gh_summary_path, "a", encoding="utf-8") as sf:
                sf.write(f"\n{markdown_report}\n")
            print("✓ Appended briefing to GitHub Actions Step Summary.")
        except Exception as e:
            print(f"Warning: Could not write to GITHUB_STEP_SUMMARY: {e}")

    # 6. Send Email
    smtp_user = os.environ.get("EMAIL_USER")
    smtp_pass = os.environ.get("EMAIL_APP_PASSWORD")

    subject = f"🌅 Morning Intelligence | {today_theme} • {datetime.now().strftime('%b %d')}"
    email_sent = send_email(
        subject=subject,
        markdown_content=markdown_report,
        recipient_email=recipient_email,
        smtp_user=smtp_user,
        smtp_password=smtp_pass
    )

    # 7. Update Persistent Memory
    memory.record_run(
        date_str=date_slug,
        theme=today_theme,
        fact_summary=fact_hook,
        key_insight=f"Run completed with {total_articles} source articles."
    )
    print(f"✓ Self-improvement engine updated (Total runs: {memory.history['runs_count']}).")

    print("\n" + "=" * 60)
    print("✅ All morning briefing tasks completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
