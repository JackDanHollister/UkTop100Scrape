###### UkTop100Scrape ######



---

A little project I made where I set out to see whether I could scrape and organise all the UK top 100 single and album data from its start in 1953 to the current date (my last run was early August 2025).

Each week's data is saved to its own Excel sheet, capturing decades of music history with song/album title, artist, position, previous week position, peak position, and weeks on chart.

(Update August 2025) The chart site doesn’t capture genre data; however, I am currently exploring how to add this via other sources.

---



---

## Requirements

```bash
pip install requests beautifulsoup4 pandas xlsxwriter
```

## Usage

### For Singles Chart:
```bash
python UkTop100SongsScript.py
```
**Output**: `top_100_songs_1952_to_YYYYMMDD.xlsx`

### For Albums Chart:
```bash
python UkTop100AlbumsScript.py
```
**Output**: `top_100_albums_1956_to_YYYYMMDD.xlsx`

---



---

## Data Structure

Each Excel sheet contains:
- **Song/Album**: Title (properly cleaned, preserving "GREATEST HITS")
- **Artist**: Performing artist or band
- **Position**: Current week's chart position
- **Last Week**: Previous week's position
- **Peak**: Highest position reached
- **Weeks on Chart**: Total weeks charted
- **Week**: Date range for the chart week


### Auto-Current Date
Scripts automatically run until today's date.

## Important Notes

- **Chart Size Variation**: Early years had varying chart sizes (15 → 100)
- **Processing Time**: Complete datasets can take several hours due to volume
- **Error Handling**: Automatically skips weeks with data issues
- **Clean Data**: Advertisement content properly excluded



## Troubleshooting

- Ensure all required packages are installed
- Check internet connection for web scraping
- Large downloads may take several hours
- Scripts will automatically retry and skip problematic weeks

## License

This project is for educational and research purposes. Please respect the Official Charts Company's terms of service.

---

**Issue #1 Status**: ✅ **RESOLVED** - No more character loss in album/song titles
