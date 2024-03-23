from collections import deque

import networkx as nx
import heapq

from pygraphviz import AGraph

MAX_DIST = float('inf')


def dijkstra(graph, source):
    distances = {node: MAX_DIST for node in graph}
    routes = {}
    heap = [(0, source)]  # (distance, node)
    distances[source] = 0

    while heap:
        curr_dist, curr_node = heapq.heappop(heap)

        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph[curr_node]:
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                routes[neighbor] = curr_node
                heapq.heappush(heap, (new_dist, neighbor))

    return distances, routes


def print_routes(end_points):
    print(f'Shortest distances from node {source}:')
    for node, dist in distances.items():
        if node in end_points:
            print(f"Node {node} total cost = {dist if dist != MAX_DIST else 'Unreachable'}")
            print('Route: ', end='')
            route = deque()
            src = node
            # print(src, end='')
            while True:
                route.appendleft(src)  # Add each step to the list
                if src == source:
                    break
                src = routes[src]

            string_route = ' -> '.join(str(node) for node in route)
            print(string_route, end='\n\n')


def draw(graph):
    g = nx.DiGraph()
    g.add_weighted_edges_from([(node, neighbor, weight) for node, neighbors in graph.items()
                               for neighbor, weight in neighbors])
    a: AGraph = nx.nx_agraph.to_agraph(g)
    for u, v, data in g.edges(data=True):
        a.get_edge(u, v).attr['label'] = str(data['weight'])
    for engine in {'neato', 'dot', 'circo', 'osage', 'fdp', 'patchwork', 'twopi', 'sfdp'}:
        print(f'using engine {engine}')
        a.layout(prog=engine)
        a.draw(f'my_graph_{engine}.png')


if __name__ == '__main__':
    # Exits ignored, they are the robbers goals, so they won't go to any other node from there
    graph = {
        1: [(2, 1), (17, 1), (10, 2)],
        2: [(3, 1), (21, 1)],
        3: [(2, 1), (4, 1), (8, 2)],
        4: [(3, 1), (5, 1), (22, 2)],
        5: [(4, 1), (7, 1), (6, 2), (22, 1)],
        6: [],
        7: [(6, 1), (5, 1), (8, 1)],
        8: [],
        9: [],
        10: [(9, 1), (11, 1), (18, 2)],
        11: [(10, 1), (17, 1), (12, 2)],
        12: [(11, 2), (13, 2), (16, 2), (17, 2)],
        13: [(12, 2), (14, 2), (16, 2), (17, 2), (21, 1)],
        14: [(13, 2), (15, 1), (20, 1), (16, 1)],
        15: [],
        16: [],
        17: [(11, 1), (16, 2), (18, 2)],
        18: [(10, 2), (17, 2), (19, 2)],
        19: [(9, 1), (18, 2)],
        20: [(14, 1), (21, 2), (22, 1)],
        21: [(2, 1), (13, 1), (20, 2), (22, 2)],
        22: []
    }

    # draw(graph)

    source = 1
    distances, routes = dijkstra(graph, source)

    escape_points = {6, 8, 9, 15, 16, 22}
    print_routes(escape_points)
