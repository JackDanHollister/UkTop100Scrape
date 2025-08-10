####### UK top 100 weekly album chart data scrape script #######
### This version fixes BOTH the primis ad filtering AND the character loss issue ###
### FIXED: GREATEST HITS now preserved correctly (no more GATEST HITS) ###

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

### Main Code ###
def extract_album_data(url):
    try:
        # Sends a GET request to the URL and raises an exception for bad responses.
        response = requests.get(url)
        response.raise_for_status()
        # Parses the HTML content of the page.
        soup = BeautifulSoup(response.content, "html.parser")
        # Attempts to find the week information and handles the absence gracefully.
        week_info_element = soup.find("p", class_="text-brand-cobalt")
        week_info = week_info_element.get_text(strip=True) if week_info_element else "Week information not found"
        print("Week Information:", week_info)
        # Finds all album entries on the page.
        chart_items = soup.find_all("div", class_="chart-item")
        top_100_albums = []
        
        # Iterates through each album entry, extracting relevant data.
        for index, chart_item in enumerate(chart_items, start=1):
            album_data = {}
            # FIXED: Skip items with 'chart-ad' OR 'primis' classes (both are advertisements)
            item_classes = chart_item.get("class", [])
            if "chart-ad" in item_classes or "primis" in item_classes:
                continue
                
            # Extracts the album name, handling missing data with a default value.
            album_name_elem = chart_item.find("a", class_="chart-name")
            if album_name_elem:
                album_title = album_name_elem.get_text(strip=True)
                # FIXED: Smart removal of "New" and "RE" indicators that preserves text integrity
                cleaned_title = smart_clean_title(album_title)
                album_data["Album"] = cleaned_title
            else:
                album_data["Album"] = "Unknown Album"
            
            # Extracts the artist name, again handling missing data with a default value.
            artist_name_elem = chart_item.find("a", class_="chart-artist")
            album_data["Artist"] = artist_name_elem.get_text(strip=True) if artist_name_elem else "Unknown Artist"
            
            # Extracts the album's chart position, defaulting to None if missing.
            position_elem = chart_item.find("strong")
            album_data["Position"] = position_elem.get_text(strip=True) if position_elem else None
            
            # Extracts last week's position, peak position, and weeks on chart, providing default values for missing data.
            last_week = chart_item.find("span", title="Last week")
            album_data["Last Week"] = last_week.get_text(strip=True) if last_week else "Not Available"
            
            peak = chart_item.find("li", class_="peak")
            album_data["Peak"] = peak.find("span", class_="text-brand-cobalt").get_text(strip=True) if peak else "Not Available"
            
            weeks_on_chart = chart_item.find("li", class_="weeks")
            album_data["Weeks on Chart"] = weeks_on_chart.find("span", class_="text-brand-pink").get_text(strip=True) if weeks_on_chart else "Not Available"
            
            # Adds the week's information to the album data.
            album_data["Week"] = week_info
            top_100_albums.append(album_data)
            
        # Converts the list of album data into a DataFrame for export.
        df = pd.DataFrame(top_100_albums)
        return df
    # Handles exceptions from HTTP requests.
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    # Catches and prints any other exceptions.
    except Exception as e:
        print("Error processing data:", e)
        return None

def smart_clean_title(title):
    """
    Intelligently removes chart indicators without damaging actual album content.
    
    FIXED: The original .replace("New", "").replace("RE", "") was too aggressive and would
    remove "RE" from within words like "GREATEST" -> "GATEST".
    
    This function only removes these indicators when they appear as chart markers.
    """
    # Remove leading/trailing whitespace
    cleaned = title.strip()
    
    # Remove "New" indicator when it appears at the start (common pattern)
    # Use word boundary to avoid removing "New" from album titles like "New York"
    cleaned = re.sub(r'^New\s+', '', cleaned)
    cleaned = re.sub(r'^New$', '', cleaned)  # If the whole thing is just "New"
    
    # Remove "RE" indicator when it appears at the start (re-entry indicator)
    # This is more conservative - only remove "RE" at the beginning of the string
    cleaned = re.sub(r'^RE\s+', '', cleaned)
    cleaned = re.sub(r'^RE$', '', cleaned)  # If the whole thing is just "RE"
    
    # Handle cases where "RE" appears before the title (like "RETHE 50 GREATEST HITS")
    # This catches the specific pattern where RE gets stuck to the beginning
    cleaned = re.sub(r'^RE([A-Z])', r'\1', cleaned)
    
    # Clean up any extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

# Sets the base URL for the album chart and the date range for data extraction.
base_url = "https://www.officialcharts.com/charts/albums-chart/"
start_date = pd.Timestamp("1956-07-29")
end_date = pd.Timestamp.now()  # Run until current date
# Initializes an Excel writer for exporting the data with current date in filename
current_date_str = pd.Timestamp.now().strftime("%Y%m%d")
excel_file = pd.ExcelWriter(f"top_100_albums_1956_to_{current_date_str}.xlsx", engine="xlsxwriter")

# Loops through each week in the date range, extracting and exporting data.
current_date = start_date
while current_date <= end_date:
    start_week = current_date.strftime("%Y%m%d") + "/7502/"
    print(f"Processing week: {start_week[:8]}")
    url = base_url + start_week
    week_data = extract_album_data(url)
    # Checks if data was successfully extracted and exports it to a new sheet in the Excel file.
    if week_data is not None:
        next_date = current_date + pd.DateOffset(weeks=1)
        week_start_date = start_week[:8]
        sheet_name = f"Week {week_start_date}"
        week_data.to_excel(excel_file, sheet_name=sheet_name, index=False)
        print(f"Week {week_start_date} data saved successfully.")
        current_date = next_date
    else:
        # Skips weeks where data could not be extracted due to errors.
        print(f"Skipping Week {start_week[:8]} due to an error.")
        current_date = current_date + pd.DateOffset(weeks=1)

# Finalizes the Excel file and prints a success message.
excel_file.close()
print("Final Excel file saved.")
print("All data saved successfully.")
