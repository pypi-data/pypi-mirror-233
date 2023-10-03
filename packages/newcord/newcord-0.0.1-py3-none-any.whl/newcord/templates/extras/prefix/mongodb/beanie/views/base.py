from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Optional, Union, ClassVar
from discord import ui, ButtonStyle

if TYPE_CHECKING:
    from discord import Interaction, Message, WebhookMessage, User, Member

__all__: Sequence[str] = ("View",)


class View(ui.View):
    message: ClassVar[Union[Message, WebhookMessage]]

    def __init__(
        self,
        author: Optional[Union[User, Member]],
        *,
        timeout: Optional[float] = 180,
        disable_on_timeout: bool = True,
        disable_button_style: Optional[ButtonStyle] = ButtonStyle.grey,
    ):
        super().__init__(timeout=timeout)
        self.author = author
        self.disable_on_timeout = disable_on_timeout
        self.disable_button_style = disable_button_style

    def disable_items(self, *exclude: ui.Item[Any]) -> None:
        for child in self.children:
            if child not in exclude:
                if isinstance(child, ui.Select):
                    child.disabled = True

                if isinstance(child, ui.Button):
                    child.disabled = True

                    if self.disable_button_style is not None:
                        child.style = self.disable_button_style

    async def on_timeout(self) -> None:
        if hasattr(self, "message") and self.disable_on_timeout:
            self.disable_items()
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        if self.author and self.author.id != interaction.user.id:
            await interaction.response.send_message(
                f"This view can only be controlled by {self.author.mention}",
                ephemeral=True,
            )
            return False
        return True
