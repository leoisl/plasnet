
from collections import Counter, defaultdict, deque

import networkx as nx
from networkx.utils import groups, not_implemented_for, py_random_state



@py_random_state(2)
@nx._dispatchable(edge_attrs="weight")
def appendable_lpa_communities(G, initial_labels=None, weight=None, seed=None):
    """Returns communities in `G` as detected by asynchronous label
    propagation.

    The asynchronous label propagation algorithm is described in
    [1]_. The algorithm is probabilistic and the found communities may
    vary on different executions.

    The algorithm proceeds as follows. After initializing each node with
    a unique label, the algorithm repeatedly sets the label of a node to
    be the label that appears most frequently among that nodes
    neighbors. The algorithm halts when each node has the label that
    appears most frequently among its neighbors. The algorithm is
    asynchronous because each node is updated without waiting for
    updates on the remaining nodes.

    This generalized version of the algorithm in [1]_ accepts edge
    weights.

    Parameters
    ----------
    G : Graph

    weight : string
        The edge attribute representing the weight of an edge.
        If None, each edge is assumed to have weight one. In this
        algorithm, the weight of an edge is used in determining the
        frequency with which a label appears among the neighbors of a
        node: a higher weight means the label appears more often.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    communities : iterable
        Iterable of communities given as sets of nodes.

    Notes
    -----
    Edge weight attributes must be numerical.

    References
    ----------
    .. [1] Raghavan, Usha Nandini, Réka Albert, and Soundar Kumara. "Near
           linear time algorithm to detect community structures in large-scale
           networks." Physical Review E 76.3 (2007): 036106.
    """

    if not initial_labels:
        labels = {n: i for i, n in enumerate(G)}
    else:
        start = max(initial_labels.values())
        H = G.remove_nodes_from(initial_labels.keys())
        labels = {n: i+start for i,n in enumerate(H)}
        labels.update(initial_labels)
            
    cont = True

    while cont:
        cont = False
        nodes = list(G)
        seed.shuffle(nodes)

        for node in nodes:
            if not G[node]:
                continue

            # Get label frequencies among adjacent nodes.
            # Depending on the order they are processed in,
            # some nodes will be in iteration t and others in t-1,
            # making the algorithm asynchronous.
            if weight is None:
                # initialising a Counter from an iterator of labels is
                # faster for getting unweighted label frequencies
                label_freq = Counter(map(labels.get, G[node]))
            else:
                # updating a defaultdict is substantially faster
                # for getting weighted label frequencies
                label_freq = defaultdict(float)
                for _, v, wt in G.edges(node, data=weight, default=1):
                    label_freq[labels[v]] += wt

            # Get the labels that appear with maximum frequency.
            max_freq = max(label_freq.values())
            best_labels = [
                label for label, freq in label_freq.items() if freq == max_freq
            ]

            # If the node does not have one of the maximum frequency labels,
            # randomly choose one of them and update the node's label.
            # Continue the iteration as long as at least one node
            # doesn't have a maximum frequency label.
            if labels[node] not in best_labels:
                labels[node] = seed.choice(best_labels)
                cont = True

    yield from groups(labels).values()