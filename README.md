# 🌅 Dailynewsreport

An autonomous, self-evolving morning intelligence engine that delivers daily executive briefings across **Politics, Stocks & Trading, Technology, Sports, and Deep Curiosities** directly to your email every morning at **6:00 AM Mauritius Time (02:00 UTC)**.

Equipped with the **"Most Interesting Person in the Room"** feature: an obscure, conversation-starting fact, psychological insight, or mental model that will make you the most fascinating conversationalist in any setting by the end of the year.

---

## 🚀 Key Features

- **Runs 100% in the Cloud**: Powered by GitHub Actions. Operates reliably every day, even when your computer is completely powered off.
- **Powered by Google Gemini AI**: Synthesizes live global news into punchy, executive insights with second-order effects and macro trading angles.
- **The Most Interesting Person in the Room**: Daily rotation across 7 intellectual domains (Psychology, Game Theory, Secret History, Macroeconomics, Frontier Science, Philosophy, and Charisma).
- **Self-Improving Memory**: Tracks covered facts in `history.json` to guarantee zero repetition and progressively elevates sophistication every 7 days.
- **Daily Automated Archives**: Automatically commits every morning's digest into `archive/` on GitHub for long-term review.
- **Mobile-Responsive HTML Email**: Clean, executive design formatted for instant morning reading.

---

## ⏰ Schedule

- **Time**: 6:00 AM Indian/Mauritius Time (`MUT`, UTC+4)
- **GitHub Actions Cron**: `0 2 * * *` (02:00 AM UTC daily)
- **Manual Trigger**: Can be run anytime via the GitHub Actions tab (`workflow_dispatch`).

---

## 🛠️ Repository Structure

```
Dailynewsreport/
├── .github/
│   └── workflows/
│       └── daily_briefing.yml  # GitHub Actions automated cron schedule (06:00 MUT)
├── archive/                    # Daily digests saved as markdown
├── src/
│   ├── fetcher.py              # Fetches Google News RSS & custom search feeds
│   ├── intelligence.py         # Gemini 2.5/3.5/3.8 Flash synthesis & conversation curation
│   ├── mailer.py               # Responsive HTML email builder & SMTP dispatcher
│   └── memory.py               # Self-evolution engine & topic deduplication
├── main.py                     # Central orchestrator
├── config.json                 # Custom topics, search queries, recipient settings
├── history.json                # Cloud memory tracking past facts & evolution level
├── INSTRUCTIONS.md             # Guide on self-improvement & customizations
└── README.md                   # Project overview & quickstart
```

---

## 🔐 Secrets Configuration

Stored in GitHub Repository Secrets (`Settings` → `Secrets and variables` → `Actions`):

| Secret Name | Description | Status |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google Gemini AI API key | ✅ Configured |
| `EMAIL_USER` | Sender Gmail address (`anesumupesa@gmail.com`) | ⚙️ Pending user setup |
| `EMAIL_APP_PASSWORD` | 16-character Google App Password | ⚙️ Pending user setup |
| `RECIPIENT_EMAIL` | Target email (`anesumupesa@gmail.com`) | Optional (defaults to config.json) |

*For instructions on generating your 16-character Google App Password, see [INSTRUCTIONS.md](INSTRUCTIONS.md).*

---

## 🧪 Testing Locally

To test locally on your computer:
```bash
set GEMINI_API_KEY=your_gemini_api_key_here
python main.py
```
*(On Linux/macOS: `export GEMINI_API_KEY="..." && python3 main.py`)*
