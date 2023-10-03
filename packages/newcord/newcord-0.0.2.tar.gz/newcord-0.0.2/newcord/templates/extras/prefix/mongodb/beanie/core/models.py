from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Sequence, Type, Union

from beanie import Document
from pydantic import Field

if TYPE_CHECKING:
    from beanie import View
    from typing_extensions import Self

# fmt: off

__all__: Sequence[str] = (
    "models",
    "Task",
)

# fmt: on

# Documentation: http://beanie-odm.dev/


class Task(Document):
    user_id: int
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    completed: bool = Field(default=False)

    class Settings:
        name = "tasks"
        validate_on_save = True


# This will be used when we initialize beanie.
models: Optional[List[Union[Type[Document], Type[View], str]]] = [Task]
