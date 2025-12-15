import requests
import logging
import os


def extract_image_urls(
        html_content, 
        START_STR = '<div class="separator"><a class="hoverZoomLink" href="',
        END_STR = '"'
    ):

    idx = html_content.find(START_STR)
    image_urls = []
    while idx != -1:
        idx += len(START_STR)
        end_idx = html_content.find(END_STR, idx)
        image_url = html_content[idx:end_idx]
        image_urls.append(image_url)
        idx = html_content.find(START_STR, end_idx)
    return image_urls


def dowload_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        logging.info("Downloaded %s", filename)
    else:
        logging.error("Failed to download image from %s", image_url)


def dowload_manga_chapter(url, target_dir, manga_name="manga", chapter_number=1):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("Failed to retrieve data. Status code: %d", response.status_code)
        return
    html_content = response.text
    image_urls = extract_image_urls(html_content)

    for i, image_url in enumerate(image_urls):
        dowload_image(image_url, os.path.join(target_dir, f"{manga_name}_{chapter_number:03d}_{i+1:02d}.jpg"))


def parse_manga_name(manga_name):
    start_idx = 0
    end_idx = manga_name.find(":")
    series_name = manga_name[start_idx:end_idx].strip()

    start_idx = end_idx + 1
    end_idx = manga_name.find("Chapter", start_idx)
    subtitle = manga_name[start_idx:end_idx].strip()
    if subtitle.endswith(","):
        subtitle = subtitle[:-1].strip()

    start_idx = end_idx + len("Chapter")
    chapter_number = manga_name[start_idx:].strip() 
    try:
        chapter_number = int(chapter_number)
    except ValueError:
        chapter_number = 1

    return series_name, subtitle, chapter_number
