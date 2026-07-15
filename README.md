# bina.az Scraper

A Python scraper that collects real estate listings from [bina.az](https://bina.az)'s homepage at regular intervals and exports the results to a CSV file.

## Features

- Scrapes listing cards from the bina.az homepage using `requests` and `BeautifulSoup`
- Extracts:
  - Price (`qiymet`) and payment period (e.g. `/ay`, `/gün`)
  - Number of rooms (`otaqlar`)
  - Area in m² (`sahe`)
  - Floor / total floors (`mertebe`)
  - District / area (`erazi`)
  - City (`sheher`)
  - Listing date and time (`gun ve vaxt`)
  - Timestamp of when the row was parsed (`parsed_at`)
- Runs on a configurable interval for a configurable duration, so it can capture new listings as they appear
- Deduplicates results and exports everything to `bina_data.csv`

## Requirements

- Python 3.8+
- Dependencies:
  ```
  requests
  beautifulsoup4
  lxml
  pandas
  ```

Install them with:

```bash
pip install requests beautifulsoup4 lxml pandas
```

## Usage

Run the script directly:

```bash
python scraper.py
```

By default, it will:
1. Fetch and parse the bina.az homepage every **5 seconds**
2. Run for a total of **2 minutes**
3. Save all collected (deduplicated) listings to `bina_data.csv`

### Configuration

You can adjust the scraping behavior by editing these variables in the script:

```python
duration = 2 * 60   # total run time in seconds
interval = 5         # delay between scraping iterations, in seconds
```

## Output

The script produces a CSV file (`bina_data.csv`) with the following columns:

| Column       | Description                              |
|--------------|-------------------------------------------|
| `qiymet`     | Price and payment period                  |
| `otaqlar`    | Number of rooms                           |
| `sahe`       | Area (m²)                                 |
| `mertebe`    | Floor / total floors                      |
| `erazi`      | District / neighborhood                   |
| `sheher`     | City                                       |
| `gun ve vaxt`| Listing day and time                       |
| `parsed_at`  | Timestamp when the row was scraped         |

## Notes

- The scraper relies on specific CSS class names from bina.az's current HTML structure. If the site's frontend changes, the class selectors in `parse_page()` will need to be updated accordingly.
- Since the homepage is scraped repeatedly, the same listings may appear across multiple iterations. Duplicates are removed via `drop_duplicates()` before saving.
- Please review and respect bina.az's [terms of service](https://bina.az) and `robots.txt` before running this scraper, and avoid setting the interval too low to prevent overloading their servers.

## Disclaimer

This project is intended for personal/educational data analysis purposes only. Scraped data should not be redistributed or used commercially without permission from bina.az.
