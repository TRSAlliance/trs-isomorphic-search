import networkx as nx
import rustworkx as rx
from typing import Callable, Any

def graph_to_rx(nx_graph: nx.DiGraph) -> rx.PyDiGraph:
    """Convert NetworkX DiGraph to Rustworkx PyDiGraph"""
    rx_graph = rx.PyDiGraph()
    node_map = {}
    
    for node_id, data in nx_graph.nodes(data=True):
        idx = rx_graph.add_node(data)
        node_map[node_id] = idx
        
    for source, target, data in nx_graph.edges(data=True):
        rx_graph.add_edge(node_map[source], node_map[target], data)
        
    return rx_graph

def node_matcher(node1: dict, node2: dict) -> bool:
    """Custom node matcher focusing on structural layer_type"""
    return node1.get("layer_type") == node2.get("layer_type")

def edge_matcher(edge1: dict, edge2: dict) -> bool:
    """Custom edge matcher focusing on relation_type"""
    return edge1.get("relation_type") == edge2.get("relation_type")
