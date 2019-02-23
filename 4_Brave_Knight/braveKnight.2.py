import sys
from collections import deque, namedtuple

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)

class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            # this piece of magic turns ([1,2], [3,4]) into [1, 2, 3, 4]
            # the set above makes it's elements unique.
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node 
        # and to infinity for other nodes.
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            # 3. Select the unvisited node with the smallest distance, 
            # it's current node now.
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])

            # 6. Stop, if the smallest distance 
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node 
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost

                # Compare the newly calculated distance to the assigned 
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited 
            # and remove it from the unvisited set.
            vertices.remove(current_vertex)

        path, current_vertex = deque(), dest
        if current_vertex in previous_vertices.keys():
            while previous_vertices[current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            if path:
                path.appendleft(current_vertex)
            return path
        else:
            return "IMPOSSIBLE"

def step(current):
    reach = []
    if current in superSquares:
        movimientos = [(2,4),(2,-4),(-2,4),(-2,-4),(4,2),(4,-2),(-4,2),(-4,-2)]
    else:
        movimientos = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    for mov in movimientos:
        possible = tuple(map(sum, zip(current, mov)))
        if possible in openSquares:
                reach.append(possible)
    return reach


if __name__ == '__main__':
    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')
    cases = int(fin.readline())

    for case in range(1, cases+1):

        (N,M)=fin.readline().rsplit()
        # print("Dimensiones: "+ N +"x"+ M)
        (N,M) = (int(N),int(M))
        arena = []
        for n in range(0,N):
            line = list(fin.readline().replace('\n', ''))
            arena.append(line)
            # print(arena[n])

        openSquares = []
        superSquares = []
        for n in range(N):
            for m in range(M):
                if arena[n][m] != '#' :
                    openSquares.append((n,m))
                if arena[n][m] == '*' :
                    superSquares.append((n,m))
                if arena[n][m] == 'S' :
                    origen = (n,m)
                if arena[n][m] == 'P' :
                    stop = (n,m)
                if arena[n][m] == 'D' :
                    destino = (n,m)
        # print(str(openSquares))
        # print(str(origen) + ", " + str(stop) + ", " + str(destino))

        graph = Graph([])

        for square in openSquares:
            reach = step(square)
            # print(reach)
            for rch in reach:
                graph.add_edge(square, rch, 1, False)
        
        path1 = graph.dijkstra(origen, stop)
        # print(path1)
        path2 = graph.dijkstra(stop, destino)
        # print(path2)
        if path1 != "IMPOSSIBLE" and path2 != "IMPOSSIBLE":
            n_saltos = len(path1) + len(path2) - 2
            fout.write(f'Case #{case}: {n_saltos}\n')
        else:
            fout.write(f'Case #{case}: IMPOSSIBLE\n')