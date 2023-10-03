from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


__all__: Sequence[str] = ("Context",)


@dataclass
class Context:
    project_location: Path
    base: str
    bot_path: str
