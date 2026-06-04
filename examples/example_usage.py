"""
Example usage of the TRS Isomorphic Search library.

Demonstrates how to programmatically validate system graphs.
"""

import json
from pathlib import Path

from trs_isomorphic_search.models import SystemGraph, GraphNode, GraphEdge
from trs_isomorphic_search.validator import validate_isomorphism
from trs_isomorphic_search.templates import AGENT_LATTICE_TEMPLATE


def example_1_basic_validation():
    """Example 1: Validate a simple system graph against the agent lattice template."""
    print("=" * 60)
    print("Example 1: Basic Validation")
    print("=" * 60)

    # Create a system graph that matches the agent lattice pattern
    my_system = SystemGraph(
        nodes=[
            GraphNode(
                id="coordinator",
                layer_type="agent",
                attributes={"name": "main_coordinator"}
            ),
            GraphNode(
                id="decision_engine",
                layer_type="agent",
                attributes={"name": "decision_logic"}
            ),
            GraphNode(
                id="execution_layer",
                layer_type="agent",
                attributes={"name": "executor"}
            ),
            GraphNode(
                id="monitoring_agent",
                layer_type="agent",
                attributes={"name": "monitor"}
            ),
        ],
        edges=[
            GraphEdge(
                source="coordinator",
                target="decision_engine",
                relation_type="delegates_to"
            ),
            GraphEdge(
                source="decision_engine",
                target="execution_layer",
                relation_type="directs"
            ),
            GraphEdge(
                source="execution_layer",
                target="monitoring_agent",
                relation_type="reports_to"
            ),
            GraphEdge(
                source="monitoring_agent",
                target="coordinator",
                relation_type="feeds_back"
            ),
        ],
        metadata={"system_id": "example_system_1"}
    )

    # Validate against the agent lattice template
    report = validate_isomorphism(my_system, AGENT_LATTICE_TEMPLATE)

    print(f"Status: {report.status}")
    print(f"System ID: {report.system_id}")
    print(f"Risk Score: {report.residual_risk_score}")
    print(f"Message: {report.message}")
    print()


def example_2_load_from_json():
    """Example 2: Load system graph from JSON file."""
    print("=" * 60)
    print("Example 2: Load from JSON")
    print("=" * 60)

    # Create sample JSON data (in practice, you'd load from a file)
    json_data = {
        "nodes": [
            {
                "id": "main_orchestrator",
                "layer_type": "agent",
                "attributes": {"name": "orchestrator", "version": "2.0"}
            },
            {
                "id": "planner",
                "layer_type": "agent",
                "attributes": {"name": "planning_agent", "version": "2.0"}
            },
            {
                "id": "executor",
                "layer_type": "agent",
                "attributes": {"name": "execution_agent", "version": "2.0"}
            },
            {
                "id": "monitor",
                "layer_type": "agent",
                "attributes": {"name": "monitoring_agent", "version": "2.0"}
            },
        ],
        "edges": [
            {
                "source": "main_orchestrator",
                "target": "planner",
                "relation_type": "delegates_to",
                "weight": 1.0
            },
            {
                "source": "planner",
                "target": "executor",
                "relation_type": "directs",
                "weight": 1.0
            },
            {
                "source": "executor",
                "target": "monitor",
                "relation_type": "reports_to",
                "weight": 1.0
            },
            {
                "source": "monitor",
                "target": "main_orchestrator",
                "relation_type": "feeds_back",
                "weight": 1.0
            },
        ],
        "metadata": {"system_id": "json_system_example"}
    }

    # Parse JSON into SystemGraph
    system = SystemGraph.model_validate(json_data)

    # Validate
    report = validate_isomorphism(system, AGENT_LATTICE_TEMPLATE)

    print(f"Status: {report.status}")
    print(f"System ID: {report.system_id}")
    print(f"Risk Score: {report.residual_risk_score:.2f}")
    print(f"Message: {report.message}")
    print()


def example_3_invalid_system():
    """Example 3: Validate a system that doesn't match the template."""
    print("=" * 60)
    print("Example 3: Invalid System Detection")
    print("=" * 60)

    # Create a system with different structure
    invalid_system = SystemGraph(
        nodes=[
            GraphNode(id="node_a", layer_type="agent"),
            GraphNode(id="node_b", layer_type="agent"),
            GraphNode(id="node_c", layer_type="service"),  # Different type
            GraphNode(id="node_d", layer_type="agent"),
        ],
        edges=[
            GraphEdge(source="node_a", target="node_b", relation_type="calls"),
            GraphEdge(source="node_b", target="node_c", relation_type="uses"),
            GraphEdge(source="node_c", target="node_d", relation_type="calls"),
            GraphEdge(source="node_d", target="node_a", relation_type="notifies"),
        ],
        metadata={"system_id": "invalid_example"}
    )

    report = validate_isomorphism(invalid_system, AGENT_LATTICE_TEMPLATE)

    print(f"Status: {report.status}")
    print(f"System ID: {report.system_id}")
    print(f"Risk Score: {report.residual_risk_score:.2f}")
    print(f"Message: {report.message}")
    print()


def example_4_programmatic_report_output():
    """Example 4: Save validation report as JSON."""
    print("=" * 60)
    print("Example 4: Save Validation Report")
    print("=" * 60)

    # Create a test system
    test_system = SystemGraph(
        nodes=[
            GraphNode(id="coord", layer_type="agent"),
            GraphNode(id="decider", layer_type="agent"),
            GraphNode(id="executor", layer_type="agent"),
            GraphNode(id="monitor", layer_type="agent"),
        ],
        edges=[
            GraphEdge(source="coord", target="decider", relation_type="delegates_to"),
            GraphEdge(source="decider", target="executor", relation_type="directs"),
            GraphEdge(source="executor", target="monitor", relation_type="reports_to"),
            GraphEdge(source="monitor", target="coord", relation_type="feeds_back"),
        ],
        metadata={"system_id": "report_example"}
    )

    # Validate
    report = validate_isomorphism(test_system, AGENT_LATTICE_TEMPLATE)

    # Save report (in memory, simulating file save)
    report_json = json.dumps(
        report.model_dump(mode="json"),
        indent=2,
        default=str
    )

    print("Report JSON:")
    print(report_json)
    print()


if __name__ == "__main__":
    example_1_basic_validation()
    example_2_load_from_json()
    example_3_invalid_system()
    example_4_programmatic_report_output()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
