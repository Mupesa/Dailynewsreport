"""
AI Intelligence & Synthesis Module.
Uses Google Gemini API to analyze raw news, synthesize insights, and craft
the 'Most Interesting Person in the Room' intellectual centerpiece.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime


FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest"
]


def call_gemini(prompt: str, api_key: str) -> str:
    """Calls Gemini generateContent with fallback across models."""
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    last_error = None
    for model in FALLBACK_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 3500
            }
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=data, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=50) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                candidates = res.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"Warning: Model {model} returned HTTP {e.code}: {err_body[:120]}")
            last_error = e
        except Exception as e:
            print(f"Warning: Model {model} failed: {e}")
            last_error = e

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


def generate_daily_briefing(raw_categories: dict, memory_context: str, today_theme: str, api_key: str) -> dict:
    """Prompts Gemini to generate the morning intelligence briefing."""
    today_str = datetime.now().strftime("%A, %B %d, %Y")

    # Format raw articles for prompt
    articles_text_blocks = []
    for cat_key, cat_data in raw_categories.items():
        title = cat_data["display_name"]
        articles = cat_data["articles"]
        articles_text_blocks.append(f"### CATEGORY: {title}")
        for idx, art in enumerate(articles, 1):
            articles_text_blocks.append(f"{idx}. {art['title']}")
            if art.get("description"):
                articles_text_blocks.append(f"   Context: {art['description']}")
            if art.get("link"):
                articles_text_blocks.append(f"   Source URL: {art['link']}")

    all_articles_text = "\n".join(articles_text_blocks)

    system_instruction = f"""You are the personal Chief Intelligence Officer and intellectual mentor to Anesu.
Every morning, Anesu reads this briefing at 6:00 AM (Mauritius Time).

CORE MISSION:
Anesu wants to be the MOST INTERESTING PERSON IN ANY ROOM by the end of the year. He needs:
1. High-signal, executive summaries of what is happening right now in Politics, Stocks & Trading, Technology, Sports, and Curiosities.
2. A captivating, mind-expanding intellectual centerpiece: an obscure, fascinating fact or mental model that makes anyone who hears it stop and listen.
3. Sharper, more sophisticated thinking every day.

TODAY'S SPECIAL THEME: {today_theme}
DATE: {today_str}

PERSISTENT MEMORY & CONTINUOUS IMPROVEMENT:
{memory_context}

RAW NEWS HEADLINES COLLECTED TODAY:
{all_articles_text}

INSTRUCTIONS FOR OUTPUT:
Craft an executive, beautifully written, magnetic morning intelligence briefing in clean Markdown.
Structure your report with these sections:

# 🌅 Executive Intelligence Briefing | {today_str}
*Curated exclusively for Anesu*

## 🧠 The Most Interesting Person in the Room: {today_theme}
- **The Mind-Expanding Fact / Phenomenon**: An obscure, counter-intuitive, or mind-blowing reality from history, psychology, science, or game theory. Explain the mechanism clearly.
- **The Dinner-Table Conversation Starter**: Exactly how to bring this up casually in conversation (e.g., *"Did you know that...?"* or a thought experiment) that instantly captivates people.
- **The Mental Model / Razor**: A crisp heuristic or decision framework derived from this fact that improves daily life or strategy.

## 🏛️ Global Politics & Geopolitics
- 2 to 3 key developments from the news above.
- For each item, give: **The Strategic Move**, **Why It Matters**, and **The 2nd-Order Effect**.

## 📈 Stocks, Trading & Macro Markets
- 2 to 3 key financial / market movements.
- Focus on: **Market Sentiment**, **The Big Macro Trade / Opportunity**, and **What Smart Money Is Watching**.

## ⚡ Technology & Frontier AI
- 2 to 3 breakthrough updates.
- Focus on: **The Engineering / Product Leap** and **The Industry Disruption**.

## ⚽ Sports Highlights & Tactical Drama
- 2 to 3 top sporting moments.
- Focus on: **The Climax / Result** and **The Tactical or Human Drama**.

## 🔍 Deep Curiosities & Frontier Discoveries
- 1 to 2 fascinating snippets from the custom searches or science.

## 🚀 Today's Curiosity Challenge
- A single intriguing question or observation for Anesu to ponder today.

IMPORTANT GUIDELINES:
- No filler or fluff. Be concise, punchy, articulate, and intellectually rigorous.
- Format links naturally if relevant.
- Do NOT use generic buzzwords. Speak with the authority of a world-class strategist and conversational savant.

At the very end of your response, output on a single line:
FACT_HOOK: <A short 1-sentence summary of today's fact for memory tracking>
"""

    response_text = call_gemini(system_instruction, api_key)

    # Extract FACT_HOOK
    fact_hook = ""
    lines = response_text.splitlines()
    clean_lines = []
    for line in lines:
        if line.strip().startswith("FACT_HOOK:"):
            fact_hook = line.strip().replace("FACT_HOOK:", "").strip()
        else:
            clean_lines.append(line)

    cleaned_markdown = "\n".join(clean_lines).strip()

    return {
        "markdown": cleaned_markdown,
        "fact_hook": fact_hook or f"Insight on {today_theme}",
        "theme": today_theme,
        "date_str": today_str
    }
