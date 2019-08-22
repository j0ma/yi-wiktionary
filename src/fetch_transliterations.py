import helpers as h
import pandas as pd
import pickle
import sys

with open('../data/meta/word_urls', 'r') as f_in:
    word_urls = [url.strip() for url in f_in.readlines() if url.strip() != ""]

n = len(word_urls)
translit_dicts = []
for ix, url in enumerate(word_urls):
    print('{} / {}'.format(ix+1, n), url)
    result = h.fetch_transliteration(url)
    print(result)
    translit_dicts.append(result)

yiddish_words = [d['yiddish'] for d in translit_dicts]
translit_words = [d['transliteration'] for d in translit_dicts]


output_format = input('What is the output format? (csv, pickle, txt) > ')

if output_format == 'pickle':
    with open('../data/raw/wiktionary_transliterations.pkl', 'wb') as f_out:
        pickle.dump(translit_dicts, f_out)

elif output_format == 'txt':
    with open('../data/raw/wiktionary_transliterations.txt', 'a') as f_out:
        for yiddish_word, transliteration in zip(yiddish_words, translit_words):
            f_out.write('{}\t{}'.format(yiddish_word, transliteration))

else:
    out = pd.DataFrame()
    out['yiddish'] = yiddish_words
    out['transliteration'] = translit_words
    if output_format == 'csv':
        out.to_csv('../data/raw/wiktionary_transliterations.csv', index=False, encoding='utf-8')
    else:
        print(out)
        sys.exit(0)


