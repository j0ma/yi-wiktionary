import helpers as h
import pandas as pd
import pickle
import sys
import click
import os


@click.command()
@click.option(
    "--word_url_file",
    required=True,
    help="Text file to save word urls to",
    default=os.path.join("../data/meta", "word_urls"),
)
@click.option(
    "--output_format", default="pickle", help="Output format to use [pickle/txt/csv]"
)
@click.option(
    "--output_path",
    default="../data/raw/wiktionary_transliterations.pkl",
    help="File to save outputs to",
)
@click.option("--save", is_flag=True, default=False)
def scrape(word_url_file, output_format, output_path, save):
    with open(word_url_file, "r") as f_in:
        word_urls = [url.strip() for url in f_in.readlines() if url.strip() != ""]

    n = len(word_urls)
    translit_dicts = []
    for ix, url in enumerate(word_urls):
        print("{} / {}".format(ix + 1, n), url)
        try:
            result = h.fetch_transliteration(url)
            print(result)
            translit_dicts.append(result)
        except IndexError:
            print("Error, can't find anything meaningful! Skipping...")

    yiddish_words = [d["yiddish"] for d in translit_dicts]
    translit_words = [d["transliteration"] for d in translit_dicts]

    out = pd.DataFrame()
    out["yiddish"] = yiddish_words
    out["transliteration"] = translit_words

    if output_format == "pickle" and save:
        with open(output_path, "wb") as f_out:
            pickle.dump(translit_dicts, f_out)

    elif output_format == "txt" and save:
        with open(output_path, "w") as f_out:
            for yiddish_word, transliteration in zip(yiddish_words, translit_words):
                f_out.write("{}\t{}".format(yiddish_word, transliteration))

    else:
        if save:
            out.to_csv(
                output_path, index=False, encoding="utf-8",
            )
        else:
            print(out)
            sys.exit(0)

if __name__ == "__main__":
    scrape()
