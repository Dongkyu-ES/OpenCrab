"""
Type Schema Registry loader.

Loads YAML type schemas from opencrab/schemas/types/ and caches them.
If a node type has no registered schema file, load_type_schema() returns None
and validation is skipped (schema-optional pattern).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

SCHEMAS_DIR = Path(__file__).parent / "types"
RELATIONS_DIR = Path(__file__).parent / "relations"


@lru_cache(maxsize=None)
def load_type_schema(node_type: str) -> dict[str, Any] | None:
    """
    Load the YAML schema for *node_type* from schemas/types/<node_type>.yaml.

    Returns None if no schema file exists for that type.
    The result is cached after the first load.
    """
    path = SCHEMAS_DIR / f"{node_type}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_registered_types() -> list[str]:
    """Return a list of all node types that have a registered YAML schema."""
    if not SCHEMAS_DIR.exists():
        return []
    return sorted(p.stem for p in SCHEMAS_DIR.glob("*.yaml"))


def reload_schema(node_type: str) -> dict[str, Any] | None:
    """Clear the cache for *node_type* and reload from disk."""
    load_type_schema.cache_clear()
    return load_type_schema(node_type)


@lru_cache(maxsize=1)
def load_pack_relations() -> dict[tuple[str, str], frozenset[str]]:
    """
    Aggregate relation declarations from installed pack relation files
    (schemas/relations/<pack>.yaml), keyed by (from_space, to_space).

    Used by the grammar validator as an extension of META_EDGES.
    """
    result: dict[tuple[str, str], set[str]] = {}
    if not RELATIONS_DIR.exists():
        return {}
    for path in sorted(RELATIONS_DIR.glob("*.yaml")):
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        for rel in data.get("relations", []):
            name = rel.get("name")
            key = (rel.get("from_space"), rel.get("to_space"))
            if name and key[0] and key[1]:
                result.setdefault(key, set()).add(name)
    return {k: frozenset(v) for k, v in result.items()}


def reload_pack_relations() -> dict[tuple[str, str], frozenset[str]]:
    """Clear the pack-relation cache and reload from disk."""
    load_pack_relations.cache_clear()
    return load_pack_relations()
