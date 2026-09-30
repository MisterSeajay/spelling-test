import json
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class Profile:
    user: str
    level: int = 1
    words: dict = field(default_factory=dict)

    def __post_init__(self):
        self.display_name = self.user.replace(" ", "_").capitalize()
        self.profile_path = Path(f"{self.user.lower().replace(' ', '_')}.profile")

    def __str__(self):
        return f"{self.display_name} @ level {self.level}"

    def profile_file_exists(self) -> bool:
        return self.profile_path.exists()

    def load_profile(self):
        with open(self.profile_path) as f:
            data = json.load(f)
            self.level = data.get("level", 1)
            self.words = data.get("words", {})

    def save_profile(self):
        with open(self.profile_path, "w") as f:
            json.dump({"level": self.level, "words": self.words}, f, indent=4)
