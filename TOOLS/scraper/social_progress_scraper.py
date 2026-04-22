#!/usr/bin/env python3
"""Scraper for Social Progress Index from statbase.org"""

import argparse
import csv
import json
import pathlib
from contextlib import suppress

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://statbase.org/datasets/indexes-and-ratings/social-progress-index/"

AVAILABLE_YEARS = [
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024,
]


def scrape_social_progress_index(year=2024):
    """Scrape the Social Progress Index table from statbase.org.

    Args:
        year: The year of data to scrape (default: 2024).
              Use 'last' for the last available year.

    Returns:
        List of dicts with 'rank', 'country', and 'score' keys.
    """
    url = BASE_URL
    year_str = str(year)

    if year_str != "last" and int(year) not in AVAILABLE_YEARS:
        raise ValueError(f"Invalid year. Choose from: {AVAILABLE_YEARS + ['last']}")

    params = {} if year_str == "last" else {"syear": year_str}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table_container = soup.find("div", class_="comp-content")
    if not table_container:
        print("Could not find table container")
        return []

    results = []
    for row in table_container.find_all("div", class_="it_row"):
        row_classes = row.get("class") or []
        if "col_row" in row_classes:
            continue

        cells = row.find_all("div", class_="it_cell")
        if len(cells) < 4:
            continue

        country_link = cells[0].find("a")
        country_name = country_link.get_text(strip=True).strip() if country_link else ""

        score_link = cells[2].find("a")
        score = score_link.get_text(strip=True).strip() if score_link else ""

        rank_link = cells[3].find("a")
        rank = rank_link.get_text(strip=True).strip() if rank_link else ""

        if country_name and rank:
            with suppress(ValueError):
                results.append(
                    {
                        "rank": int(rank),
                        "country": country_name,
                        "score": float(score) if score else None,
                    }
                )

    results.sort(key=lambda x: x["rank"])
    return results


def save_to_csv(data, filename="social_progress_index.csv"):
    """Save scraped data to CSV file"""
    with pathlib.Path(filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "country", "score"])
        writer.writeheader()
        writer.writerows(data)


def save_to_json(data, filename="social_progress_index.json"):
    """Save scraped data to JSON file"""
    with pathlib.Path(filename).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Scrape Social Progress Index")
    parser.add_argument(
        "-y",
        "--year",
        default="2024",
        help="Year to scrape (default: 2024). Use 'last' for latest.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (default: social_progress_index_{year}.csv)",
    )
    parser.add_argument("--json", action="store_true", help="Also save as JSON")
    args = parser.parse_args()

    year = args.year
    print(f"Scraping Social Progress Index for {year}...")

    data = scrape_social_progress_index(year)
    print(f"Found {len(data)} countries")

    if not data:
        print("No data scraped")
        return

    output = args.output or f"social_progress_index_{year}.csv"
    save_to_csv(data, output)
    print(f"Saved to {output}")

    if args.json:
        json_output = output.replace(".csv", ".json")
        save_to_json(data, json_output)
        print(f"Saved to {json_output}")

    print("\nTop 10 countries:")
    for item in data[:10]:
        print(f"  {item['rank']}. {item['country']}: {item['score']}")


if __name__ == "__main__":
    main()
