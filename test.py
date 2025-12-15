import requests
import logging
import os



def extract_image_urls(html_content):
    START_STR = '<div class="separator"><a class="hoverZoomLink" href="'
    END_STR = '"'
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


def dowload_manga_chapter(manga_name, chapter_number, target_dir):
    urls = f"https://w15.read-borutomanga.com/manga/{manga_name}-chapter-{chapter_number}/"
    response = requests.get(urls)
    if response.status_code != 200:
        logging.error("Failed to retrieve data. Status code: %d", response.status_code)
        return
    html_content = response.text
    image_urls = extract_image_urls(html_content)

    for i, image_url in enumerate(image_urls):
        dowload_image(image_url, os.path.join(target_dir, f"{manga_name}_{chapter_number:03d}_{i+1:02d}.jpg"))


def main():
    target_dir = os.path.join(".", "data", "boruto", "92")
    os.makedirs(target_dir, exist_ok=True)

    dowload_manga_chapter("boruto", 92, target_dir)



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    main()

