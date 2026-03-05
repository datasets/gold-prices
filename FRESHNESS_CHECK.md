# FRESHNESS CHECK — gold-prices

- **Repo:** `gold-prices`
- **Checked on:** `2026-03-03`

---

## 1. Repository Structure

Files found:

| File | Path |
|------|------|
| README | `README.md` |
| Data Package | `datapackage.json` |
| Process Script | `scripts/process.py` |
| Requirements | `scripts/requirements.txt` |
| Local Data (monthly) | `data/monthly.csv` |
| Local Data (annual) | `data/annual.csv` |
| Cached XLS (monthly) | `cache/monthly.xls` |
| Cached XLS (annual) | `cache/annual.xls` |
| Cached PDF | `cache/historical_gold_prices.pdf` |

---

## 2. Dataset Description

**Gold Prices** — Monthly and annual gold prices in USD since 1833.

Data is sourced from two upstream origins:
1. **Timothy Green's Historical Gold Price Table** (PDF) — covers 1833–1959. Hosted at `https://nma.org/wp-content/uploads/2016/09/historic_gold_prices_1833_pres.pdf`
2. **World Bank Commodity Markets ("Pink Sheet")** — covers 1960 to present. Main page: `https://www.worldbank.org/en/research/commodity-markets`

The `scripts/process.py` script:
- Scrapes the World Bank commodity markets page with BeautifulSoup to find the current XLS download links for monthly and annual prices
- Downloads `CMO-Historical-Data-Monthly.xlsx` and `CMO-Historical-Data-Annual.xlsx`
- Downloads the historical PDF from NMA
- Merges PDF data (pre-1960) with the World Bank data (1960+) into `data/monthly.csv` and `data/annual.csv`

---

## 3. Local Data — Latest Dates

Scanned `data/monthly.csv` (2,312 rows) and `data/annual.csv` (192 rows).

| File | Latest Date | Latest Price (USD) |
|------|-------------|-------------------|
| `data/monthly.csv` | **2025-07** | 3,340.15 |
| `data/annual.csv` | **2024** | 2,387.702 |

The monthly CSV is the higher-resolution dataset. Its latest entry is `2025-07` (July 2025).

---

## 4. Upstream Source Probing

### Step 4a — World Bank Commodity Markets Page

- **URL probed:** `https://www.worldbank.org/en/research/commodity-markets`
- **HTTP status:** 200 OK
- **Result:** Page loaded successfully. Parsed all `<a>` tags with BeautifulSoup.

Found active download links:
- **Monthly prices XLSX:** `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx`
- **Annual prices XLSX:** `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Annual.xlsx`
- **Pink Sheet PDF:** `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-February-2026.pdf`

The document ID `74e8be41ceb20fa0da750cda2f6b9e4e-0050012026` and the Pink Sheet PDF filename both indicate the **February 2026** release.

### Step 4b — Direct HEAD request on Monthly XLSX

- **URL:** `https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx`
- **HTTP status from HEAD:** 404 (CloudFront CDN quirk — the file requires a standard GET with a User-Agent)
- **HTTP status from GET with User-Agent:** 200 OK — downloaded successfully (779 KB `.xlsx` file)

### Step 4c — Parsing the Monthly XLSX

Downloaded and opened the XLSX with `openpyxl`. Sheet structure:
- `AFOSHEET` (metadata)
- `Monthly Prices` ← gold price data here
- `Monthly Indices`
- `Description`
- `Index Weights`

Key metadata from `Monthly Prices` sheet:
- **Row 3:** `"Updated on February 03, 2026"`
- **Row 4:** Column headers; Gold is at **column index 69**

Scanned all data rows (format `YYYYMNN`). Last 10 rows with Gold prices:

| Date (upstream) | Gold Price (USD/troy oz) |
|-----------------|--------------------------|
| 2025M04 | 3,217.64 |
| 2025M05 | 3,309.49 |
| 2025M06 | 3,352.66 |
| 2025M07 | 3,340.15 |
| 2025M08 | 3,368.03 |
| 2025M09 | 3,667.68 |
| 2025M10 | 4,058.33 |
| 2025M11 | 4,087.19 |
| 2025M12 | 4,309.23 |
| **2026M01** | **4,752.75** |

**Latest upstream date with gold data: January 2026 (2026-01)**

---

## 5. Comparison

| | Monthly CSV | Annual CSV | Upstream (World Bank) |
|-|-------------|------------|----------------------|
| **Latest date** | 2025-07 | 2024 | **2026-01** |
| **Gap** | 6 months behind | — | — |

The local monthly dataset is **6 months behind** the upstream World Bank data.

Missing months in local data: **2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01**

---

## 6. Verdict

**The dataset IS STALE.**

- Latest local date: `2025-07`
- Latest upstream date: `2026-01`
- Staleness: **6 months behind** (missing 6 monthly data points)
- The World Bank Pink Sheet was last updated on **February 3, 2026** and contains gold price data through **January 2026**.
- Running `python scripts/process.py` would refresh the data to the current upstream state.
