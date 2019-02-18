test = open("./testInput.txt", "r")
output = open("./testOutput.txt", "w")
# n = input.readline()
for (i, line) in enumerate(test):
	if i == 0:
		n = line
	else:
		output.write("Case #" + str(i) + ": ")
		elements = line.split()
		holes = (int(elements[0])-1)*(int(elements[1])-1)
		output.write(str(holes) + "\n")

test.close()
output.close()

