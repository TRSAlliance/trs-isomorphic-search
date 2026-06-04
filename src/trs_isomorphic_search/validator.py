"""
Core validation logic for graph isomorphism checking.

Implements the VF2 isomorphism algorithm via NetworkX and Rustworkx.
"""

import networkx as nx
import rustworkx as rx
from .models import SystemGraph, ValidationReport
from .utils import graph_to_rx, node_matcher, edge_matcher, get_isomorphism_mapping


def validate_isomorphism(input_graph: SystemGraph, template: SystemGraph) -> ValidationReport:
    """
    Validate that input_graph is isomorphic to the template graph.

    Performs structural integrity verification by checking if the input system
    maintains isomorphism to a high-trust reference template.

    Args:
        input_graph: The system graph to validate
        template: The reference template graph

    Returns:
        ValidationReport with status, risk score, and optional mapping
    """
    # Build NetworkX graphs for isomorphism checking
    G_input = nx.DiGraph()
    G_template = nx.DiGraph()

    # Add nodes to input graph
    for node in input_graph.nodes:
        G_input.add_node(
            node.id,
            layer_type=node.layer_type,
            **node.attributes
        )

    # Add edges to input graph
    for edge in input_graph.edges:
        G_input.add_edge(
            edge.source,
            edge.target,
            relation_type=edge.relation_type,
            weight=edge.weight,
        )

    # Add nodes to template graph
    for node in template.nodes:
        G_template.add_node(
            node.id,
            layer_type=node.layer_type,
            **node.attributes
        )

    # Add edges to template graph
    for edge in template.edges:
        G_template.add_edge(
            edge.source,
            edge.target,
            relation_type=edge.relation_type,
            weight=edge.weight,
        )

    # Check basic graph properties first
    if len(G_input.nodes()) != len(G_template.nodes()):
        return ValidationReport(
            system_id=input_graph.metadata.get("system_id", "unknown"),
            status="FAIL",
            isomorphism_map=None,
            residual_risk_score=1.0,
            message="Node count mismatch: structural deviation detected.",
        )

    if len(G_input.edges()) != len(G_template.edges()):
        return ValidationReport(
            system_id=input_graph.metadata.get("system_id", "unknown"),
            status="FAIL",
            isomorphism_map=None,
            residual_risk_score=1.0,
            message="Edge count mismatch: structural deviation detected.",
        )

    # Perform isomorphism check using NetworkX with custom matchers
    try:
        mapping = get_isomorphism_mapping(
            G_input,
            G_template,
            node_matcher_func=node_matcher,
            edge_matcher_func=edge_matcher,
        )

        if mapping is not None:
            return ValidationReport(
                system_id=input_graph.metadata.get("system_id", "unknown"),
                status="PASS",
                isomorphism_map=mapping,
                residual_risk_score=0.0,
                message="Structural match to TRS high-trust template.",
            )
        else:
            return ValidationReport(
                system_id=input_graph.metadata.get("system_id", "unknown"),
                status="FAIL",
                isomorphism_map=None,
                residual_risk_score=1.0,
                message="Structural deviation detected: graph not isomorphic to template.",
            )
    except Exception as e:
        return ValidationReport(
            system_id=input_graph.metadata.get("system_id", "unknown"),
            status="FAIL",
            isomorphism_map=None,
            residual_risk_score=1.0,
            message=f"Validation error: {str(e)}",
        )
