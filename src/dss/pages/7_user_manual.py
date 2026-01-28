"""Streamlit page: User Manual for the DSS."""

import streamlit as st


def page() -> None:
    st.set_page_config(page_title="User Manual", layout="wide")
    st.title("User Manual")
    st.markdown(
        """
        ## Introduction
        
        This Decision Support System (DSS) helps you analyse clandestine networks and make
        informed decisions about operational strategies.  The dashboard is organised
        into several pages, each focused on a specific analytic task.  This manual
        explains how to use the DSS and how to interpret its outputs.
        
        ## Upload & Overview
        
        1. Navigate to the **Upload & Overview** page.
        2. Use the file uploader to select a `.mtx` file containing the adjacency matrix of the network.
        3. After uploading, the DSS will validate the file, compute basic statistics
           (number of nodes, edges, density, connected components) and display a
           baseline network plot.  Any warnings about symmetry or self loops
           indicate potential data issues.
        
        ## Centrality Analysis
        
        Centrality measures quantify the importance of each node in the network.
        This page computes several centralities (degree, Katz, eigenvector,
        betweenness, closeness and PageRank) and allows you to:
        
        * **Weight measures:** Use the sliders in the sidebar to adjust the importance of each metric in the aggregated score.
        * **Aggregate metrics:** Choose between a weighted sum or a Borda count (rank aggregation) to combine measures.
        * **Highlight nodes:** Highlight the top and/or bottom `N` nodes based on the aggregated score.
        * **Select nodes:** Choose specific nodes from a list to inspect.  Selected nodes are highlighted on the network plot and their centrality values and aggregated score are shown in a table.
        * **Download data:** Export the centrality table as a CSV for offline analysis.
        
        Operational interpretation:
        
        * **Degree centrality:** Popularity of a node (number of connections).
        * **Katz centrality:** Accounts for all paths in the network, giving less weight to longer paths; useful for identifying influential spreaders.
        * **Eigenvector centrality:** Measures influence of a node in terms of its connections to other influential nodes.
        * **Betweenness centrality:** Captures brokerage power; nodes with high betweenness lie on many shortest paths.
        * **Closeness centrality:** Inverse of the average distance to all other nodes; smaller values indicate quick reachability.
        * **PageRank:** Probability of visiting a node in a random walk with teleportation; similar to eigenvector but more robust.

        ## Role Identification
        
        This page includes various methods of role identification, with Cooper and Barahona, RoleSim, RoleSim*, and RolX. The first
        three of these methods work by computing a similarity matrix, which can then be used for clustering, where the clustering assigns
        the roles. RolX groups nodes together with use of feature vectors, and assigns roles to these groups. Furthermore, this page
        creates leadership rankings for each of the computed roles, to find which roles consist of leaders and which consist of followers.
        When possible, options are provided to adjust each of these methods to suit the user's needs. Below we provide these methods:

        1. Select method out of Cooper and Barahona, RoleSim, RoleSim*, and RolX.
        2. Select role similarity parameters:

        **Cooper and Barahona:**
        * Select structural signature: k-hop or random walk.
        * Select number of hops/steps, to decide how long path lengths can be to be included in creating the similarity matrix.
        * Select similarity metric: cosine or correlation, which are functions used to measure distance of similarity between nodes.
        
        **RoleSim**:
        * Select value of beta (decay factor), where higher values result in less information being used, as well as a higher baseline value for the RoleSim score.
        * Select maximum number of iterations, where it can go both lower and higher. Lower number of iterations can result in loss of accuracy if convergence not reached, yet it does improve computation time. Higher number of iterations result in the opposite effect if convergence not reached. Use with caution.
        
        **RoleSim***:
        * Select value of beta (decay factor), where higher values result in less information being used, as well as a higher baseline value for the RoleSim* score.
        * Select maximum number of iterations, where it can go both lower and higher. Lower number of iterations can result in loss of accuracy if convergence not reached, yet it does improve computation time. Higher number of iterations result in the opposite effect if convergence not reached. Use with caution.
        * Select value of lambda (weight balancing factor), higher values result in more importance given to edges in the matching, while lower values result in higher importance of edges outside the matchinig. Read documentation for more detailed description of this variable.
        
        **RolX** does not make use of any role similarity parameters, so can continue to the next step immediately.

        3. Select role identification methods and parameters:
        * Select role identification method, which performs the clustering with the similarity matrix provided by the methods. Not applicable for RolX, as the role identification method is built in.
        * Set number of roles manually or select auto-detect number of roles. Maximum number of roles for RolX is set to 6, as there are 6 features and there cannot be more roles than features present.
        4. Click compute button, where RoleSim and RoleSim* have significantly larger computation time than other methods.
        * Check role cluster summary, to find mean values of centrality measures over all the nodes within the role.
        * Check leader rankings, to find which roles are more likely to consist of leadership nodes.
        * Check network graph, to visualise the network and find where in the network roles are present. Darker colours indicate lower role numbers and vice versa for higher role numbers.
        * Check community clustering comparison, to obtain some comparative information of role assignment and community clustering, with a table that shows number of nodes in cluster that have certain role.
        
        ## Community Detection & Robustness
        
        Community detection algorithms partition the network into highly connected
        subgroups. The DSS implements Louvain, Girvan–Newman and spectral
        clustering methods.  For each method the modularity `Q` score and
        cluster statistics are reported.  You can examine robustness by
        repeatedly removing a fraction of edges and observing how the community
        assignments change (ARI) and how modularity drops.
        
        * **Modularity Q Score**: A measure of how well a network is partitioned into communities.
        * **Within Ratio**: A measure of how internally connected the communities are, as oposed to connections outside of the community.

        #### Community clustering methods
        * **Spectral**: Identifies communities by using the eigenvectors of the graph Laplacian to partition the network into weakly connected groups. It is based on minimizing a graph-cut objective and is effective at revealing global structure in the network.
        * **Girvan-Newman**: Detects communities by repeatedly removing edges with high betweenness centrality, which act as bridges between groups. As these bridging edges are removed, the network splits into increasingly well-defined communities. 
        * **Louvain**: Detects communities by iteratively grouping nodes to maximize the modularity Q score. It is well suited for large networks and produces a hierarchical community structure.

        #### Robustness Analysis
        Robustness analysis evaluates how stable the results of a network analysis are when the network is slightly altered or when different methods are applied. 
        A robust result indicates that the identified structure reflects meaningful patterns rather than noise or modeling choices.
        * **Perturbation Test**: Assesses robustness by deliberately introducing small changes to the network, in this case removing some of the edges, and re-running the analysis. If the results remain largely unchanged, the detected structure is considered robust.
        * **Adjusted Rand Index (ARI)**: Measures the similarity between two clusterings while correcting for simularities that could occur by chance. In this context, it is used to quantify how consistently communities are identified under network perturbations.     
        
        ## Kemeny Analysis
        
        The Kemeny constant measures the expected time to go from one random node
        to another in a Markov chain defined on the network.  Smaller values indicate
        faster mixing and better overall connectivity.  On this page you can:
        
        * View the baseline Kemeny constant for the entire network.
        * View the edge sensitivity: how much the Kemeny constant would change if an edge is removed.
        * Interactively remove nodes (by selecting them in a list) and observe how
          the Kemeny constant changes.  A decrease after removing a node
          suggests that the node was hindering connectivity (e.g. a bottleneck). Conversely,
          an increase indicates that the node was facilitating connectivity.
        * Change the order of removals to see how different sequences impact the Kemeny constant.
        * View a network plot of the current graph where removed nodes are outlined in
          red and all node identifiers are displayed directly on the plot so
          that you can easily see which nodes have been removed.
        * Choose whether to recompute the constant on the largest connected
          component when removals disconnect the graph.
        
        ## Arrest Optimisation
        
        The agency has two departments to arrest members of the network.  To
        maximise arrests and minimise warnings (information leaks), it is
        preferable that connected members are assigned to the same department and
        that department capacities (ceil(`N`/2)) are respected【659313343491487†L195-L250】.  This page formulates the
        problem as a balanced cut optimisation.  You can:
        
        * **Select a community detection method** to determine which edges are
          penalised more heavily when cut.
        * **Adjust the regret strength (alpha):** Higher values penalise
          splitting edges within the same community and splitting high‑centrality
          nodes across departments.
        * **Adjust the penalty strength (beta):** Determines how many arrests
          are lost for each warning (cross‑department edge).
        * **Choose a centrality metric** to weight high‑centrality nodes in the
          regret term.
        
        The page displays the resulting assignment (department 0 or 1) on the
        network, the objective value, the number of cross‑department edges and
        the estimated number of effective arrests.  If an integer linear
        programming solver is unavailable, the DSS falls back to a heuristic.
        
        ## Recommended Workflow
        
        1. **Upload your network** on the first page and review its basic
           properties.  Resolve any data issues indicated by warnings.
        2. **Analyse centrality** to identify key players and potential
           influencers.  Adjust weighting schemes to see how rankings change.
        3. **Examine structural roles** to understand functional positions
           (brokers, hubs, peripherals) that may not align with centrality alone.
        4. **Detect communities** and evaluate robustness to see whether the
           network splits into stable factions.  Compare these with roles.
        5. **Assess connectivity** with the Kemeny constant and identify nodes
           whose removal improves mixing (possible targets for disruption).
        6. **Optimise arrests** by assigning members to departments, balancing
           capacity and minimising warnings.
        
        ## Glossary
        
        * **Centrality:** Quantitative measure of node importance in a network.
        * **Katz centrality:** Centrality measure incorporating paths of all
          lengths, attenuated by a factor of `alpha` per step.
        * **Kemeny constant:** Sum of mean first passage times; reflects network
          mixing speed.
        * **Modularity (Q):** Quality of a partition; higher values indicate
          dense intra‑community and sparse inter‑community connections.
        * **Adjusted Rand Index (ARI):** Metric to compare two partitions; 1
          indicates identical partitions, 0 indicates random agreement.
        * **Normalised Mutual Information (NMI):** Normalised measure of shared
          information between two partitions; ranges from 0 to 1.
        * **Balanced cut:** Graph partition problem with capacity constraints.
        
        ## Limitations
        
        * The results depend on the quality and completeness of the network data.
        * Community detection heuristics may yield different partitions on
          repeated runs; robustness analysis helps gauge stability.
        * The ILP solver used in the arrest optimisation may time out for very
          large networks; a heuristic solution is provided as a fallback.
        """
    )
'''
        ## Role Identification
        
        This page applies the role‑similarity approach of Cooper & Barahona (2010).
        Nodes with similar structural signatures (k‑hop neighbourhoods or
        random‑walk profiles) are grouped into roles.  You can choose:
        
        * **Signature type:** k‑hop degree distributions or random‑walk probability profiles.
        * **Similarity metric:** Cosine or correlation similarity.
        * **Clustering algorithm:** Spectral clustering or hierarchical clustering.
        * **Number of clusters:** Let the DSS choose automatically or set a value manually.
        
        The page displays a similarity heatmap, a network coloured by roles and a
        summary of each role in terms of average centrality measures and size.  A
        node selector in the sidebar lets you highlight specific nodes on the
        role plot; the selected nodes’ role assignments and centrality values
        are shown below the plot.  You can also compare role clusters to
        communities using Adjusted Rand Index (ARI) and Normalised Mutual
        Information (NMI).
'''

if __name__ == "__main__":
    page()
