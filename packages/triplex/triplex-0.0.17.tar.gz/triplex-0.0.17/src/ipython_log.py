# IPython log file

import textacy
# Load spacy model
nlp = spacy.load('en_core_web_sm')
# Plain text
text = "Barrack Obama was born in Hawaii in the year 1961. He was president of the United States."
# Process plain text with spacy
doc = nlp(text)
import spacy
# Load spacy model
nlp = spacy.load('en_core_web_sm')
# Plain text
text = "Barrack Obama was born in Hawaii in the year 1961. He was president of the United States."
# Process plain text with spacy
doc = nlp(text)
# Extract SVO list from spacy object
triples = list(textacy.extract.subject_verb_object_triples(doc))
print(triples)
triples
len(triples)
doc
type(doc)
def extract_relations(doc):

    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    
    triples = []
        
    for ent in doc.ents:
        preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
        for prep in preps:
            for child in prep.children:
                triples.append((ent.text, "{} {}".format(ent.root.head, prep), child.text))
            
    
    return triples
    
extract_relations(doc)
def extract_relations(doc):

    spans = list(doc.ents) + list(doc.noun_chunks)
#    for span in spans:
#        span.merge()
    
    triples = []
        
    for ent in doc.ents:
        preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
        for prep in preps:
            for child in prep.children:
                triples.append((ent.text, "{} {}".format(ent.root.head, prep), child.text))
            
    
    return triples
    
extract_relations(doc)
nlp = spacy.load("en_core_web_sm")
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from spacy import displacy 
text = "GDP in developing countries such as Vietnam will continue growing at a high rate." 

# create a spaCy object 
doc = nlp(text)
for tok in doc: 
  print(tok.text, "-->",tok.dep_,"-->", tok.pos_)
  
get_ipython().run_line_magic('logstart', '')
pattern = [{'POS':'NOUN'}, 
           {'LOWER': 'such'}, 
           {'LOWER': 'as'}, 
           {'POS': 'PROPN'}]

           
           
matcher = Matcher(nlp.vocab) 
matcher.add("matching_1", None, pattern) 

matches = matcher(doc) 
span = doc[matches[0][1]:matches[0][2]] 

