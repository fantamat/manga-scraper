# Manga Scraper

A flexible Python-based manga scraper designed to download manga chapters from various sources. Currently supports Boruto manga series with an extensible architecture for adding more series like One Piece, Death Note, and others.

## Features

- 📚 Download complete manga chapters with all pages
- 🗂️ Organized file structure by series and chapters
- 🔧 Modular design for easy extension to new manga sources
- 📝 Automatic naming and numbering of downloaded pages
- 🎯 Parse manga metadata (series name, subtitle, chapter number)

## Currently Supported Manga

- **Boruto: Naruto Next Generations**
- **Boruto: Two Blue Vortex**

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fantamat/manga-scraper.git
cd manga-scraper
```

2. Install dependencies:
```bash
pip install -e .
```

Or install requirements manually:
```bash
pip install requests
```

## Usage

### Basic Usage

Run the scraper to download Boruto manga:

```bash
python test.py
```

This will:
1. Fetch the list of available Boruto chapters
2. Download all chapters to the `data/` directory
3. Organize files by series and chapter number

### Output Structure

Downloaded manga is organized as follows:
```
data/
├── Boruto_Naruto_Next_Generations/
│   ├── 001/
│   │   ├── Boruto_001_01.jpg
│   │   ├── Boruto_001_02.jpg
│   │   └── ...
│   ├── 002/
│   └── ...
└── Boruto_Two_Blue_Vortex/
    ├── 001/
    └── ...
```

## Project Structure

```
manga-scraper/
├── mangasc/                 # Main package
│   ├── __init__.py
│   ├── lists.py            # Functions to fetch manga lists
│   ├── utils.py            # Core utility functions
├── data/                   # Downloaded manga storage
├── test.py                 # Example usage script
├── pyproject.toml          # Project configuration
└── README.md
```

## Extending to New Manga Series

The project is designed to be easily extensible. Here's how to add support for new manga series:

### Step 1: Create a List Fetcher

Add a new function in `mangasc/lists.py` to fetch the manga list for your series:

```python
def get_onepiece_manga_list():
    """
    Fetch One Piece manga chapter list
    Returns: dict with {manga_name: manga_url}
    """
    response = requests.get("https://your-manga-site.com/")
    if response.status_code != 200:
        logging.error("Failed to retrieve manga list. Status code: %d", response.status_code)
        return {}
    
    # Parse the HTML to extract manga chapters
    pattern = re.compile(r'your-regex-pattern-here')
    find_patterns = re.findall(pattern, response.text)
    
    manga_list = {}
    # Extract URLs and names from matched patterns
    for item in find_patterns:
        # Your parsing logic here
        manga_list[manga_name] = manga_url
    
    return manga_list
```

### Step 2: Adapt Image Extraction (if needed)

If the target site uses a different HTML structure, modify `extract_image_urls()` in `mangasc/utils.py` or create a new variant:

```python
def extract_image_urls_onepiece(html_content):
    """Extract image URLs for One Piece manga site"""
    # Customize START_STR and END_STR for the target site
    return extract_image_urls(
        html_content,
        START_STR='<img src="',
        END_STR='"'
    )
```

### Step 3: Create a Download Script

Create a new script (e.g., `download_onepiece.py`):

```python
import os
import logging
from mangasc.utils import dowload_manga_chapter, parse_manga_name
from mangasc.lists import get_onepiece_manga_list

def main():
    manga_list = get_onepiece_manga_list()
    
    for manga_name, manga_url in manga_list.items():
        logging.info("Downloading: %s", manga_name)
        series_name, subtitle, chapter_number = parse_manga_name(manga_name)
        
        target_dir = os.path.join(".", "data", f"{series_name}_{subtitle.replace(' ', '_')}", f"{chapter_number:03d}")
        os.makedirs(target_dir, exist_ok=True)
        
        dowload_manga_chapter(manga_url, target_dir, series_name, chapter_number)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
```

### Step 4: Adapt Name Parser (if needed)

If your manga uses a different naming convention, modify `parse_manga_name()` in `mangasc/utils.py` or create a specialized version.

## API Reference

### Core Functions

#### `get_boruto_manga_list()`
Fetches the list of available Boruto manga chapters from the source website.

**Returns:** `dict` - Dictionary mapping manga names to URLs

#### `dowload_manga_chapter(url, target_dir, manga_name, chapter_number)`
Downloads a complete manga chapter.

**Parameters:**
- `url` (str): URL of the manga chapter
- `target_dir` (str): Directory to save downloaded images
- `manga_name` (str): Name of the manga series
- `chapter_number` (int): Chapter number for naming files

#### `parse_manga_name(manga_name)`
Parses manga name to extract series name, subtitle, and chapter number.

**Parameters:**
- `manga_name` (str): Full manga name (e.g., "Boruto: Naruto Next Generations, Chapter 1")

**Returns:** `tuple` - (series_name, subtitle, chapter_number)

#### `extract_image_urls(html_content, START_STR, END_STR)`
Extracts image URLs from HTML content.

**Parameters:**
- `html_content` (str): HTML content to parse
- `START_STR` (str): String marking the start of image URL
- `END_STR` (str): String marking the end of image URL

**Returns:** `list` - List of image URLs

## Contributing

Contributions are welcome! If you want to add support for new manga sources:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/add-onepiece`)
3. Implement the list fetcher and any necessary adaptations
4. Test thoroughly
5. Submit a pull request

## Roadmap

- [ ] Add support for One Piece
- [ ] Add support for Death Note
- [ ] Add support for Naruto
- [ ] Implement parallel downloading for faster performance
- [ ] Add progress bar for downloads
- [ ] Create CLI with argument parsing
- [ ] Add configuration file support
- [ ] Implement resume capability for interrupted downloads
- [ ] Add manga search functionality
- [ ] Create a simple GUI interface

## Requirements

- Python >= 3.13
- requests >= 2.32.5

## License

[Add your license here]

## Disclaimer

This tool is for educational purposes only. Please respect copyright laws and the terms of service of manga websites. Support official releases when possible.

## Troubleshooting

### Common Issues

**Issue:** Failed to retrieve manga list
- Check your internet connection
- Verify the source website is accessible
- The website structure may have changed (update regex patterns)

**Issue:** Images not downloading
- Check if the image URL extraction pattern is correct
- Some sites may have anti-scraping measures
- Try adding delays between requests

**Issue:** Incorrect chapter numbering
- Verify the manga name format matches expected pattern
- Adjust `parse_manga_name()` function if needed

## Contact

For questions or suggestions, please open an issue on GitHub.
