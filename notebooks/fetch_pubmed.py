#!/usr/bin/env python3
"""Fetch PubMed records and export structured metadata to CSV."""

from __future__ import annotations

import argparse
import http.client
import re
import time
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from Bio import Entrez
from tqdm import tqdm

PUBMED_EFETCH_MAX = 10000
NOT_USEFUL_PUB_TYPES = {
    "Research Support, Non-U.S. Gov't",
    "Research Support, N.I.H., Extramural",
    "Research Support, U.S. Gov't, Non-P.H.S.",
    "Research Support, N.I.H., Extramural,Research Support, U.S. Gov't, Non-P.H.S.",
    "Research Support, N.I.H., Intramural",
    "Research Support, U.S. Gov't, P.H.S.",
}


@dataclass
class FetchWindow:
    start: date
    end: date
    count: int
    webenv: str
    query_key: str


def _fmt_date(d: date) -> str:
    return d.strftime("%Y/%m/%d")


def _fmt_date_compact(d: date) -> str:
    return d.strftime("%Y%m%d")


def _validate_year_range(
    start_year: Optional[int], end_year: Optional[int]
) -> Tuple[Optional[int], Optional[int]]:
    if start_year is None and end_year is None:
        return None, None
    if start_year is None:
        start_year = 1900
    if end_year is None:
        end_year = date.today().year
    if start_year > end_year:
        raise ValueError("start-year cannot be greater than end-year")
    if start_year < 1700 or end_year > 2100:
        raise ValueError("year values look invalid; use a range between 1700 and 2100")
    return start_year, end_year


