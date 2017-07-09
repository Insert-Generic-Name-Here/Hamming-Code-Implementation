import error_addition
from sage.all import *
from random import randint


lst = [0,0,0,0]
words = []
errwords = []
w = 2

for i in range (20):
	tmp = []
	for i in range (4):
		tmp.append(randint(0,1))
	vector(tmp)
	words.append(tmp)

c = codes.HammingCode(GF(2),3)

for vec in words:
	c.encode(vec,'Systematic')
	error_addition.adderror(vector(vec),randint(0,2))
	errwords.append(vec)

print words, errwords




