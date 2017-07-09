from random import randint

def adderror(lst , max_weight):
	error = []
	weight = randint(0,max_weight)

	if max_weight> len(lst):
		print "wrong input"
		return 0

	while len(error)<weight:
		err = randint(0,len(lst)-1)
		if err not in error:
			error.append(err)

	for index in error:
		lst[index] = str(1 - int(lst[index]))
	print weight , error , lst

	return lst 