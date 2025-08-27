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
Number of review over time
<img width="868" height="316" alt="image" src="https://github.com/user-attachments/assets/16cec57d-a8c1-4cd8-b7bf-1ae5158051ab" />

Histogram of rating distribution by provider

<img width="1189" height="396" alt="image" src="https://github.com/user-attachments/assets/69cef621-beb8-4776-95a4-2ee8a232e37e" />

Review trend over time by provider

<img width="1489" height="790" alt="image" src="https://github.com/user-attachments/assets/414c56f6-ff0a-40dd-aac6-049732263bbd" />

Early observation: Average ratings show a noticeable dip across providers from 2022–2024. A plausible hypothesis is a post-pandemic return to in-store visits that exposed service bottlenecks; this requires further validation with operational/context data.

Average rating by region by provider

<img width="1189" height="413" alt="image" src="https://github.com/user-attachments/assets/65a39b7f-cad6-4659-80c0-67dcb9c65dc6" />


