import argparse, time
from shutil import which

from xklb import utils
from xklb.utils import log, pipe_print


def get_inner_urls(url, markup, include=None, exclude=None):
    from urllib.parse import urlparse

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(markup, "html.parser")
    film_list = set()

    for a in soup.findAll("a", attrs={"href": True}):
        log.debug(a)

        href = a["href"].strip()
        if (len(href) > 1) and href[0] != "#":
            if any(s in href for s in (exclude or [])):
                log.debug("excluded: %s", href)
                continue

            up = urlparse(href)
            if not up.netloc:
                up = urlparse(url)
                href = up.scheme + "://" + up.netloc + href

            if include is None or len(include) == 0:
                film_list.add(href)
            elif all(s in href for s in include):
                log.debug("included: %s", href)
                film_list.add(href)
            else:
                log.debug("else: %s", href)

        # breakpoint()

    return film_list


def get_page_infinite_scroll(driver, url):
    driver.get(url)
    time.sleep(1)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver.page_source


def extract_links() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include", "-s", nargs="*", help="substrings for inclusion (all must match to include)")
    parser.add_argument(
        "--exclude",
        "-E",
        nargs="*",
        default=["javascript:", "mailto:", "tel:"],
        help="substrings for exclusion (any must match to exclude)",
    )
    parser.add_argument("--scroll", action="store_true", help="Scroll down the page; infinite scroll")
    parser.add_argument("--download", action="store_true", help="Download filtered links")
    parser.add_argument("--verbose", "-v", action="count", default=0)

    parser.add_argument("--file", "-f", help="File with one URL per line")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()

    if args.scroll:
        from selenium import webdriver

        if which("firefox"):
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Chrome()

    def process_url(line):
        url = line.rstrip("\n")
        if url in ["", '""', "\n"]:
            return

        if args.scroll:
            markup = get_page_infinite_scroll(driver, url)
        else:
            r = utils.requests_session().get(url, timeout=120, headers=utils.headers)
            r.raise_for_status()
            markup = r.content
        inner_urls = get_inner_urls(url, markup, include=args.include, exclude=args.exclude)

        if args.download:
            for inner_url in inner_urls:
                utils.download_url(inner_url)
        else:
            pipe_print("\n".join(inner_urls))

    if args.file:
        with open(args.file) as f:
            for line in f:
                process_url(line)
    else:
        for path in args.paths:
            process_url(path)

    if args.scroll:
        driver.quit()


if __name__ == "__main__":
    # echo $directors | python scripts/mining/nfb.ca.py | tee -a ~/.jobs/75
    extract_links()