def search_pubmed(
    term: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Tuple[int, str, str]:
    """Run PubMed esearch and return (total_count, webenv, query_key)."""
    kwargs: Dict = {"db": "pubmed", "term": term, "usehistory": "y", "retmax": 0}
    if start_date and end_date:
        kwargs.update(datetype="pdat", mindate=_fmt_date(start_date), maxdate=_fmt_date(end_date))

    handle = Entrez.esearch(**kwargs)
    result = Entrez.read(handle)
    handle.close()
    return int(result["Count"]), result["WebEnv"], result["QueryKey"]


def _build_fetch_windows(
    term: str, start_year: int, end_year: int, request_delay: float
) -> List[FetchWindow]:
    """Recursively split date range until each window is within the efetch limit."""
    stack = [(date(start_year, 1, 1), date(end_year, 12, 31))]
    windows: List[FetchWindow] = []

    while stack:
        start, end = stack.pop()
        count, webenv, query_key = search_pubmed(term, start, end)
        time.sleep(request_delay)

        if count == 0:
            continue

        if count <= PUBMED_EFETCH_MAX or start == end:
            if count > PUBMED_EFETCH_MAX:
                print(
                    f"Warning: single-day {_fmt_date(start)} has {count} records; "
                    f"capped at {PUBMED_EFETCH_MAX}."
                )
                count = PUBMED_EFETCH_MAX
            windows.append(FetchWindow(start, end, count, webenv, query_key))
            continue

        mid = start + timedelta(days=(end - start).days // 2)
        if mid >= end:
            windows.append(FetchWindow(start, end, PUBMED_EFETCH_MAX, webenv, query_key))
            continue

        stack.append((mid + timedelta(days=1), end))
        stack.append((start, mid))

    windows.sort(key=lambda w: w.start)
    return windows


def fetch_window_to_disk(
    window: FetchWindow,
    xml_dir: Path,
    batch_size: int,
    request_delay: float,
) -> List[Path]:
    """Download all chunks for a window to disk. Skips chunks already saved."""
    xml_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"{_fmt_date_compact(window.start)}_{_fmt_date_compact(window.end)}"
    chunk_files: List[Path] = []

    for retstart in tqdm(
        range(0, window.count, batch_size), desc=f"{prefix}", unit="chunk", leave=False
    ):
        chunk_path = xml_dir / f"{prefix}_{retstart:07d}.xml"
        chunk_files.append(chunk_path)

        if chunk_path.exists():
            continue  # resume: already downloaded

        for attempt in range(1, 5):
            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    retmode="xml",
                    query_key=window.query_key,
                    WebEnv=window.webenv,
                    retstart=retstart,
                    retmax=batch_size,
                )
                data = handle.read()
                handle.close()
                chunk_path.write_bytes(data)
                break
            except (http.client.IncompleteRead, Exception) as exc:
                if attempt == 4:
                    raise RuntimeError(f"Failed to fetch {chunk_path.name} after 4 attempts") from exc
                wait = 5 * attempt
                print(f"\nRetry {attempt}/3 for {chunk_path.name} after {wait}s ({exc})")
                time.sleep(wait)
        time.sleep(request_delay)

    return chunk_files


def parse_chunk_files(chunk_files: List[Path]) -> List[Dict]:
    """Parse saved XML chunk files into a list of row dicts."""
    rows = []
    for path in tqdm(chunk_files, desc="Parsing XML", unit="file"):
        handle = open(path, "rb")
        batch = Entrez.read(handle)
        handle.close()
        rows.extend(parse_article(a) for a in batch.get("PubmedArticle", []))
    return rows


def parse_article(article: Dict) -> Dict:
    """Parse one PubmedArticle record into a flat dict row."""
    mc = article.get("MedlineCitation", {})
    art = mc.get("Article", {})
    journal = art.get("Journal", {})
    medline_info = mc.get("MedlineJournalInfo", {})

    pub_date = journal.get("JournalIssue", {}).get("PubDate", {})
    raw_year = pub_date.get("Year") or pub_date.get("MedlineDate", "")[:4]
    published_year = int(raw_year) if raw_year and raw_year.isdigit() else None

    pubmed_year = None
    for entry in article.get("PubmedData", {}).get("History", []):
        if entry.attributes.get("PubStatus") == "pubmed":
            pubmed_year = int(entry["Year"])
            break

    abstract_parts = art.get("Abstract", {}).get("AbstractText", [])
    if not abstract_parts:
        for other in mc.get("OtherAbstract", []):
            other_parts = other.get("AbstractText", [])
            if other_parts:
                abstract_parts = other_parts
                break

    if isinstance(abstract_parts, str):
        abstract_text = re.sub(r"<[^>]+>", "", abstract_parts).strip() or None
    else:
        abstract_text = "\n".join(
            re.sub(r"<[^>]+>", "", str(p)).strip()
            for p in abstract_parts
            if re.sub(r"<[^>]+>", "", str(p)).strip()
        ) or None

    pub_types = [
        str(pt) for pt in art.get("PublicationTypeList", [])
        if str(pt) not in NOT_USEFUL_PUB_TYPES
    ]

    keywords = [
        str(kw)
        for kw_list in mc.get("KeywordList", [])
        for kw in kw_list
        if str(kw).strip()
    ]

    seen: set = set()
    affiliations = []
    for author in art.get("AuthorList", []):
        for aff_info in author.get("AffiliationInfo", []):
            aff = aff_info.get("Affiliation", "").strip()
            if aff and aff not in seen:
                seen.add(aff)
                affiliations.append(aff)

    return {
        "PMID": str(mc.get("PMID", "")),
        "Title": str(art.get("ArticleTitle", "")) or None,
        "ISOAbbreviation": journal.get("ISOAbbreviation") or None,
        "journal_title": journal.get("Title") or None,
        "Abstract": abstract_text,
        "Journalinfo_country": medline_info.get("Country") or None,
        "Published_year": published_year,
        "Keyword_list": ",".join(keywords) or None,
        "publication_type": ",".join(pub_types) or None,
        "medline_citation": mc.attributes.get("Status") if hasattr(mc, "attributes") else None,
        "pubmed_year": pubmed_year,
        "Affiliation": "\n".join(affiliations) or None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch PubMed articles and export to CSV")
    parser.add_argument("query", help="PubMed search term")
    parser.add_argument("--email", required=True, help="Email address (required by NCBI)")
    parser.add_argument("--csv-name", default="pubmed_results.csv", help="Output CSV filename")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: ../data/output/)")
    parser.add_argument("--batch-size", type=int, default=10000, help="Records per efetch request (max 10000)")
    parser.add_argument("--start-year", type=int, default=None, help="Publication start year (inclusive)")
    parser.add_argument("--end-year", type=int, default=None, help="Publication end year (inclusive)")
    parser.add_argument("--api-key", default=None, help="NCBI API key for higher rate limits")
    parser.add_argument(
        "--request-delay",
        type=float,
        default=None,
        help="Delay between requests in seconds (default: 0.34 without API key, 0.11 with)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.batch_size < 1 or args.batch_size > PUBMED_EFETCH_MAX:
        raise ValueError(f"batch-size must be between 1 and {PUBMED_EFETCH_MAX}")

    Entrez.email = args.email
    if args.api_key:
        Entrez.api_key = args.api_key
    Entrez.max_tries = 4
    Entrez.sleep_between_tries = 15

    request_delay = args.request_delay if args.request_delay is not None else (
        0.11 if args.api_key else 0.34
    )
    start_year, end_year = _validate_year_range(args.start_year, args.end_year)

    repo_root = Path(__file__).resolve().parents[1]
    out_dir = Path(args.output_dir) if args.output_dir else repo_root / "data" / "output"
    xml_dir = out_dir / "xml_chunks"
    csv_name = args.csv_name if args.csv_name.lower().endswith(".csv") else f"{args.csv_name}.csv"
    csv_path = out_dir / csv_name

    total_count, webenv, query_key = search_pubmed(
        args.query,
        date(start_year, 1, 1) if start_year else None,
        date(end_year, 12, 31) if end_year else None,
    )
    print(f"Total records from search: {total_count}")

    if total_count == 0:
        out_dir.mkdir(parents=True, exist_ok=True)
        pd.DataFrame().to_csv(csv_path, index=False)
        print(f"No records found. Wrote empty CSV: {csv_path}")
        return

    all_chunk_files: List[Path] = []

    if total_count > PUBMED_EFETCH_MAX and start_year and end_year:
        print("Total exceeds 10000; splitting into date windows.")
        windows = _build_fetch_windows(args.query, start_year, end_year, request_delay)
        print(f"Created {len(windows)} date windows for retrieval.")
        for idx, window in enumerate(windows, 1):
            print(
                f"Window {idx}/{len(windows)}: {_fmt_date(window.start)} to "
                f"{_fmt_date(window.end)} ({window.count} records)"
            )
            all_chunk_files.extend(
                fetch_window_to_disk(window, xml_dir, args.batch_size, request_delay)
            )
    else:
        fetch_count = min(total_count, PUBMED_EFETCH_MAX)
        if total_count > PUBMED_EFETCH_MAX:
            print(
                f"Warning: capped at {PUBMED_EFETCH_MAX} records. "
                "Use --start-year/--end-year to retrieve all results."
            )
        all_chunk_files.extend(
            fetch_window_to_disk(
                FetchWindow(
                    start=date(start_year, 1, 1) if start_year else date(1900, 1, 1),
                    end=date(end_year, 12, 31) if end_year else date.today(),
                    count=fetch_count,
                    webenv=webenv,
                    query_key=query_key,
                ),
                xml_dir,
                args.batch_size,
                request_delay,
            )
        )

    print(f"Parsing {len(all_chunk_files)} XML chunk files...")
    rows = parse_chunk_files(all_chunk_files)
    df = pd.DataFrame(rows)

    if "PMID" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["PMID"]).copy()
        if len(df) != before:
            print(f"Deduplicated by PMID: {before} -> {len(df)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Parsed article rows: {len(df)}")
    print(f"CSV saved: {csv_path}")
    print(f"XML chunks kept at: {xml_dir}  (safe to delete once CSV looks good)")


if __name__ == "__main__":
    main()
