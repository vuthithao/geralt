from util import get_model, get_index_to_id
import numpy as np
import gensim.similarities

from mapper import Mungen,MuhExKillEl
mongo = Mungen()
mysql = MuhExKillEl()

it_id = 2228

query_res = mongo.get_token(it_id)
index_to_id = get_index_to_id()

model, dictionary, corpus, index = get_model()

#
doc = query_res['token']
vec_bow = dictionary.doc2bow(doc)
vec_lda = model[vec_bow]

sims = index[vec_lda]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

result = sims[:20]
res = []
result_corpus = []
for sim in sims[:20]:
    if str(sim[0]) == str(it_id):
        continue
    res.append((index_to_id[sim[0]],round(sim[1], 2)))
    result_corpus.append(corpus[sim[0]])


corpus_trend = gensim.corpora.MmCorpus('/home/topica/PycharmProjects/Recomend_API/corpus_trend.mm')
index_trend = gensim.similarities.MatrixSimilarity.load('/home/topica/PycharmProjects/Recomend_API/index_trend.index')


sims_trend = index_trend[vec_lda]
sims_trend = sorted(enumerate(sims_trend), key=lambda item: -item[1])

result_trend = sims_trend[:50]

result_trend_corpus = []
for sim in sims_trend:
    # print(corpus_trend[sim[0]])
    result_trend_corpus.append(corpus_trend[sim[0]])

dists = []
all_sum_sim = []
for i in range(len(result_corpus)):
    dist =[]
    sum_sim = 0
    for j in range(len(result_trend_corpus)):
        sim_sim= gensim.matutils.cossim(model[result_corpus[i]], model[result_trend_corpus[j]])
        dist.append(sim_sim)
        sum_sim += sim_sim
    dists.append(dist)
    all_sum_sim.append(sum_sim)

sort_index = np.argsort(all_sum_sim)
sort_index = sort_index[::-1]
sort_trend = []
for i in range(len(sort_index)):
    sort_trend.append(res[sort_index[i]])
print(all_sum_sim)
print(sort_trend)





