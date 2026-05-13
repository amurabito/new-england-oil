# 🛢️ Oil Intelligence Pro

A lightweight, automated market analysis tool for heating oil prices in the Northeast US. This project scrapes live vendor data, tracks historical trends, and identifies the most reliable price leaders.

---

## 🚀 Features

*   **Live Scraping:** Automated daily polling of New England Oil zones.
*   **Market Dominance:** Historical tracking of which vendors stay cheapest the longest.
*   **Interactive UI:** High-contrast dashboard with clickable bars for instant ordering.
*   **Value Scoring:** Visual color-coding (Green/Yellow/Red) based on the global market average.
*   **Zero Infrastructure:** Runs entirely on GitHub Actions and GitHub Pages.

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.11 (BeautifulSoup4, Requests) |
| **Frontend** | HTML5, CSS (Inter Font), Chart.js |
| **Data** | CSV (Flat-file storage) |
| **Automation** | GitHub Actions (Cron @ 12:00 UTC) |

## 📊 Data Visualization

1.  **Dominance Chart:** Ranks vendors by frequency of "Low Price" title.
2.  **Market Spread:** Daily snapshot of all vendors vs. the global average.
3.  **Historical Trends:** Zone-specific low and average price movement over time.

## ⚙️ Setup

1.  **Fork this repo.**
2.  **Enable GitHub Pages:** Point it to the `root` or `/(main)` branch.
3.  **Enable Actions:** Ensure the `Poll Oil Prices` workflow has write permissions to update `data.csv`.

---
*Created for market transparency and optimized home energy management.*
