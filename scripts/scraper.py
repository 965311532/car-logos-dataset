import logging
from pathlib import Path
from typing import Union

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from config import Config as config

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _fix_url(url: Union[str, None], base_url: str = config.BASE_URL) -> str:
    """Fixes the URL"""
    if not url:
        raise ValueError("URL is empty")
    if not url.startswith(("http://", "https://", "www.")):
        if url.startswith("/"):
            return base_url + url
        return base_url + "/" + url
    return url


def get_makers_urls(session) -> list:
    """Returns the relative URLs of the makers"""
    # Get the makers list page
    page = session.get(config.MAKERS_LIST_URL)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, "html.parser")
    # Get the makers list
    return [_fix_url(link.get("href")) for link in soup.select(".a-z dd a")]  # type: ignore


def get_logo_url_from_maker_url(session, maker_url):
    """Returns the logo URL from a maker URL"""
    # Get the maker page
    page = session.get(maker_url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, "html.parser")
    # Get the logo URL
    img = soup.select_one(".logo-content img")
    try:
        if img and img.parent.get("href"):  # type: ignore
            return _fix_url(img.parent.get("href"))  # type: ignore
        else:
            return _fix_url(img.get("src"))  # type: ignore
    except AttributeError:
        return None


def download_logo(session, logo_url):
    """Downloads the logo"""
    # Create the folder if it doesn't exist
    raw_logo_folder = config.RAW_DIRPATH
    raw_logo_folder.mkdir(parents=True, exist_ok=True)
    # Get the logo
    logo = session.get(logo_url)
    # Save the logo
    raw_filename = filename = logo_url.split("/")[-1]
    extension = filename.split(".")[-1]
    filename = raw_filename.lower().split("-logo")[0] + "." + extension
    logo_file = raw_logo_folder / filename
    with open(logo_file, "wb") as f:
        f.write(logo.content)


def main():
    """Main function"""
    # Create a session
    session = requests.Session()
    session.headers = config.HEADERS  # type: ignore

    # Get the makers list
    makers_urls = get_makers_urls(session)
    # For each maker
    for maker_url in tqdm(makers_urls):
        # Get the logo URL
        logo_url = get_logo_url_from_maker_url(session, maker_url)
        # Download the logo
        download_logo(session, logo_url)


if __name__ == "__main__":
    main()
    exit(0)
