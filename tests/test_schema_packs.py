"""
Tests for the schema pack registry and its integration with the grammar
validator: pack-installed types must pass validate_node in their declared
space and enforce their property schemas.
"""

import pytest

from opencrab.grammar.validator import (
    get_allowed_relations,
    validate_edge,
    validate_node,
    validate_node_properties,
)
from opencrab.schemas import loader, pack_registry


@pytest.fixture
def isolated_types_dir(tmp_path, monkeypatch):
    """Point the type/relation registries and loader at empty temp directories."""
    types_dir = tmp_path / "types"
    types_dir.mkdir()
    relations_dir = tmp_path / "relations"
    monkeypatch.setattr(pack_registry, "_TYPES_DIR", types_dir)
    monkeypatch.setattr(pack_registry, "_RELATIONS_DIR", relations_dir)
    monkeypatch.setattr(loader, "SCHEMAS_DIR", types_dir)
    monkeypatch.setattr(loader, "RELATIONS_DIR", relations_dir)
    loader.load_type_schema.cache_clear()
    loader.load_pack_relations.cache_clear()
    yield types_dir
    loader.load_type_schema.cache_clear()
    loader.load_pack_relations.cache_clear()


class TestPackManifests:
    def test_all_packs_listed(self):
        names = {p["name"] for p in pack_registry.list_packs()}
        assert {"biomedical", "legal", "saas", "ontology-playground"} <= names

    def test_ontology_playground_types_are_rich(self):
        pack = pack_registry.get_pack("ontology-playground")
        assert pack is not None
        entries = pack_registry._type_entries(pack)
        assert len(entries) == 75
        for entry in entries:
            assert entry["space"] == "concept"
            assert entry["name"].isidentifier(), entry["name"]

    def test_identifier_properties_are_required(self):
        pack = pack_registry.get_pack("ontology-playground")
        by_name = {e["name"]: e for e in pack_registry._type_entries(pack)}
        assert by_name["Customer"]["properties"]["customerId"]["required"] is True

    def test_legacy_string_types_still_parse(self):
        pack = pack_registry.get_pack("saas")
        assert pack_registry._type_names(pack) == [
            "Subscription", "Feature", "ChurnSignal", "PricingTier", "ProductEvent",
        ]


class TestInstallValidatorIntegration:
    def test_pack_type_invalid_before_install(self, isolated_types_dir):
        assert not validate_node("concept", "WorkOrder")

    def test_install_makes_types_grammar_valid(self, isolated_types_dir):
        result = pack_registry.install_pack("ontology-playground")
        assert "error" not in result
        assert len(result["created"]) == 75
        assert validate_node("concept", "WorkOrder")
        assert validate_node("concept", "DisruptionEvent")
        # Declared space only — not valid elsewhere.
        assert not validate_node("resource", "WorkOrder")

    def test_canonical_types_unaffected(self, isolated_types_dir):
        assert validate_node("concept", "Concept")
        assert not validate_node("concept", "NoSuchType")

    def test_installed_schema_enforces_properties(self, isolated_types_dir):
        pack_registry.install_pack("ontology-playground")
        assert validate_node_properties("Customer", {"customerId": "C-1"})
        missing = validate_node_properties("Customer", {"name": "Kim"})
        assert not missing
        assert "customerId" in missing.error
        bad_enum = validate_node_properties(
            "Customer", {"customerId": "C-1", "loyaltyTier": "Diamond"}
        )
        assert not bad_enum

    def test_uninstall_reverts_grammar(self, isolated_types_dir):
        pack_registry.install_pack("ontology-playground")
        result = pack_registry.uninstall_pack("ontology-playground")
        assert len(result["removed"]) == 75
        assert not validate_node("concept", "WorkOrder")

    def test_legacy_pack_install_writes_properties_format(self, isolated_types_dir):
        result = pack_registry.install_pack("saas")
        assert len(result["created"]) == 5
        schema = loader.load_type_schema("Subscription")
        assert schema["pack"] == "saas"
        assert "properties" in schema


class TestPackRelations:
    def test_manifest_declares_96_relations(self):
        pack = pack_registry.get_pack("ontology-playground")
        rels = pack.get("relations", [])
        assert len(rels) == 96
        type_names = set(pack_registry._type_names(pack))
        for rel in rels:
            assert rel["from_space"] == "concept"
            assert rel["to_space"] == "concept"
            assert rel["from_type"] in type_names
            assert rel["to_type"] in type_names

    def test_pack_relation_invalid_before_install(self, isolated_types_dir):
        assert not validate_edge("concept", "concept", "OrderPlacedByCustomer")

    def test_install_extends_edge_grammar(self, isolated_types_dir):
        result = pack_registry.install_pack("ontology-playground")
        assert result["relations"] == 96
        assert validate_edge("concept", "concept", "OrderPlacedByCustomer")
        # Canonical meta-edge relations keep working.
        assert validate_edge("concept", "concept", "related_to")
        # Pack relations are scoped to their declared space pair.
        assert not validate_edge("subject", "resource", "OrderPlacedByCustomer")
        assert "OrderPlacedByCustomer" in get_allowed_relations("concept", "concept")

    def test_uninstall_reverts_edge_grammar(self, isolated_types_dir):
        pack_registry.install_pack("ontology-playground")
        result = pack_registry.uninstall_pack("ontology-playground")
        assert result["removed_relations"] is True
        assert not validate_edge("concept", "concept", "OrderPlacedByCustomer")
