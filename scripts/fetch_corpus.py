"""Download the official documents listed in corpus/sources.csv.

PDFs are saved as they are; web pages are reduced to the text of their main content.
Usage: python scripts/fetch_corpus.py
"""

import csv
import html
import re
import urllib.request
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[1] / "corpus"
MAIN = re.compile(r"<article.*?</article>|<main.*?</main>", re.DOTALL)
NOISE = re.compile(r"^(Você está em:|Compartilhe:|Twitter|Facebook|Linkedin|WhatsApp|Área do conteúdo)")


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "corpus-fetcher"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def page_text(page: str) -> str:
    found = MAIN.search(page)
    body = found.group(0) if found else page
    body = re.sub(r"<(script|style).*?</\1>", "", body, flags=re.DOTALL)
    body = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>|</tr>", "\n", body)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line and not NOISE.match(line))


def main() -> None:
    with open(CORPUS / "sources.csv", newline="") as sources:
        for source in csv.DictReader(sources):
            target = CORPUS / source["file"]
            content = download(source["url"])
            if target.suffix == ".txt":
                target.write_text(page_text(content.decode("utf-8")) + "\n")
            else:
                target.write_bytes(content)
            print(f"{source['doc_id']}: {target.stat().st_size} bytes")


if __name__ == "__main__":
    main()
