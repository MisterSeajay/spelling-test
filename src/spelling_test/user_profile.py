import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Profile:
    """Per-user progress: current level and a word -> score mapping."""

    user: str
    level: int = 1
    words: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.display_name = self.user.replace(" ", "_").capitalize()
        self.profile_path = Path(f"{self.user.lower().replace(' ', '_')}.profile")

    def __str__(self) -> str:
        return f"{self.display_name} @ level {self.level}"

    def profile_file_exists(self) -> bool:
        return self.profile_path.exists()

    def load_profile(self) -> None:
        with open(self.profile_path, encoding="utf-8") as f:
            data = json.load(f)
        self.level = data.get("level", 1)
        self.words = data.get("words", {})

    def save_profile(self) -> None:
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump({"level": self.level, "words": self.words}, f, indent=4)
