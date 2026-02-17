import pandas as pd
import numpy as np

def read_in_clusters(compare_tsv):
    pling_df = pd.read_csv(compare_tsv, sep="\t")
    plasmids = list(pling_df["plasmid"].values)
    clusters_pling = {i:set(pling_df[pling_df["type"]==el]["plasmid"].values) for i,el in enumerate(list(set(pling_df["type"])))}
    clusters_pling_old = {i:set(pling_df[pling_df["previous_type"]==el]["plasmid"].values) for i,el in enumerate(list(set(pling_df["previous_type"])))}
    return clusters_pling, clusters_pling_old, plasmids

def make_contingency_matrix(clusters_1, clusters_2): #clusters_1 and clusters_2 are dictionaries of clusters, k_1 and k_2 the lengths of the respective dictionaries
    k_1 = len(clusters_1)
    k_2 = len(clusters_2)
    contingency = np.zeros((k_1,k_2))
    for i in range(k_1):
        for j in range(k_2):
            contingency[i][j] = len(clusters_1[i].intersection(clusters_2[j]))
    return contingency, k_1, k_2

def split_join(contingency, k_1, k_2, n): #clusters_1 and clusters_2 are dictionaries of clusters, n is the total number of data points (plasmids)
    dist = 2*n - sum([max(contingency[i]) for i in range(k_1)]) - sum([max(contingency[:,j]) for j in range(k_2)])
    return int(dist)

def rand_index(contingency):
    contingency = np.asarray(contingency)

    def comb2(x):
        return x * (x - 1) / 2.0

    n = contingency.sum()
    if n <= 1:
        return 1.0  # degenerate case

    # True positives
    tp = np.sum(comb2(contingency))

    # Row and column sums
    row_sums = contingency.sum(axis=1)
    col_sums = contingency.sum(axis=0)

    sum_rows = np.sum(comb2(row_sums))
    sum_cols = np.sum(comb2(col_sums))

    fp = sum_cols - tp
    fn = sum_rows - tp

    total_pairs = comb2(n)
    tn = total_pairs - tp - fp - fn

    ri = (tp + tn) / total_pairs
    return ri

def adjusted_rand_index(contingency):
    # Helper function: n choose 2
    def comb2(x):
        return x * (x - 1) / 2.0

    n = contingency.sum()
    if n <= 1:
        return 0.0

    # Sum over all pairs in cells
    sum_comb_cells = np.sum(comb2(contingency))

    # Row and column sums
    row_sums = contingency.sum(axis=1)
    col_sums = contingency.sum(axis=0)

    sum_comb_rows = np.sum(comb2(row_sums))
    sum_comb_cols = np.sum(comb2(col_sums))

    total_pairs = comb2(n)

    expected_index = (sum_comb_rows * sum_comb_cols) / total_pairs
    max_index = 0.5 * (sum_comb_rows + sum_comb_cols)

    denominator = max_index - expected_index
    if denominator == 0:
        return 0.0

    ari = (sum_comb_cells - expected_index) / denominator
    return ari

def mutual_information(contingency):
    n = contingency.sum()
    if n == 0:
        return 0.0

    row_sums = contingency.sum(axis=1)
    col_sums = contingency.sum(axis=0)

    # Only consider nonzero entries
    nz = contingency > 0
    nij = contingency[nz]

    # Corresponding row and column sums
    i_idx, j_idx = np.nonzero(nz)
    ai = row_sums[i_idx]
    bj = col_sums[j_idx]

    # Compute MI
    mi = np.sum(
        (nij / n) * np.log((nij * n) / (ai * bj))
    )

    return mi

def all_clustering_dists(contingency,k_1,k_2,n):
    dists = {}
    dists["rand index"]=rand_index(contingency)
    dists["adjusted rand index"]=adjusted_rand_index(contingency)
    dists["mutual information"]=mutual_information(contingency)
    dists["split join"]=split_join(contingency,k_1,k_2,n)
    return dists
