import os
import logging


from mangasc.utils import dowload_manga_chapter, parse_manga_name
from mangasc.lists import get_boruto_manga_list

def main():
    manga_list = get_boruto_manga_list()
    
    for manga_name, manga_url in manga_list.items():
        logging.info("Manga: %s, URL: %s", manga_name, manga_url)
        series_name, subtitle, chapter_number = parse_manga_name(manga_name)

        target_dir = os.path.join(".", "data", f"{series_name}_{subtitle.replace(' ', '_')}", f"{chapter_number:03d}")
        os.makedirs(target_dir, exist_ok=True)

        dowload_manga_chapter(manga_url, target_dir, series_name, chapter_number)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    main()

