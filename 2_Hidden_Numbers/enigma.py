import sys

fin = open(sys.argv[1], 'r')
fout = open(sys.argv[2], 'w')
cases = int(fin.readline())

for case in range(1, cases+1):
    min = max = 0
    a = fin.readline()
    a = a.replace("\n", "")
    base = len(a)
    # print(a)
    # print(base)
    usableBase = base-1
    min += 1*(base**(base-1))
    for figure in range(0, base):
        max+= figure*(base**figure)
        # print(max)
        if figure<=(base-3):
            min += (usableBase)*(base**figure)
            usableBase-=1
    # print("Min: " + str(min) + ", Max: " + str(max))
    difference = max-min
    # print(str(difference))
    fout.write(f'Case #{case}: {difference}\n')
fout.close()