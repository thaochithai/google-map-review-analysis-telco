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


#### Provider performance by regions
- Telenet shows consistently strong ratings across most Flemish regions, often scoring among the highest. They perform particularly well in West-Vlaanderen (3.98), Limburg (3.97), and Vlaams-Brabant (3.91). Their presence is indeed concentrated in Flanders, with no ratings shown for Walloon regions
- Proximus appears to have the most consistent coverage across all regions (both Flanders and Wallonia) and often leads in ratings, especially in Walloon areas like Brabant wallon (4.02) and Limburg (4.19)
- Orange shows strong performance in some areas like Vlaams-Brabant (3.92) and Oost-Vlaanderen (3.80)
- BASE has more limited coverage but performs well where available, particularly in Antwerpen (3.90)

The data confirms Telenet's strong position in the Flemish market with consistently high customer satisfaction ratings. Proximus appears to be the most comprehensive national provider, while Orange and BASE have more selective regional presence.

<img width="1189" height="413" alt="image" src="https://github.com/user-attachments/assets/374b6e12-caf9-4332-8cd5-a43a114ffb08" />


## Sentiment analysis

## Topic modelling with LDA
Using LDA, there are 6 common topic discovered. However, there is overlap: Topics 3, 6 all relate to service interactions; and topic 4 is too generic
- Topic 1: internet, month, day, week, subscription, pay, problem, tv
- Topic 2: long, wait, waiting, problem, minute, people
- Topic 3: thank, team, star, experience, kind, review, happy
- Topic 4: customer, employee, help, like, people, problem, question, work
- Topic 5: phone, new, mobile, subscription, mobile phone, sim card
- Topic 6: friendly, helped, professional, help, welcome, received, super, explanation

<img width="1189" height="515" alt="image" src="https://github.com/user-attachments/assets/9419e1fc-ece7-4992-934e-2323f42e56e9" />

- Operational triage (Topic 2): Identify stores/times with high Queueing & Wait-Time share → adjust staffing/appointment systems, deploy “quick wins” counters (SIM swaps, bill pay).
- Churn risk (Topic 1): Billing/Plan & Connectivity mentions often precede cancellations. Route these reviews to a retention workflow; add clear signage/process for cancellations/plan changes.
- Sales enablement (Topic 5): If Device & SIM co-occurs with explanation (Topic 6), that’s successful onboarding. If it co-occurs with problem (Topic 4), improve scripts/checklists for SIM activations/number porting.
  
## N-gram frequency & word clouds for quick theme scanning

### High rating reviews
<img width="1521" height="790" alt="image" src="https://github.com/user-attachments/assets/c25eb6dc-28d0-4647-849f-92e4d1576d0e" />

### Low rating reviews
<img width="1521" height="790" alt="image" src="https://github.com/user-attachments/assets/9117d1a3-b667-4c85-bbd9-2491883982d6" />



