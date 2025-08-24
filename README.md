# Google Map reviews analysis of major Belgian telecom providers
Analyze what customers say about Belgium’s four major telecom providers: Telenet, Proximus, Orange, and BASE; by collecting and exploring ~64,000 Google Maps reviews across their retail stores. This repository documents the full pipeline: store discovery, automated review collection, cleaning/enrichment, and analysis notebooks.

## Highlights
### Coverage: 305 stores nationwide
### Reviews: ~64,000 total; ~27,000 include text
### Time span: 2014 → present

## Data Collection (Scraping)

### Store discovery: Query Google Maps for “<provider> shop” to surface official store pages.
### URL scraping: Export store URLs (e.g., via the Instant Data Scraper Chrome extension) to create a shop list.
### Automated reviews collection: A Selenium-based crawler visits each store page, opens the Reviews tab, and scrolls to load reviews (ratings + text where available).


## Data Cleaning & Enrichment

### Deduplication & normalization: Remove duplicates, standardize provider/store names, unify date formats.
### Text preprocessing: Lowercasing, basic punctuation cleanup; optional stopword removal and lemmatization for NLP tasks.

## Exploratory Analysis

### Number of reviews & rating trends over time (by provider and region)
Early observation: Average ratings show a noticeable dip across providers from 2022–2024. A plausible hypothesis is a post-pandemic return to in-store visits that exposed service bottlenecks; this requires further validation with operational/context data.
<img width="1489" height="790" alt="image" src="https://github.com/user-attachments/assets/eb0de0ab-2007-4f98-a1d0-8b05f4f1c9e3" />

### Sentiment analysis
### Topic modelling with LDA
### N-gram frequency & word clouds for quick theme scanning

<img width="1521" height="790" alt="image" src="https://github.com/user-attachments/assets/c25eb6dc-28d0-4647-849f-92e4d1576d0e" />

<img width="1521" height="790" alt="image" src="https://github.com/user-attachments/assets/9117d1a3-b667-4c85-bbd9-2491883982d6" />



