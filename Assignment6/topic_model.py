from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding("ISO-8859-1")





def clean_data(data):
    stop_wrd = get_stop_words("en")
    stam = PorterStemmer()
    main = {}

    txts = []
    for key in data.keys():
        text = data[key].lower()
        text = text.split()
        text = [i for i in text if i not in stop_wrd]
        text = map(lambda x:stam.stem(x),text)
        txts.append(text) 
    datax = corpora.Dictionary(txts)
    corpx = [datax.doc2bow(text) for text in txts]
    lda_model = model(datax,corpx)
    predict(data.keys(),corpx,lda_model)
    
    return 0

def predict(keys,corpx,ldamodel):
    doc_lda = ldamodel[corpx]
    j = 0
    for i in doc_lda: 
        print "Election Candidate:",keys[j],":\t",i
        j += 1
def model(data,corp):
    ldamodel = gensim.models.ldamodel.LdaModel(corp, num_topics = 50, id2word = data, passes=200)
    y = ldamodel.print_topics(num_topics = 30,num_words = 30)
    tup = zip(*y)[1:]
    j = 0
    for i in tup[0]:
        dic = {}
        i = i.split("+")
        i = map(lambda x:x.split("*"),i)
        i = {v:k for k,v in i}
        j += 1
        print "Topic: ",j,"word distribution is: \t",i 
    return(ldamodel)
def read_data(file):
    data = pd.read_csv(file)
    dic_data = {k:g['Text'] for k,g in data.groupby('Speaker')}
    for i in dic_data.keys():
        dic_data[i] = ' '.join(list(dic_data[i]))
    return dic_data


def main():
    data = read_data(sys.argv[1])
    main = clean_data(data)
if __name__ == '__main__':main()
