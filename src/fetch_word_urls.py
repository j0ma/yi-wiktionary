import lxml.html as html
import helpers as h
import cssselect
import requests
import sys

# load urls
with open('../data/urls', 'r') as f_in:
    list_page_urls = [url.strip() for url in f_in.readlines()
                                  if url.strip() != ""]

# loop over list urls, fetch each link
word_urls = []
for url in list_page_urls:
    _urls = h.fetch_links_to_words(url)
    word_urls.extend(_urls)

# output
output = "\n".join(word_urls)
print(output)
save_or_not = input('save? > ')
if save_or_not == 'y':
    with open('../data/word_urls', 'a') as f_out:
        f_out.write("\n".join(word_urls))
else:
    sys.exit(0)