print(span.text)
text
get_ipython().run_line_magic('clear', '')
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sentences:
    try:
        if len(s.entities) < 2:
            continue
    except ValueError:
        continue

    if DEBUG == 1:
        print s
        print
        print s.entities
        print

    for i in range(len(s.entities)):
        if i + 1 == len(s.entities):
            break

        e1 = s.entities[i]
        e2 = s.entities[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        if DEBUG == 1:
            print entity1, '\t', entity2
            print s.pos_tags[e1.end:e2.start]
            print
        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sentences:
    try:
        if len(s.entities) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(s.entities)):
        if i + 1 == len(s.entities):
            break

        e1 = s.entities[i]
        e2 = s.entities[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        if DEBUG == 1:
            print entity1, '\t', entity2
            print s.pos_tags[e1.end:e2.start]
            print
        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sentences:
    try:
        if len(s.entities) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(s.entities)):
        if i + 1 == len(s.entities):
            break

        e1 = s.entities[i]
        e2 = s.entities[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
import nltk
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sentences:
    try:
        if len(s.entities) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(s.entities)):
        if i + 1 == len(s.entities):
            break

        e1 = s.entities[i]
        e2 = s.entities[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
                
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sents:
    try:
        if len(s.entities) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(s.entities)):
        if i + 1 == len(s.entities):
            break

        e1 = s.entities[i]
        e2 = s.entities[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
text.sents[0]
list(text.sents)[0]
list(text.sents)[0].ents
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sents:
    try:
        if len(s.ents) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(s.ents)):
        if i + 1 == len(s.ents):
            break

        e1 = s.ents[i]
        e2 = s.ents[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
triples
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sents:
    try:
        if len(list(s.ents)) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(list(s.ents))):
        if i + 1 == len(list(s.ents)):
            break

        e1 = list(s.ents)[i]
        e2 = list(s.ents)[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
triples
verb = "<ADV>*<AUX>*<VERB><PART>*<ADV>*"
word = "<NOUN|ADJ|ADV|DET|ADP>"
preposition = "<ADP|ADJ>"

rel_pattern = "( %s (%s* (%s)+ )? )+ " % (verb, word, preposition)
grammar_long = '''REL_PHRASE: {%s}''' % rel_pattern
reverb_pattern = nltk.RegexpParser(grammar_long)
nlp = spacy.load("en_core_web_sm")
text = nlp("GDP in developing countries such as Vietnam will continue growing at a high rate.")
triples = []

for s in text.sents:
    try:
        print(list(s.ents))
        if len(list(s.ents)) < 2:
            continue
    except ValueError:
        continue

    for i in range(len(list(s.ents))):
        if i + 1 == len(list(s.ents)):
            break

        e1 = list(s.ents)[i]
        e2 = list(s.ents)[i + 1]
        entity1 = " ".join(e1)
        entity2 = " ".join(e2)

        if entity1.encode("utf8") in ignore_entities \
                or entity2.encode("utf8") in ignore_entities:
            continue

        if entity1.islower() or entity1.islower():
            continue

        context = s.words[e1.end:e2.start]
        if len(context) > 8 or len(context) == 0:
            continue

        rel = reverb_pattern.parse(s.pos_tags[e1.end:e2.start])
        for x in rel:
            if isinstance(x, nltk.Tree) and x.label() == 'REL_PHRASE':
                rel_phrase = " ".join([t[0] for t in x.leaves()])
                triple = Triple(entity1, e1.tag, rel_phrase, entity2, e2.tag)
                triples.append(triple)
import requests, json, pandas, numpy, os, copy, random, time
entities = list()
text
type(text)
text = "GDP in developing countries such as Vietnam will continue growing at a high rate."
inputs = {'model': model, 
             'text': text,
             'entities': list()}
model = "gpt-4-0613"
inputs = {'model': model, 
             'text': text,
             'entities': list()}
df = pandas.DataFrame([])
tic = time.time()
        response = requests.post(server_url, json=inputs).json()
        toc = time.time()
        if 'triplets' in response:
            df = pandas.DataFrame(response['triplets'])
        logger.info('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
tic = time.time()
response = requests.post(server_url, json=inputs).json()
toc = time.time()
if 'triplets' in response:
    df = pandas.DataFrame(response['triplets'])
logger.info('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
text
get_ipython().run_line_magic('clear', '')
_url='http://165.1.75.234'
#_url = 'http://localhost'
server_url=f"{_url}:5011/text"
model = "gpt-4-0613"
text = "GDP in developing countries such as Vietnam will continue growing at a high rate."
inputs = {'model': model, 
             'text': text,
             'entities': list()}


tic = time.time()
response = requests.post(server_url, json=inputs).json()
toc = time.time()
if 'triplets' in response:
    df = pandas.DataFrame(response['triplets'])
logger.info('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
get_ipython().run_line_magic('clear', '')
import gradio as gr
import requests, json, pandas, numpy, os, copy, random, time
import logging
logging.basicConfig(level=logging.INFO)

_url='http://165.1.75.234'
#_url = 'http://localhost'
server_url=f"{_url}:5011/text"
model = "gpt-4-0613"
text = "GDP in developing countries such as Vietnam will continue growing at a high rate."
inputs = {'model': model,
             'text': text,
             'entities': list()}


tic = time.time()
response = requests.post(server_url, json=inputs).json()
toc = time.time()
if 'triplets' in response:
    df = pandas.DataFrame(response['triplets'])
logger.info('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
import requests, json, pandas, numpy, os, copy, random, time
import logging
logging.basicConfig(level=logging.INFO)

_url='http://165.1.75.234'
#_url = 'http://localhost'
server_url=f"{_url}:5011/text"
model = "gpt-4-0613"
text = "GDP in developing countries such as Vietnam will continue growing at a high rate."
inputs = {'model': model,
             'text': text,
             'entities': list()}


tic = time.time()
response = requests.post(server_url, json=inputs).json()
toc = time.time()
if 'triplets' in response:
    df = pandas.DataFrame(response['triplets'])
logger.info('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
import requests, json, pandas, numpy, os, copy, random, time
import logging
logging.basicConfig(level=logging.INFO)

_url='http://165.1.75.234'
#_url = 'http://localhost'
server_url=f"{_url}:5011/text"
model = "gpt-4-0613"
text = "GDP in developing countries such as Vietnam will continue growing at a high rate."
inputs = {'model': model,
             'text': text,
             'entities': list()}


tic = time.time()
response = requests.post(server_url, json=inputs).json()
toc = time.time()
if 'triplets' in response:
    df = pandas.DataFrame(response['triplets'])
print('\033[94m' + f"\n Model: {model} Extracted {len(df)} triples, Elapsed time: {round(toc-tic, 3)} second " + '\033[0m')
df
response
response["triples"]
response["triplets"]
for _, row in df.iterrows():
    print(row["subject"])
    
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
explainer = TripleX(model, parser="remote")
from triplex.triplex import TripleX
explainer = TripleX(model, parser="remote")
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
model = 'microsoft/deberta-base'
model = AutoModel.from_pretrained(model, output_attentions=True)
from transformers import AutoModel
import logzero
model = 'microsoft/deberta-base'
model = AutoModel.from_pretrained(model, output_attentions=True)
explainer = TripleX(model, parser="remote")
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
import nltk
nltk.download("stopwords")
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
nltk.download("wordnet")
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
nltk.download("punkt")
premise = 'Dana Reeve, the widow of the actor Christopher Reeve, has died of lung cancer at age 44, according to the Christopher Reeve Foundation.'
hypothesis = 'Christopher Reeve had an accident.'
dfas, counterfactual_dfas = explainer.extract(premise, hypothesis,
                                              depth=2,
                                              max_perturbations_per_token=3)
dfas
counterfactual_dfas
