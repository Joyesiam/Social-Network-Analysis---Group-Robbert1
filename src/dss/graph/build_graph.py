# """Functions to build NetworkX graphs from adjacency matrices."""

# from typing import Optional
# import networkx as nx
# from scipy.sparse import csr_matrix


# def build_graph(adjacency: csr_matrix, directed: Optional[bool] = False) -> nx.Graph:
#     """Construct a NetworkX graph from a sparse adjacency matrix.

#     Parameters
#     ----------
#     adjacency: csr_matrix
#         A square sparse matrix representing the adjacency weights between
#         nodes.  Non‑zero entries indicate edges; diagonal entries are
#         ignored.
#     directed: bool, optional
#         Whether to build a directed graph.  If False (default), an
#         undirected graph is built.  Otherwise, a `nx.DiGraph` is returned.

#     Returns
#     -------
#     networkx.Graph
#         The resulting graph.  Self loops are removed automatically.
#     """
#     n, m = adjacency.shape
#     if n != m:
#         raise ValueError("Adjacency matrix must be square.")
#     # Remove self loops by setting diagonal to zero
#     adjacency = adjacency.tolil()
#     adjacency.setdiag(0)
#     adjacency = adjacency.tocsr()
#     if directed:
#         G = nx.from_scipy_sparse_matrix(adjacency, create_using=nx.DiGraph)
#     else:
#         # Use undirected graph; duplicate edges will be collapsed
#         G = nx.from_scipy_sparse_matrix(adjacency, create_using=nx.Graph)
#     # Relabel nodes with integers (0 .. n-1).  This preserves the
#     # ordering from the adjacency matrix.
#     mapping = {i: i for i in range(n)}
#     G = nx.relabel_nodes(G, mapping)
#     return G


# if __name__ == "__main__":
#     # Quick demonstration
#     import numpy as np
#     from scipy.sparse import csr_matrix

#     adj = csr_matrix(np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]))
#     G = build_graph(adj)
#     print("Nodes:", G.nodes())
#     print("Edges:", list(G.edges()))



# File: dss-social-network-analysis/src/dss/graph/build_graph.py
"""Functions to build NetworkX graphs from adjacency matrices."""

from typing import Optional
import networkx as nx
from scipy.sparse import csr_matrix


def build_graph(adjacency: csr_matrix, directed: Optional[bool] = False) -> nx.Graph:
    """Construct a NetworkX graph from a sparse adjacency matrix.

    Parameters
    ----------
    adjacency: csr_matrix
        A square sparse matrix representing the adjacency weights between
        nodes. Non-zero entries indicate edges; diagonal entries are ignored.
    directed: bool, optional
        Whether to build a directed graph. If False (default), an
        undirected graph is built. Otherwise, a `nx.DiGraph` is returned.

    Returns
    -------
    networkx.Graph
        The resulting graph. Self loops are removed automatically.
    """
    n, m = adjacency.shape
    if n != m:
        raise ValueError("Adjacency matrix must be square.")

    # Remove self loops by setting diagonal to zero
    adjacency = adjacency.tolil()
    adjacency.setdiag(0)
    adjacency = adjacency.tocsr()

    create_using = nx.DiGraph if directed else nx.Graph

    # NetworkX 3.x uses from_scipy_sparse_array (matrix variant removed).
    # NetworkX 2.x uses from_scipy_sparse_matrix.
    if hasattr(nx, "from_scipy_sparse_array"):
        G = nx.from_scipy_sparse_array(adjacency, create_using=create_using)
    else:
        G = nx.from_scipy_sparse_matrix(adjacency, create_using=create_using)

    # Relabel nodes with integers (0 .. n-1). This preserves the ordering.
    mapping = {i: i for i in range(n)}
    G = nx.relabel_nodes(G, mapping)
    return G


if __name__ == "__main__":
    # Quick demonstration
    import numpy as np
    from scipy.sparse import csr_matrix

    adj = csr_matrix(np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]))
    G = build_graph(adj)
    print("Nodes:", G.nodes())
    print("Edges:", list(G.edges()))
