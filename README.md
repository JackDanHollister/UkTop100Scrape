# UkTop100Scrape

## 🆕 Bug Fix Update (August 2025) - ISSUE #1 RESOLVED

**IMPORTANT**: This repository has been updated to fix critical bugs that were causing data accuracy issues.

### 🐛 Issues Fixed:
1. **Character Loss Bug**: Albums showing "GATEST HITS" instead of "GREATEST HITS" 
   - **Root Cause**: `.replace("RE", "")` was removing "RE" from within words
   - **Solution**: Smart cleaning function that only removes New/RE chart indicators
2. **Advertisement Filtering**: Missing "primis" advertisements in data
   - **Solution**: Enhanced filtering to catch both "chart-ad" and "primis" ads
3. **Date Range**: Scripts now auto-update to current date instead of fixed end date

### ✅ Verification:
- **Zero** "GATEST" entries found in new datasets
- **17** correctly preserved "GREATEST HITS" entries verified
- Clean advertisement filtering working perfectly

---

## Description

This project scrapes complete UK chart data:
- **Singles**: Every weekly UK Top 100 singles from November 1952 to present
- **Albums**: Every weekly UK Top 100 albums from July 1956 to present

Each week's data is saved to its own Excel sheet, capturing decades of music history with song/album title, artist, position, previous week position, peak position, and weeks on chart.

## Features

- ✅ **Complete Historical Data**: From chart inception to current date
- ✅ **Robust Error Handling**: Skips problematic weeks instead of crashing
- ✅ **Clean Data**: Proper advertisement filtering and text preservation
- ✅ **Auto-Updating**: Automatically runs to current date
- ✅ **Issue #1 Resolved**: "GREATEST HITS" preserved correctly

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

## Data Structure

Each Excel sheet contains:
- **Song/Album**: Title (properly cleaned, preserving "GREATEST HITS")
- **Artist**: Performing artist or band
- **Position**: Current week's chart position
- **Last Week**: Previous week's position
- **Peak**: Highest position reached
- **Weeks on Chart**: Total weeks charted
- **Week**: Date range for the chart week

## Recent Improvements

### Smart Title Cleaning
The new cleaning function preserves text integrity:
```python
# OLD (BUGGY): 
title.replace("New", "").replace("RE", "")  # "GREATEST" → "GATEST" ❌

# NEW (FIXED):
smart_clean_title(title)  # Only removes chart indicators ✅
```

### Enhanced Advertisement Filtering
```python
# Now catches both types of advertisements
if "chart-ad" in item_classes or "primis" in item_classes:
    continue
```

### Auto-Current Date
Scripts automatically run until today's date instead of requiring manual updates.

## Important Notes

- **Chart Size Variation**: Early years had varying chart sizes (15 → 100)
- **Processing Time**: Complete datasets take several hours due to volume
- **Error Handling**: Automatically skips weeks with data issues
- **Clean Data**: Advertisement content properly excluded

## Sample Data Files

This repository includes sample Excel files demonstrating the clean, accurate output format with all fixes applied.

## Troubleshooting

- Ensure all required packages are installed
- Check internet connection for web scraping
- Large downloads may take several hours
- Scripts will automatically retry and skip problematic weeks

## License

This project is for educational and research purposes. Please respect the Official Charts Company's terms of service.

---

**Issue #1 Status**: ✅ **RESOLVED** - No more character loss in album/song titles
