"""
Unit tests for the validation engine.

Tests isomorphism checking against various graph configurations.
"""

import pytest
from trs_isomorphic_search.models import SystemGraph, GraphNode, GraphEdge
from trs_isomorphic_search.validator import validate_isomorphism
from trs_isomorphic_search.templates import AGENT_LATTICE_TEMPLATE


class TestValidateIsomorphism:
    """Tests for the validate_isomorphism function."""

    def test_isomorphic_to_template(self):
        """Test validation passes for isomorphic graph."""
        # Use exact template structure
        report = validate_isomorphism(AGENT_LATTICE_TEMPLATE, AGENT_LATTICE_TEMPLATE)

        assert report.status == "PASS"
        assert report.residual_risk_score == 0.0
        assert report.isomorphism_map is not None

    def test_node_count_mismatch(self):
        """Test validation fails when node count differs."""
        input_graph = SystemGraph(
            nodes=[
                GraphNode(id="n1", layer_type="agent"),
                GraphNode(id="n2", layer_type="agent"),
            ],
            edges=[],
            metadata={"system_id": "test_mismatch"},
        )

        report = validate_isomorphism(input_graph, AGENT_LATTICE_TEMPLATE)

        assert report.status == "FAIL"
        assert report.residual_risk_score == 1.0
        assert "Node count mismatch" in report.message

    def test_edge_count_mismatch(self):
        """Test validation fails when edge count differs."""
        input_graph = SystemGraph(
            nodes=[
                GraphNode(id="n1", layer_type="agent"),
                GraphNode(id="n2", layer_type="agent"),
                GraphNode(id="n3", layer_type="agent"),
                GraphNode(id="n4", layer_type="agent"),
            ],
            edges=[
                GraphEdge(source="n1", target="n2", relation_type="depends_on"),
            ],
            metadata={"system_id": "test_edge_mismatch"},
        )

        report = validate_isomorphism(input_graph, AGENT_LATTICE_TEMPLATE)

        assert report.status == "FAIL"
        assert report.residual_risk_score == 1.0
        assert "Edge count mismatch" in report.message

    def test_non_isomorphic_structure(self):
        """Test validation fails for structurally different graphs."""
        # Create a graph with same node/edge count but different structure
        input_graph = SystemGraph(
            nodes=[
                GraphNode(id="a", layer_type="agent"),
                GraphNode(id="b", layer_type="agent"),
                GraphNode(id="c", layer_type="agent"),
                GraphNode(id="d", layer_type="agent"),
            ],
            edges=[
                GraphEdge(source="a", target="b", relation_type="connects_to"),
                GraphEdge(source="a", target="c", relation_type="connects_to"),
                GraphEdge(source="a", target="d", relation_type="connects_to"),
                GraphEdge(source="b", target="c", relation_type="connects_to"),
            ],
            metadata={"system_id": "test_non_iso"},
        )

        report = validate_isomorphism(input_graph, AGENT_LATTICE_TEMPLATE)

        assert report.status == "FAIL"
        assert report.residual_risk_score == 1.0

    def test_system_id_preserved(self):
        """Test that system_id is correctly preserved in report."""
        input_graph = SystemGraph(
            nodes=[GraphNode(id="n1", layer_type="test")],
            edges=[],
            metadata={"system_id": "custom_system_123"},
        )

        report = validate_isomorphism(input_graph, AGENT_LATTICE_TEMPLATE)

        assert report.system_id == "custom_system_123"

    def test_default_system_id(self):
        """Test default system_id when not provided."""
        input_graph = SystemGraph(
            nodes=[GraphNode(id="n1", layer_type="test")],
            edges=[],
            metadata={},
        )

        report = validate_isomorphism(input_graph, AGENT_LATTICE_TEMPLATE)

        assert report.system_id == "unknown"
