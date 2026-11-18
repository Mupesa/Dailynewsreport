"""
Persistent Memory & Self-Improvement Engine.
Tracks past themes, facts, and evolutionary feedback to continuously improve daily briefings.
"""

import os
import json
from datetime import datetime


class MemoryEngine:
    def __init__(self, history_file: str = "history.json", config_file: str = "config.json"):
        self.history_file = history_file
        self.config_file = config_file
        self.history = self._load_history()
        self.config = self._load_config()

    def _load_history(self) -> dict:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not read {self.history_file}: {e}")

        return {
            "system_initialized": datetime.now().strftime("%Y-%m-%d"),
            "runs_count": 0,
            "last_run_date": None,
            "recent_facts": [],
            "recent_themes": [],
            "evolution_level": 1,
            "feedback_notes": []
        }

    def _load_config(self) -> dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not read {self.config_file}: {e}")
        return {}

    def get_todays_theme(self) -> str:
        """Rotates through curiosity themes systematically."""
        theme_list = self.config.get("most_interesting_person", {}).get("theme_rotation", [
            "Psychology & Human Quirks",
            "Game Theory & High-Stakes Strategy",
            "Untold History & Secret Diplomatic Maneuvers",
            "Macroeconomics & Secret Fortunes",
            "Frontier Science & Mind-Bending Cosmos",
            "Philosophy & Counter-Intuitive Mental Models",
            "The Art of Wit, Rhetoric & Charisma"
        ])
        runs_count = self.history.get("runs_count", 0)
        idx = runs_count % len(theme_list)
        return theme_list[idx]

    def get_memory_context_for_prompt(self) -> str:
        """Constructs context for Gemini showing recent topics to avoid repetition and elevate depth."""
        runs = self.history.get("runs_count", 0)
        level = self.history.get("evolution_level", 1)
        recent_facts = self.history.get("recent_facts", [])[-5:]
        recent_themes = self.history.get("recent_themes", [])[-5:]
        notes = self.history.get("feedback_notes", [])[-3:]

        lines = [
            f"Consecutive Briefing Run: Day #{runs + 1}",
            f"Intellectual Evolution Stage: Tier {level}",
            f"Recent Facts/Hooks Covered (DO NOT REPEAT): {'; '.join(recent_facts) if recent_facts else 'None yet'}",
            f"Recent Focus Themes: {'; '.join(recent_themes) if recent_themes else 'Initial launch'}",
            f"Evolution Guidance: {'; '.join(notes) if notes else 'Deliver punchy, high-signal, charismatic insights.'}"
        ]
        return "\n".join(lines)

    def record_run(self, date_str: str, theme: str, fact_summary: str, key_insight: str):
        """Records today's execution to ensure tomorrow's run builds upon it."""
        self.history["runs_count"] = self.history.get("runs_count", 0) + 1
        self.history["last_run_date"] = date_str

        # Add theme
        themes = self.history.setdefault("recent_themes", [])
        themes.append(f"{date_str}: {theme}")
        self.history["recent_themes"] = themes[-14:]

        # Add fact
        if fact_summary:
            facts = self.history.setdefault("recent_facts", [])
            facts.append(fact_summary)
            self.history["recent_facts"] = facts[-20:]

        # Evolution stage level up every 7 runs
        runs = self.history["runs_count"]
        self.history["evolution_level"] = max(1, 1 + (runs // 7))

        self._save_history()

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save {self.history_file}: {e}")
