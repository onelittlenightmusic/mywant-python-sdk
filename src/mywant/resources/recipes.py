from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import MyWantClient


class RecipesResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def create(self, recipe: dict) -> dict:
        """Create a new recipe. recipe must have the top-level 'recipe' key."""
        return self._c._post("/api/v1/recipes", recipe, expected=201)

    def list(self) -> dict[str, Any]:
        """Return all recipes as a name→recipe map."""
        return self._c._get("/api/v1/recipes")

    def get(self, id: str) -> dict:
        return self._c._get(f"/api/v1/recipes/{id}")

    def update(self, id: str, recipe: dict) -> dict:
        return self._c._put(f"/api/v1/recipes/{id}", recipe)

    def delete(self, id: str) -> None:
        self._c._delete(f"/api/v1/recipes/{id}", expected=204)

    def create_from_want(self, want_id: str, name: str, description: str = "", version: str = "1.0.0") -> None:
        payload = {
            "wantId": want_id,
            "metadata": {"name": name, "description": description, "version": version},
        }
        self._c._post("/api/v1/recipes/from-want", payload, expected=201)
