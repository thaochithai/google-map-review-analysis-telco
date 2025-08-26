# Google Map reviews analysis of major Belgian telecom providers
Analyze what customers say about Belgium’s four major telecom providers: Telenet, Proximus, Orange, and BASE; by collecting and exploring ~64,000 Google Maps reviews across their retail stores. This repository documents the full pipeline: store discovery, automated review collection, cleaning/enrichment, and analysis notebooks.

## Dataset Stats

## Data collection & cleaning

### 1. Store url collection
- **Method**: Google Maps queries for `"<provider> shop"`
- **Output**: Official store page URLs
- **Tool**: Instant Data Scraper Chrome extension

### 2. Automated review scraping
- **Tool**: Selenium
- **Process**: Visit store url pages → Open Reviews tab → Scroll-load all reviews
- **Data**: Ratings + reviews text content + shop location

### 3. Data Processing
- **Deduplication**: Remove duplicate reviews
- **Standardization**: Normalize provider/store names, unify date formats
- **Text Preprocessing**: Lowercasing, punctuation cleanup, optional NLP prep

## Exploratory Analysis

### Number of reviews & rating trends over time (by provider and region)
Early observation: Average ratings show a noticeable dip across providers from 2022–2024. A plausible hypothesis is a post-pandemic return to in-store visits that exposed service bottlenecks; this requires further validation with operational/context data.

<img width="1489" height="790" alt="image" src="https://github.com/user-attachments/assets/eb0de0ab-2007-4f98-a1d0-8b05f4f1c9e3" />


