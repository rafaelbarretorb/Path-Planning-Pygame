cond = True
cond2 = True
cond3 = False
count = 0

N = 10
i = 0
b = 3
j = 0
n = N
goal_found = False
while cond:
	print i
	print "n: " + str((n + j*b))
	if i == (n + j*b):
		j = j + 1
		print "Optimize"
		if i > 20:
			cond = False
	else:
		if not goal_found:
			print "search"
			if i == 4:
				goal_found = True
				n = i + 1

				print "n: " + str(n)
		else:
			print "compute path"
	
	i = i + 1

