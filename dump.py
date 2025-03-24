import argparse
import asyncio
import re
import aiohttp
import aiofiles
import random
import shutil
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm.asyncio import tqdm, tqdm_asyncio
from pathlib import Path

USER_AGENT = "Mozilla/5.0"
HOST = "www.erome.com"
CHUNK_SIZE = 1024

def _clean_album_title(title: str, default_title="temp") -> str:
    """Remove illegal characters from the album title"""
    illegal_chars = r'[\\/:*?"<>|]'
    title = re.sub(illegal_chars, "_", title)
    title = title.strip(". ")
    return title if title else default_title

def _get_final_download_path(album_title: str, profile_name: str = None) -> Path:
    """Create a directory with the title of the album"""
    base_path = Path("downloads")
    if profile_name:
        base_path /= profile_name
    final_path = base_path / album_title
    if not final_path.exists():
        final_path.mkdir(parents=True)
    return final_path

async def dump(url: str, max_connections: int, skip_videos: bool, skip_images: bool, profile_name: str = None):
    """Collect album data and download the album"""
    if urlparse(url).hostname != HOST:
        raise ValueError(f"Host must be {HOST}")

    title, urls = await _collect_album_data(
        url=url, skip_videos=skip_videos, skip_images=skip_images
    )
    download_path = _get_final_download_path(album_title=title, profile_name=profile_name)

    await _download(
        album=url,
        urls=urls,
        max_connections=max_connections,
        download_path=download_path,
    )

    zip_path = shutil.make_archive(str(download_path), 'zip', str(download_path))
    tqdm.write(f"[*] Created zip file: {zip_path}")

    shutil.rmtree(download_path)
    tqdm.write(f"[*] Deleted folder: {download_path}")

    final_delay = random.randint(15, 25)
    tqdm.write(f"[*] Waiting {final_delay} seconds before finishing...")
    await asyncio.sleep(final_delay)

async def _download(
    album: str,
    urls: list[str],
    max_connections: int,
    download_path: Path,
):
    """Download the album"""
    semaphore = asyncio.Semaphore(max_connections)
    async with aiohttp.ClientSession(
        headers={"Referer": album, "User-Agent": USER_AGENT},
        timeout=ClientTimeout(total=None),
    ) as session:
        for url in urls:
            await _download_file(
                session=session,
                url=url,
                semaphore=semaphore,
                download_path=download_path,
            )
            delay = random.randint(1, 5)
            tqdm.write(f"[*] Waiting {delay} seconds before next download...")
            await asyncio.sleep(delay)

async def _download_file(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    download_path: Path,
):
    """Download the file"""
    async with semaphore:
        async with session.get(url) as r:
            if r.ok:
                file_name = Path(urlparse(url).path).name
                total_size_in_bytes = int(r.headers.get("content-length", 0))
                file_path = Path(download_path, file_name)

                if file_path.exists():
                    existing_file_size = file_path.stat().st_size
                    if abs(existing_file_size - total_size_in_bytes) <= 50:
                        tqdm.write(f"[#] Skipping {url} [already downloaded]")
                        return

                progress_bar = tqdm(
                    desc=f"[+] Downloading {url}",
                    total=total_size_in_bytes,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=CHUNK_SIZE,
                    colour="MAGENTA",
                    leave=False,
                )
                async with aiofiles.open(file_path, "wb") as f:
                    async for chunk in r.content.iter_chunked(CHUNK_SIZE):
                        written_size = await f.write(chunk)
                        progress_bar.update(written_size)
                progress_bar.close()
            else:
                tqdm.write(f"[ERROR] Failed to download {url}")

async def _collect_album_data(
    url: str, skip_videos: bool, skip_images: bool
) -> tuple[str, list[str]]:
    """Collect videos and images from the album with retry logic"""
    headers = {"User-Agent": USER_AGENT}
    retries = 5
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, "html.parser")
                    album_title = _clean_album_title(
                        soup.find("meta", property="og:title")["content"]
                    )
                    videos = (
                        [video_source["src"] for video_source in soup.find_all("source")]
                        if not skip_videos
                        else []
                    )
                    images = (
                        [
                            image["data-src"]
                            for image in soup.find_all("img", {"class": "img-back"})
                        ]
                        if not skip_images
                        else []
                    )
                    album_urls = list({*videos, *images})
                    return album_title, album_urls
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            tqdm.write(f"[ERROR] Attempt {attempt + 1}/{retries} failed: {e}")
            await asyncio.sleep(random.randint(5, 10))
    raise RuntimeError(f"[ERROR] Failed to fetch album data after {retries} attempts")

async def _get_albums_from_profile(profile_url: str) -> list[str]:
    """Extract all album URLs from a profile page."""
    headers = {"User-Agent": USER_AGENT}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(profile_url) as response:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
            album_links = [urljoin(profile_url, a['href']) for a in soup.find_all('a', href=True) if "/a/" in a['href']]
            return album_links

if __name__ == "__main__":
    choice = input("Choose an option (1,2, or 3):\n1. Enter the album link\n2. Enter the profile link\n3. Download all albums from url.txt\n")
    if choice == "1":
        url = input("Enter the album URL: ")
        asyncio.run(dump(url, max_connections=5, skip_videos=False, skip_images=False))
    elif choice == "2":
        profile_url = input("Enter the profile URL: ")
        album_urls = asyncio.run(_get_albums_from_profile(profile_url))
        with open("profile_url.txt", "w") as f:
            f.writelines(line + "\n" for line in album_urls)
        profile_name = urlparse(profile_url).path.strip('/')
        for url in album_urls:
            asyncio.run(dump(url, max_connections=5, skip_videos=False, skip_images=False, profile_name=profile_name))
    elif choice == "3":
        with open("url.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            asyncio.run(dump(url, max_connections=5, skip_videos=False, skip_images=False))
