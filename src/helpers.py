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

    #print(yi_in_title)

    # grab div in which words live
    #div_elems = [e for e in tree.cssselect('div.mw-parser-output')[0] if isinstance(e, html.HtmlElement)]

    # find yiddish index
    #text_contents = [e.text_content() for e in div_elems]
    #yi_ix = text_contents.index('Yiddish[edit]')

    # filter out everything before yiddish
    #filtered_div_elems = div_elems[yi_ix:]

    # find <p> after Yiddish header
    #p_elem = [e for e in filtered_div_elems if e.tag == 'p' and is_valid_yiddish(e.getchildren()[0])][0]
    #yi_word = [e.text_content() for e in p_elem.cssselect('strong') if is_valid_yiddish(e)][0]
    #transliteration = [e.text_content() for e in p_elem.cssselect('span') if is_valid_transliteration(e)][0]

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
