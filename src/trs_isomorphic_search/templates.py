"""
Pre-defined reference templates for structural validation.

Contains standard architectural templates for common TRS patterns.
"""

from .models import SystemGraph, GraphNode, GraphEdge


# Agent Lattice Template: Standard TRS agent communication pattern
AGENT_LATTICE_TEMPLATE = SystemGraph(
    nodes=[
        GraphNode(
            id="coordinator",
            layer_type="agent",
            attributes={"name": "coordinator", "tier": "orchestration"}
        ),
        GraphNode(
            id="decision_engine",
            layer_type="agent",
            attributes={"name": "decision_engine", "tier": "logic"}
        ),
        GraphNode(
            id="execution_layer",
            layer_type="agent",
            attributes={"name": "execution_layer", "tier": "operations"}
        ),
        GraphNode(
            id="monitoring_agent",
            layer_type="agent",
            attributes={"name": "monitoring_agent", "tier": "observation"}
        ),
    ],
    edges=[
        GraphEdge(
            source="coordinator",
            target="decision_engine",
            relation_type="delegates_to",
            weight=1.0
        ),
        GraphEdge(
            source="decision_engine",
            target="execution_layer",
            relation_type="directs",
            weight=1.0
        ),
        GraphEdge(
            source="execution_layer",
            target="monitoring_agent",
            relation_type="reports_to",
            weight=1.0
        ),
        GraphEdge(
            source="monitoring_agent",
            target="coordinator",
            relation_type="feeds_back",
            weight=1.0
        ),
    ],
    metadata={
        "template_id": "agent_lattice_v1",
        "description": "Standard agent coordination pattern with feedback loop",
        "tier_count": 4,
    }
)


def get_template(template_name: str) -> SystemGraph | None:
    """
    Retrieve a template by name.

    Args:
        template_name: Name of the template (e.g., 'agent_lattice')

    Returns:
        SystemGraph template, or None if not found
    """
    templates = {
        "agent_lattice": AGENT_LATTICE_TEMPLATE,
    }

    return templates.get(template_name.lower())


def list_templates() -> dict[str, str]:
    """
    List all available templates.

    Returns:
        Dictionary mapping template names to descriptions
    """
    return {
        "agent_lattice": "Standard agent coordination pattern with feedback loop",
    }
