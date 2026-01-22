"""Compute and cache graph layouts."""

from typing import Dict, Any
import networkx as nx
import numpy as np
from ..utils.caching import cache_data
from ..config import DEFAULTS


# @cache_data
# def compute_layout(G: nx.Graph, layout_name: str = DEFAULTS.layout, seed: int = DEFAULTS.seed) -> Dict[Any, np.ndarray]:
#     """Compute a layout for visualising the graph.

#     Parameters
#     ----------
#     G: networkx.Graph
#         The graph to layout.
#     layout_name: str, optional
#         The name of the layout algorithm.  Currently only "spring" is
#         supported.  Additional layouts could be added in the future.
#     seed: int, optional
#         Seed for random layouts, ensuring reproducibility.

#     Returns
#     -------
#     dict
#         A mapping of node to 2‑D coordinates.
#     """
#     spacing = DEFAULTS.layout_spacing
#     if layout_name == "spring":
#         # return nx.spring_layout(G, seed=seed)
#         n_nodes = max(G.number_of_nodes(), 1)
#         base_k = 1 / np.sqrt(n_nodes)
#         return nx.spring_layout(G, seed=seed, k=base_k * spacing)
#     elif layout_name == "kamada_kawai":
#         # return nx.kamada_kawai_layout(G)
#         pos = nx.kamada_kawai_layout(G)
#     else:
#         # Fallback to spring layout
#         # return nx.spring_layout(G, seed=seed)
#         n_nodes = max(G.number_of_nodes(), 1)
#         base_k = 1 / np.sqrt(n_nodes)
#         return nx.spring_layout(G, seed=seed, k=base_k * spacing)

#     if spacing != 1.0:
#         pos = {node: coords * spacing for node, coords in pos.items()}
#     return pos


# if __name__ == "__main__":
#     import networkx as nx
#     G = nx.cycle_graph(5)
#     pos = compute_layout(G)
#     print(pos)
#     print(pos)





def rescale_layout(pos: Dict[Any, np.ndarray], scale: float = 1.0) -> Dict[Any, np.ndarray]:
    """
    Rescale a network layout to fill the available plotting area.

    NetworkX layouts typically return coordinates in a small range
    (often roughly [-1, 1]), which can leave large margins in the final
    visualisation.  This function rescales the layout so that:

    - Relative geometry is preserved
    - Clusters and factions remain clearly visible
    - The network occupies almost the full canvas

    Parameters
    ----------
    pos : dict
        Mapping of node -> 2-D coordinate array.
    scale : float
        Target half-range of coordinates.  For scale = 1.0, coordinates
        are mapped to approximately [-1, 1] on each axis.

    Returns
    -------
    dict
        Rescaled mapping of node -> 2-D coordinate array.
    """
    if not pos:
        return pos

    nodes = list(pos.keys())
    coords = np.asarray([pos[node] for node in nodes], dtype=float)

    # Compute bounding box of the layout
    min_vals = coords.min(axis=0)
    max_vals = coords.max(axis=0)

    # Prevent division by zero in degenerate cases
    span = np.maximum(max_vals - min_vals, 1e-12)

    # Normalise to [0, 1]
    coords = (coords - min_vals) / span

    # Map to [-scale, scale]
    coords = (coords - 0.5) * 2.0 * scale

    return {node: coords[i] for i, node in enumerate(nodes)}


@cache_data
def compute_layout(
    G: nx.Graph,
    layout_name: str = DEFAULTS.layout,
    seed: int = DEFAULTS.seed,
) -> Dict[Any, np.ndarray]:
    """
    Compute a 2-D layout for visualising a network.

    This function acts as the single entry point for all layout logic
    used in the DSS visualisations.  Layout-specific parameters are
    derived from global defaults so that behaviour can be tuned without
    modifying analysis or UI code.

    Parameters
    ----------
    G : networkx.Graph
        The graph to compute a layout for.
    layout_name : str, optional
        Name of the layout algorithm to use.  Supported values:
        - "spring"
        - "kamada_kawai"
        Unknown values fall back to the spring layout.
    seed : int, optional
        Random seed used for reproducibility in stochastic layouts.

    Returns
    -------
    dict
        Mapping of node -> 2-D coordinate array.
    """
    spacing = DEFAULTS.layout_spacing

    # Scale the spring constant with graph size to maintain comparable density
    n_nodes = max(G.number_of_nodes(), 1)
    base_k = 1.0 / np.sqrt(n_nodes)

    if layout_name == "spring":
        # Force-directed layout with explicit spacing control
        pos = nx.spring_layout(
            G,
            seed=seed,
            k=base_k * spacing,
            iterations=100,
        )

    elif layout_name == "kamada_kawai":
        # Energy-based layout optimising graph-theoretic distances
        pos = nx.kamada_kawai_layout(G)

    else:
        # Fallback to spring layout for unknown layout names
        pos = nx.spring_layout(
            G,
            seed=seed,
            k=base_k * spacing,
            iterations=100,
        )

    # Expand the layout to fill the plotting area while preserving structure
    pos = rescale_layout(pos, scale=1.0)

    return pos


if __name__ == "__main__":
    # Minimal smoke test for manual inspection
    import pprint

    G_test = nx.karate_club_graph()
    layout = compute_layout(G_test)
    pprint.pprint(layout)
