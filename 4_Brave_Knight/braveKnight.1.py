import sys

class Square:
    def __init__(self, pos):
        self.pos = pos
        self.adjacent = {}
        # Set distance to infinity for all squares
        self.distance = sys.maxsize
        # Mark all nodes unvisited        
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def remove_neighbor(self, neighbor):
        if neighbor in self.adjacent.keys():
            if self.adjacent[neighbor]:
                self.adjacent.pop(neighbor)

    def get_connections(self):
        return self.adjacent.keys()
    
    def get_connections_pos(self):
        lst = []
        for s in self.adjacent:
            lst.append(s.pos)
        return lst


    def get_pos(self):
        return self.pos

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
    
    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True
    
    def __str__(self):
        return str(self.pos) + ' adjacent: ' + str([x.pos for x in self.adjacent])

    def __repr__(self):
        return str(self.pos)

class Graph:
    def __init__(self):
        self.sqr_dict = {}
        self.num_sqr = 0

    def __iter__(self):
        return iter(self.sqr_dict.values())

    def add_square(self, pos) :
        self.num_sqr +=1
        new_sqr = Square(pos)
        self.sqr_dict[pos] = new_sqr
        return new_sqr

    def get_square(self, k):
        if k in self.sqr_dict:
            return self.sqr_dict[k]
        else:
            return None
    
    def add_step(self, frm, to, cost = 0) :
        if frm not in self.sqr_dict:
            self.add_square(frm)
        if to not in self.sqr_dict:
            self.add_square(to)
        # DEBUG 
        # print('From:'+str(frm))
        # print('To:'+str(to))
        # aux = self.sqr_dict[frm].get_connections()
        # print(aux)
        # if len(a)>0:
        #     print( a[0].pos[0])
        # print(str(v) for v in self.sqr_dict[frm].get_connections())
        # print(str(to) not in self.sqr_dict[frm].get_connections())
        # print('\n')

        # a = self.sqr_dict[to].get_connections_pos()
        # print(a)

        # if frm in a:
        #     self.sqr_dict[to].remove_neighbor(self.sqr_dict[frm])

         
        self.sqr_dict[frm].add_neighbor(self.sqr_dict[to], cost)
        self.sqr_dict[to].add_neighbor(self.sqr_dict[frm], cost)

    def get_squares(self):
        return self.sqr_dict.keys()

    def set_previous(self, current):
        self.previous = current
    
    def get_previous(self, current):
        return self.previous

    
def shortest(s, path):
    ''' make shortest path from v.previous'''
    if s.previous:
        path.append(s.previous.get_pos())
        shortest(s.previous, path)
    return


import heapq

def dijkstra(aGraph, start):
    print('''Dijkstra's shortest path''')
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    # print(unvisited_queue)
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        heapq.heapify(unvisited_queue)
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for nxt in current.adjacent:
            # if visited, skip
            if nxt.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(nxt)

            if new_dist < nxt.get_distance():
                nxt.set_distance(new_dist)
                nxt.set_previous(current)
                print('updated : current = %s next = %s new_dist = %s' \
                        %(current.get_pos(), nxt.get_pos(), nxt.get_distance()))
            else:
                print('not updated : current = %s next = %s new_dist = %s' \
                        %(current.get_pos(), nxt.get_pos(), nxt.get_distance()))
        
        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


def step(current):
    reach = []
    movimientos = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    for mov in movimientos:
        possible = tuple(map(sum, zip(current, mov)))
        if possible in openSquares:
                reach.append(possible)
    return reach


if __name__ == '__main__':

    fin = open(sys.argv[1], 'r')

    (N,M)=fin.readline().rsplit()
    print("Dimensiones: "+ N +"x"+ M)
    (N,M) = (int(N),int(M))
    arena = []
    for n in range(0,N):
        line = list(fin.readline().replace('\n', ''))
        arena.append(line)
        print(arena[n])

    openSquares = []
    for n in range(N):
        for m in range(M):
            if arena[n][m] != '#' :
                openSquares.append((n,m))
            if arena[n][m] == 'S' :
                origen = (n,m)
            if arena[n][m] == 'P' :
                stop = (n,m)
            if arena[n][m] == 'D' :
                destino = (n,m)
    # print(str(openSquares))
    # print(str(origen) + ", " + str(stop) + ", " + str(destino))

    g = Graph()

    for square in openSquares:
        g.add_square(square)

        reach = step(square)
        for rch in reach:
            g.add_step(square, rch, 1)
            # g.add_step(rch, square, 1)

    for s in g:
        for t in s.get_connections():
            s_pos = s.get_pos()
            t_pos = t.get_pos()
            print('( %s , %s, %3d)'  % ( s_pos, t_pos, s.get_weight(t)))

    dijkstra(g, g.get_square(origen))

    target = g.get_square(stop)
    path = [target.get_pos()]
    shortest(target, path)
    print('The shortest path : %s' %(path[::-1]))


