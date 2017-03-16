from gensim.models.word2vec import Word2Vec

import sys
model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin',
                                      binary=True) #/Users/sanjanaagarwal/Desktop/
print (model)
vector = []


def odd(words):
    return model.doesnt_match(words)


if __name__ == '__main__':
    print ("The following program finds the odd word out!")
    print ("Enter an input of a few words. EXAMPLE: (breakfast cereal lunch dinner)")
    listOfWords = map(str, raw_input().split())
    print ("The odd word is: ")
    print (odd(listOfWords))
    # print(odd(['breakfast', 'cereal', 'lunch', 'dinner']))
