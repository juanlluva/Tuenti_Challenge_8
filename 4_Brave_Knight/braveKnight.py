import sys

def step(origen, destino):
    reach = []
    movimientos = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
    for mov in movimientos:
        possible = tuple(map(sum, zip(destino, mov)))
        if possible in openSquares:
            if possible == origen:
                return "YES"
            else:
                reach.append(possible)
    return reach


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


