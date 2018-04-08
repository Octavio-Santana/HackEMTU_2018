from textblob import TextBlob
import json

out = []
with open('Report/data/stream__EMTU.json', 'r') as f:
    for line in f.read().split('\n')[:-1]:
        dic = json.loads(line)
        text = TextBlob(dic['text'])
        trad = TextBlob(str(text.translate(to='en')))
        print(trad)
        out.append(text + ';' + str(trad.sentiment.polarity))

with open('sentimentos.csv', 'w') as f:
    f.write('texto;nota\n')
    for line in out:
        f.write(str(line) + '\n')
