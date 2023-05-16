### 1. Overview
This script collects data from the [Melanchthon Briefwechsel database](https://melanchthon.hadw-bw.de/index.html) via basic web scraping and saves the desired output to .csv for further processing (e.g. network analysis with Gephi).

### 2. Requirements

- Latest Python 3 version
- Modules: Beatifulsoup 4, requests, csv, lxml, time

### 3. Functionality
Data to scrape:
- Regest number
- Sender + location
- Recipient + location
- Date

### 4. TODO
- check whether database entry also exists ending in -a (eg. 4, 4a)
