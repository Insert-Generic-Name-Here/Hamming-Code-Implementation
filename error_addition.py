from random import randint

weight = randint(0,2) # can also be changed

lst = [0,0,0,0] # example , will be changed
error = []

# if weight > len(lst):
# 	.... (what happens if lst is not big enough due to bad input)


while len(error)<weight:
	err = randint(0,len(lst)-1)
	if err not in error:
		error.append(err)

for index in error:
	lst[index] = 1 - lst[index]

print weight , error , lst