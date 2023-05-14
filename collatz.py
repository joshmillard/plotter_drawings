# Collatz conjecture tomfoolery

depth = 100  # how far into the integers to proceed

# The basic forward Collatz operation: if n is divisible by 2, the next value is n/2;
#  otherwise the next value is 3*n + 1
def collatz(currval):
	if currval % 2 == 0:
		return(int(currval/2))
	else:
		return(int(currval*3 + 1))

# structure A: full lists 
# generate a list of lists with each having a single element of an integer in rising order
chains = [[x+1] for x in range(depth)]

# for each initial one-element list, proceed with applying the Collatz operation, stopping when
# only when we reach a value of 1.  Which, if the conjecture is true, will always happen eventually.
# And if it's false, there's no way this will be the code that finds out, since it's been tested out to
# 2**68 or so already.
for i in range(depth):
	j = 0
	while(chains[i][j] != 1):
		chains[i].append( collatz(chains[i][j]) )
		j += 1

# structure B: associative array
# Create an associate array where key = currval, value = collatz(currval);
#  this creates a short circuit test where once any given chain of values from a starting n yields
#  a key that already exists in the table, we know it will proceed from there to 1 and so can stop
#  recalculating a known chain
pairs = {} 
for i in range(depth):
	if not i in pairs:
		pairs[i] = collatz(i)

print(pairs)


# calculations with the generated structures
# how many steps does it take each initial value to reach 1?
lengths = {}
for c in chains:
	if not len(c) in lengths:
		lengths[len(c)] = [c[0]]
	else:
		lengths[len(c)].append(c[0])

#print(lengths)
#print(sorted(lengths))