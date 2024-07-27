# ConCoRD: Condo Collection Record Downloader
Python code to scrape condo information from [LivingInsider](https://www.livinginsider.com/). Built as an hobby and to get some insights of condo prices in Thailand
## Usage
1. Open `ConCoRD/scraper.py` and edit the parameters.
   1. `URLS`: list of urls to access condo locations in Thailand
   2. `N_PAGES`: number of pages to scrape for each url
   3. `USE_CACHE`: whether to use html cache
   4. `OUTPUT_DIR`: output directory
2. Run `python ConCoRD/scraper.py`.
3. Analyze the output in the `OUTPUT_DIR` :)
## Output
The output shape is csv with the format as follows:

| id      | name                  | price      | size        | level       | bedroom | bathroom | url  | last_edit | source         | datadate |
| ------- | --------------------- | ---------- | ----------- | ----------- | ------- | -------- | ---- | --------- | -------------- | -------- |
| 1952022 | Sym Vipa - Ladprao    | ฿5,700,000 | 67.44 Sq.m. | Level 10    | 2 Beds  | 1 Bath   | url1 | 20240212  | living_insider | 20240218 |
| 1709476 | Life Phahon - Ladprao | ฿5,880,000 | 42.50 Sq.m. | Level 5-10  | 1 Beds  | 1 Bath   | url2 | 20240218  | living_insider | 20240218 |
| 1802614 | Life Ladprao          | ฿4,790,000 | 35 Sq.m.    | Level 21-50 | 1 Beds  | 1 Bath   | url3 | 20240217  | living_insider | 20240218 |
