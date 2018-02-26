from gensim.models import word2vec
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

fp = codecs.open("global.txt", "r", encoding="utf-8")
text = ""
while True:
    line = fp.readline()
    text = text+line
    if not line: break

fp.close()

twitter = Twitter()
results = []
lines = text.split("\n")

for line in lines:
    malist = twitter.pos(line, norm=True, stem=True)
    r = []
    for word in malist:
        if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            r.append(word[0])
    rl = (" ".join(r).strip())
    results.append(rl)

wakati_file = 'global.wakati'
with open(wakati_file, 'w', encoding="utf-8") as fp:
    fp.write("\n".join(results))

data = word2vec.LineSentence(wakati_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
#model.save("whole.model")
print("ok")