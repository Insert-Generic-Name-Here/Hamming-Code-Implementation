from random import randint

def makeWords(q, dim):
    word = [randint(0, q) for i in range(dim)]
    return word
    
    
def makeNoise(word):
    weight = randint(0, 1) # can also be changed
    err = []
    while len(err) < weight:
        e = randint(0,len(word)-1)
        if e not in err:
            err.append(e)
    for index in err:
        word[index] = 1 - word[index]
    #print weight, err, word
    return word