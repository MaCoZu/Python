#!/usr/bin/env python3
"""Scraper for Happy Planet Index from happyplanetindex.org"""

import argparse
import csv
import json
import pathlib
import re
from contextlib import suppress

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://happyplanetindex.org"

AVAILABLE_YEARS = [2019, 2021]


def parse_score_change(change_str):
    """Parse score change string like '+2.6' or '-7.6' or '—'."""
    if not change_str or change_str == "—" or change_str == "-":
        return None
    change_str = change_str.strip()
    with suppress(ValueError):
        return float(change_str)
    return None


def parse_wellbeing(value):
    """Parse wellbeing value like '7.1/10' to float 7.1."""
    if not value:
        return None
    match = re.search(r"([\d.]+)", value)
    if match:
        with suppress(ValueError):
            return float(match.group(1))
    return None


def parse_carbon_footprint(value):
    """Parse carbon footprint like '2.62 tCO2e' to float 2.62."""
    if not value:
        return None
    match = re.search(r"([\d.]+)", value)
    if match:
        with suppress(ValueError):
            return float(match.group(1))
    return None


def parse_life_expectancy(value):
    """Parse life expectancy like '70.4 years' to float 70.4."""
    if not value:
        return None
    match = re.search(r"([\d.]+)", value)
    if match:
        with suppress(ValueError):
            return float(match.group(1))
    return None


def scrape_happy_planet_index(year=2021):
    """Scrape the Happy Planet Index table from happyplanetindex.org.

    Args:
        year: The year of data to scrape (default: 2021).
             Use 2019 or 2021.

    Returns:
        List of dicts with 'rank', 'country', 'life_expectancy', 'wellbeing',
        'carbon_footprint', 'hpi_score', and 'change' keys.
    """
    if year not in AVAILABLE_YEARS:
        raise ValueError(f"Invalid year. Choose from: {AVAILABLE_YEARS}")

    url = f"{BASE_URL}/hpi/?show_all=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table_container = soup.find("div", class_="hpi__table")
    if not table_container:
        print("Could not find data table container")
        return []

    results = []

    rows = table_container.find_all("div", class_="hpi__row")

    for row in rows:
        row_classes = row.get("class") or []
        if "hpi__row--headers" in row_classes or "hpi__row--show-more" in row_classes:
            continue

        cells = row.find_all("div", class_="hpi__cell")
        if len(cells) < 6:
            continue

        rank_text = cells[0].get_text(strip=True)
        rank_match = re.search(r"(\d+)", rank_text)
        if not rank_match:
            continue
        rank = int(rank_match.group(1))

        country_link = cells[1].find("a")
        country_name = (
            country_link.get_text(strip=True) if country_link else cells[1].get_text(strip=True)
        )

        life_exp = parse_life_expectancy(cells[2].get_text(strip=True))
        wellbeing = parse_wellbeing(cells[3].get_text(strip=True))
        carbon = parse_carbon_footprint(cells[4].get_text(strip=True))

        hpi_cell_text = cells[5].get_text(strip=True)
        hpi_match = re.search(r"([\d.]+)", hpi_cell_text)
        hpi_score = float(hpi_match.group(1)) if hpi_match else None

        change_match = re.search(r"\(([+-]?[\d.]+)\)", hpi_cell_text)
        change = float(change_match.group(1)) if change_match else None

        if country_name and hpi_score is not None:
            results.append(
                {
                    "year": year,
                    "rank": rank,
                    "country": country_name,
                    "life_expectancy": life_exp,
                    "wellbeing": wellbeing,
                    "carbon_footprint": carbon,
                    "hpi_score": hpi_score,
                    "change": change,
                }
            )

    results.sort(key=lambda x: x["rank"])
    return results


def scrape_all_years():
    """Scrape data for all available years."""
    all_data = {}
    for year in AVAILABLE_YEARS:
        print(f"Scraping {year}...")
        data = scrape_happy_planet_index(year)
        if data:
            all_data[str(year)] = data
            print(f"  Found {len(data)} countries")
    return all_data


def save_to_csv(data, filename="happy_planet_index.csv"):
    """Save scraped data to CSV file"""
    if not data:
        return
    fieldnames = [
        "year",
        "rank",
        "country",
        "life_expectancy",
        "wellbeing",
        "carbon_footprint",
        "hpi_score",
        "change",
    ]
    with pathlib.Path(filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        if isinstance(data, dict):
            for year_data in data.values():
                writer.writerows(year_data)
        else:
            writer.writerows(data)


def save_to_json(data, filename="happy_planet_index.json"):
    """Save scraped data to JSON file"""
    with pathlib.Path(filename).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Scrape Happy Planet Index")
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=2021,
        choices=AVAILABLE_YEARS,
        help="Year to scrape (default: 2021)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scrape all available years",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (default: happy_planet_index_{year}.csv)",
    )
    parser.add_argument("--json", action="store_true", help="Also save as JSON")
    args = parser.parse_args()

    if args.all:
        data = scrape_all_years()
        output = args.output or "happy_planet_index_all.csv"
        save_to_csv(data, output)
        print(f"Saved to {output}")

        if args.json:
            json_output = (
                args.output.replace(".csv", ".json")
                if args.output
                else "happy_planet_index_all.json"
            )
            save_to_json(data, json_output)
            print(f"Saved to {json_output}")

        total = sum(len(v) for v in data.values())
        print(f"\nTotal: {total} records across {len(data)} years")
    else:
        year = args.year
        print(f"Scraping Happy Planet Index for {year}...")
        data = scrape_happy_planet_index(year)
        print(f"Found {len(data)} countries")

        if not data:
            print("No data scraped")
            return

        output = args.output or f"happy_planet_index_{year}.csv"
        save_to_csv(data, output)
        print(f"Saved to {output}")

        if args.json:
            json_output = output.replace(".csv", ".json")
            save_to_json(data, json_output)
            print(f"Saved to {json_output}")

        print("\nTop 10 countries:")
        for item in data[:10]:
            change_str = f" ({item['change']:+.1f})" if item.get("change") else ""
            print(f"  {item['rank']}. {item['country']}: {item['hpi_score']}{change_str}")


if __name__ == "__main__":
    main()
