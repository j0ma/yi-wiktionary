import lxml.html as html
import cssselect
import requests
import string

ASCII_SET = set(string.ascii_letters)

def is_char_ascii(char):
    if char == '-':
        return True
    else:
        return char in ASCII_SET

def is_word_ascii(word):
    return all([is_char_ascii(c) for c in word])

def tree_from_url(url):
    page = requests.get(url).content
    tree = html.fromstring(page)
    return tree

def fetch_links_to_words(list_page_url):
    tree = tree_from_url(list_page_url)
    link_css_tag = 'div.mw-category-group > ul > li > a'
    a_elements = tree.cssselect(link_css_tag)
    hrefs = [a.attrib['href'] for a in a_elements]
    full_urls = ['https://en.wiktionary.org{}#Yiddish'.format(href) for href in hrefs]
    return full_urls

def fetch_transliteration(word_page_url):
    tree = tree_from_url(word_page_url)
    heb_css_tag = 'div.mw-parser-output > p > strong.headword'
    translit_css_tag = 'div.mw-parser-output > p > span.headword-tr'
    heb_word = tree.cssselect(heb_css_tag)[0].text
    transliteration = tree.cssselect(translit_css_tag)[0].text
    return {'yiddish': heb_word, 'transliteration': transliteration}
