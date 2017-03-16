import xmltodict as xmd
import sys
import subprocess
import shlex
import pandas as pd
import re

def read_file(file):
	with open(file,'r') as f:
		return(xmd.parse(f.read()))

class node_word(object):
	def __init__(self,word,lemma,ner,pos,speaker):
		self.word = word
		self.lemma = lemma
		self.ner = ner
		self.pos = pos
		self.speaker = speaker

class node_sentence(object):
	def __init__(self,id,words):
		self.id = id
		self.words = words

def return_sentences(sentences):
	
	sentences = sentences['root']['document']['sentences']['sentence']
	i=1
	dic = {}
	for sentence in sentences:
		dic[i] = node_sentence(i,return_token_word(sentence))
		i+=1
	return(dic)	

def return_token_word(sentence):
	token_json = sentence['tokens']['token']
	words = {}
	j = 1
	for i in token_json:
		#import pdb;pdb.set_trace()
		words[j] = node_word(i['word'],i['lemma'],i['NER'],i['POS'],i['Speaker'] if 'Speaker' in i.keys() else 'None')
		j += 1
	return words

def parse_speaker(sentences):
	speakers = {}
	i = 1
	#import pdb;pdb.set_trace()
	for sentence in sentences:
		x = None ; y = None
		if "``"  in [v.pos for (k,v) in sentences[sentence].words.iteritems()]:
			#import pdb;pdb.set_trace()
			for k,v in sentences[sentence].words.iteritems():
				x,y = return_speaker(x,y,v)
		#speakers.append(map(lambda z:return_speaker(x,y,z), [v for k,v in sentences[sentence].words.iteritems()]))
			if all((x,y)):
				speakers[i] = (x,y)
		i += 1
	return speakers
def return_speaker(x,y,word_node):
	p = re.compile('PER\w')
	prp = ['i','me','him','you','us','he','it','we','they','yourself','myself','them']
	if p.findall(str(word_node.speaker)) and (word_node.ner == 'PERSON' or word_node.ner == 'MISC' or word_node.pos in prp):
		if x == None or x.lower() in prp: x = word_node.word
		elif y == None or y.lower() in prp: y = word_node.word
	return(x,y)

def main():
	subprocess.call(shlex.split('./corenlp.sh -annotators tokenize,ssplit,pos,lemma,parse,ner,depparse,dcoref\
			 -file '+sys.argv[1]+' -outputFormat xml'))
	i = read_file(sys.argv[1]+'.xml')
	i = return_sentences(i)
	i = parse_speaker(i)
	print(pd.DataFrame(i))
if __name__=='__main__':main()
