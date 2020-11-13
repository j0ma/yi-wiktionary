import helpers as h
import click
import sys
import os


@click.command()
@click.option(
    "--category_page_url",
    required=True,
    help="Category page URLs to construct word page URLs from",
    default="https://en.wiktionary.org/w/index.php?title=Category:Yiddish_lemmas",
)
@click.option(
    "--word_url_file",
    required=True,
    help="Text file to save word urls to",
    default=os.path.join("../data/meta", "word_urls"),
)
@click.option("--save", is_flag=True, default=False)
def scrape(category_page_url, word_url_file, save):

    # loop over list urls, fetch each link
    word_urls = []
    for url in h.fetch_all_page_urls(category_page_url):
        _urls = h.fetch_links_to_words(url)
        word_urls.extend(_urls)

    # output
    if save:
        print(f"Saving word urls under {word_url_file}")
        with open(word_url_file, "w") as f_out:
            f_out.write("\n".join(word_urls))


if __name__ == "__main__":
    scrape()
