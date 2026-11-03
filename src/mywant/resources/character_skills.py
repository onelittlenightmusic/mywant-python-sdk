from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ._common import seg, yaml_text

if TYPE_CHECKING:
    from ..client import MyWantClient


class CharacterSkillsResource:
    """A character's skills on the board (the Y slot's): /api/v1/character-skills.

    Defined by the GUI extension that gives the board them, which puts them
    when it starts. Schema: want-spec's spec/character-skill-spec.yaml.
    """

    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list[dict]:
        """In their digits' order."""
        return self._c._get("/api/v1/character-skills").get("skills", [])

    def get(self, name: str) -> dict:
        return self._c._get(f"/api/v1/character-skills/{seg(name)}")

    def create(self, skill: Union[str, dict]) -> dict:
        """A new one (fails when its name is taken)."""
        return self._c._post_yaml("/api/v1/character-skills", yaml_text(skill))

    def put(self, name: str, skill: Union[str, dict]) -> dict:
        """Made or replaced."""
        return self._c._put_yaml(f"/api/v1/character-skills/{seg(name)}", yaml_text(skill))

    def delete(self, name: str) -> None:
        self._c._delete(f"/api/v1/character-skills/{seg(name)}")
