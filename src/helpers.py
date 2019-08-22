import lxml.html as html
import cssselect
import requests
import string
import pylev3

ASCII_SET = set(string.ascii_letters)

def is_char_ascii(char):
    if char == '-':
        return True
    else:
        return char in ASCII_SET

def is_word_ascii(word):
    return all([is_char_ascii(c) for c in word])

def levenshtein_distance(s1, s2):
    return (pylev3.Levenshtein
                  .classic(s1, s2))

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
    yi_word = [e.text_content() for e in tree.cssselect('strong.headword') if is_valid_yiddish(e)][0]
    transliteration = [e.text_content() for e in tree.cssselect('span.headword-tr') if is_valid_transliteration(e)][0]
    return {'yiddish': yi_word, 'transliteration': transliteration}

def is_valid_yiddish(elem):
    if 'lang' not in elem.attrib:
        return False
    else:
        return elem.attrib['lang'] == 'yi'

def is_valid_transliteration(elem):
    if 'lang' not in elem.attrib:
        return False
    else:
        return elem.attrib['lang'] == 'yi-Latn'
