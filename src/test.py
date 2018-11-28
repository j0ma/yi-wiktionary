from helpers import *
url = 'https://en.wiktionary.org/w/index.php?title=Category:Yiddish_nouns&pagefrom=%D7%A9%D7%98%D7%95%D7%93%D7%99%D7%A2#mw-pages'
hrefs = fetch_links_to_words(url)
print(hrefs)
