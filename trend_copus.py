from nlp import markdown_to_text,remove_punctuation
from util import get_model,convert_to_token
import gensim.similarities

from mapper import Mungen,MuhExKillEl
mongo = Mungen()
mysql = MuhExKillEl()


import pandas as pd
data_trend = pd.read_pickle("/home/topica/workspace/all_data_8.pkl")

post_content = data_trend["article"].tolist()

model, dictionary, corpus, index = get_model()

tokens = []
for i in range(len(post_content)):
    text = markdown_to_text(post_content[i])
    text = remove_punctuation(text)
    token = convert_to_token(text)
    tokens.append(token)


corpus_trend = [dictionary.doc2bow(text) for text in tokens]

gensim.corpora.MmCorpus.serialize('corpus_trend.mm', corpus_trend)

index_trend = gensim.similarities.MatrixSimilarity(model[corpus_trend])
index_trend.save("index_trend.index")
