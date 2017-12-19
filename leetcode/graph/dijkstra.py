#!/usr/bin/env python


import numpy as np
import pandas as pd


def find_short(adj_matrix, start_node):
    nodes = adj_matrix.index
    nodes_distance = pd.DataFrame({"dist": np.ones_like(nodes) * np.inf,
                                   "used": np.zeros_like(nodes)}, index=nodes)
    nodes_distance.loc[start_node] = [0, 0]
    while True:
        unused_nodes = nodes_distance[nodes_distance["used"] == 0]
        if unused_nodes.empty:
            break
        min_node = unused_nodes["dist"].argmin(axis=1)
        nodes_distance.loc[min_node, "used"] = 1

        neighbors = adj_matrix.loc[min_node]
        neighbors = neighbors[neighbors != 0]
        for to_node in neighbors.index:
            nodes_distance.loc[to_node, "dist"] = min(
                    nodes_distance.loc[to_node, "dist"],
                    nodes_distance.loc[min_node, "dist"] + adj_matrix.loc[min_node, to_node])

    return nodes_distance


def adj_edges2matrix(edges, nodes):
    if not edges or not nodes:
        return [[]]

    nodes_size = len(nodes)
    zeros = np.zeros((nodes_size, nodes_size))
    adj_matrix = pd.DataFrame(zeros, index=nodes, columns=nodes)

    for node, to_node, weight in edges:
        adj_matrix.loc[node, to_node] = weight

    return adj_matrix


if __name__ == "__main__":
    edges = [("s", "t", 10), ("s", "y", 5),
             ("t", "y", 2), ("t", "x", 1),
             ("x", "z", 4),
             ("z", "x", 6), ("z", "s", 7),
             ("y", "t", 3), ("y", "x", 9), ("y", "z", 2)]
    nodes = list("stxyz")
    adj_matrix = adj_edges2matrix(edges, nodes)
    print(adj_matrix)
    print("res:")
    print(find_short(adj_matrix, "s"))
