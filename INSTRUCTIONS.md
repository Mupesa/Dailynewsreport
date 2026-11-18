# 🧠 Autonomous Intelligence Engine — Operational Instructions

Welcome to your autonomous daily intelligence agent. This system runs in GitHub Actions every morning at **6:00 AM Mauritius Time (02:00 UTC)**, completely independent of whether your local computer is on or off.

---

## 🎯 The Core Mission
1. **High-Signal News**: Curate real-time updates across Politics, Stocks & Trading, Technology, Sports, and Custom Curiosities.
2. **Conversational Magnetism**: Transform Anesu into the **most interesting person in any room** by the end of the year.
3. **Continuous Evolution**: The agent improves every day, keeping track of what was covered, rotating through intellectual domains, and elevating the sophistication of its analysis.

---

## 🔄 How the Self-Improvement System Works

The engine maintains a persistent cloud memory in `history.json` and records every morning's digest in `archive/YYYY-MM-DD.md`.

### 1. Persistent Memory Tracking
- **`runs_count`**: Number of consecutive daily briefings delivered.
- **`evolution_level`**: Automatically advances every 7 days, prompting the AI to increase analytical depth, reduce introductory fluff, and tackle more sophisticated concepts.
- **`recent_facts` & `recent_themes`**: Stores past conversation starters and themes to guarantee that facts and conversation hooks are **never repeated**.
- **`feedback_notes`**: You can add notes or directives to `history.json` at any time; the AI reads this file before every run to refine its perspective.

### 2. Intellectual Theme Rotation
Every day rotates through a different domain of human curiosity:
1. **Psychology & Human Quirks** (Cognitive biases, persuasion secrets, behavioral economics)
2. **Game Theory & High-Stakes Strategy** (Nash equilibrium, signaling, geopolitical maneuvering)
3. **Untold History & Secret Diplomatic Maneuvers** (Fascinating historical turning points)
4. **Macroeconomics & Secret Fortunes** (Unusual trading lore, currency mechanics, commodity plays)
5. **Frontier Science & Mind-Bending Cosmos** (Astrophysics, quantum weirdness, biological oddities)
6. **Philosophy & Counter-Intuitive Mental Models** (First-principles thinking, inversion, second-order effects)
7. **The Art of Wit, Rhetoric & Charisma** (Conversational hooks, rhetorical devices, dinner-party stories)

---

## ⚙️ How to Customize Topics & News Sources

You can customize everything in `config.json`:

```json
{
  "recipient_email": "anesumupesa@gmail.com",
  "recipient_name": "Anesu",
  "categories": {
    "stocks_and_trading": {
      "sources": [
        "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=forex+crypto+commodities&hl=en-US&gl=US&ceid=US:en"
      ]
    }
  }
}
```

- To add a new interest (e.g. *Space Exploration* or *Real Estate*), simply add a Google News RSS query link under `sources` in `config.json`.
- Google News RSS search URL format:
  `https://news.google.com/rss/search?q=<YOUR_KEYWORDS_HERE>&hl=en-US&gl=US&ceid=US:en`

---

## ✉️ Setting Up Daily Email Delivery (Gmail)

To have the briefing delivered directly into your `anesumupesa@gmail.com` inbox:

1. **Generate a Google App Password**:
   - Go to your Google Account: [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable **2-Step Verification** (if not already enabled).
   - Search for **App Passwords** (or visit [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)).
   - App Name: `Dailynewsreport`.
   - Click **Create** and copy the 16-character generated password (e.g. `abcd efgh ijkl mnop`).

2. **Add to GitHub Secrets**:
   - In your GitHub repo: `https://github.com/Mupesa/Dailynewsreport/settings/secrets/actions`
   - Add secret: `EMAIL_USER` = `anesumupesa@gmail.com`
   - Add secret: `EMAIL_APP_PASSWORD` = `<your-16-char-app-password>`
   - (Note: `GEMINI_API_KEY` is already stored as a secret in your repository!)

---

## 🧪 How to Test It Immediately

You don't have to wait until 6:00 AM!
1. Go to your repository on GitHub: [https://github.com/Mupesa/Dailynewsreport/actions](https://github.com/Mupesa/Dailynewsreport/actions)
2. Click **Daily Intelligence & News Briefing** in the left sidebar.
3. Click **Run workflow** -> **Run workflow**.
4. Within 30 seconds, the workflow will fetch the news, invoke Gemini, archive the report, and publish the full briefing in the GitHub Job Summary (and email it if SMTP secrets are added)!
