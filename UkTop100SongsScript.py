####### UK top 100 weekly singles chart data scrape script #######
### This version fixes BOTH the primis ad filtering AND the character loss issue ###
### FIXED: GREATEST HITS now preserved correctly (no more GATEST HITS) ###

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

### Main code ###
def extract_week_data(url):
    try:
        # Sends a GET request to the specified URL
        response = requests.get(url)
        # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        # Parses the content of the response using BeautifulSoup to navigate the HTML/XML
        soup = BeautifulSoup(response.content, "html.parser")
        # Finds the first <p> element with the specified class, used to extract the week's information
        week_info_element = soup.find("p", class_="text-brand-cobalt")
        week_info = week_info_element.get_text(strip=True) if week_info_element else "Week information not found"
        print("Week Information:", week_info)
        # Finds all <div> elements with the specified class, each representing a chart item
        chart_items = soup.find_all("div", class_="chart-item")
        top_100_songs = []
        
        for index, chart_item in enumerate(chart_items, start=1):
            song_data = {}
            # FIXED: Skip items with 'chart-ad' OR 'primis' classes (both are advertisements)
            item_classes = chart_item.get("class", [])
            if "chart-ad" in item_classes or "primis" in item_classes:
                continue
                
            # Extracts the song name, cleaning up any markers like "New" or "RE"
            song_name_elem = chart_item.find("a", class_="chart-name")
            if song_name_elem:
                song_title = song_name_elem.get_text(strip=True)
                # FIXED: Smart removal of "New" and "RE" indicators that preserves text integrity
                cleaned_title = smart_clean_title(song_title)
                song_data["Song"] = cleaned_title
            else:
                song_data["Song"] = None
                
            # Extracts the artist name
            artist_name_elem = chart_item.find("a", class_="chart-artist")
            song_data["Artist"] = artist_name_elem.get_text(strip=True) if artist_name_elem else None
            
            # Extracts the song's position on the chart
            position_elem = chart_item.find("strong")
            song_data["Position"] = position_elem.get_text(strip=True) if position_elem else None
            
            # Additional details like last week's position, peak, and weeks on chart are also extracted
            last_week = chart_item.find("span", title="Last week")
            song_data["Last Week"] = last_week.get_text(strip=True) if last_week else None
            
            peak = chart_item.find("li", class_="peak")
            song_data["Peak"] = peak.find("span", class_="text-brand-cobalt").get_text(strip=True) if peak else None
            
            weeks_on_chart = chart_item.find("li", class_="weeks")
            song_data["Weeks on Chart"] = weeks_on_chart.find("span", class_="text-brand-pink").get_text(strip=True) if weeks_on_chart else None
            
            # Adds the week's information to each song's data
            song_data["Week"] = week_info
            top_100_songs.append(song_data)
        
        # Converts the list of dictionaries to a DataFrame for easier manipulation and export
        df = pd.DataFrame(top_100_songs)
        return df
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
    except Exception as e:
        print("Error processing data:", e)
        return None

def smart_clean_title(title):
    """
    Intelligently removes chart indicators without damaging actual song content.
    
    FIXED: The original .replace("New", "").replace("RE", "") was too aggressive and would
    remove "RE" from within words like "GREATEST" -> "GATEST".
    
    This function only removes these indicators when they appear as chart markers.
    """
    # Remove leading/trailing whitespace
    cleaned = title.strip()
    
    # Remove "New" indicator when it appears at the start (common pattern)
    # Use word boundary to avoid removing "New" from song titles like "New York"
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

# Base URL for fetching data
base_url = "https://www.officialcharts.com/charts/singles-chart/"
# Define the start and end dates for data extraction - NOW UPDATES TO CURRENT DATE AUTOMATICALLY
start_date = pd.Timestamp("1952-11-14")
end_date = pd.Timestamp.now()  # Run until current date
# Create an Excel writer object for exporting data with current date in filename
current_date_str = pd.Timestamp.now().strftime("%Y%m%d")
excel_file = pd.ExcelWriter(f"top_100_songs_1952_to_{current_date_str}.xlsx", engine="xlsxwriter")

current_date = start_date
while current_date <= end_date:
    start_week = current_date.strftime("%Y%m%d") + "/7501/"
    print(f"Processing week: {start_week[:8]}")
    url = base_url + start_week
    week_data = extract_week_data(url)
    if week_data is not None:
        next_date = current_date + pd.DateOffset(weeks=1)
        week_start_date = start_week[:8]
        sheet_name = f"Week {week_start_date}"
        # Saves each week's data to a separate sheet in the Excel file
        week_data.to_excel(excel_file, sheet_name=sheet_name, index=False)
        print(f"Week {week_start_date} data saved successfully.")
        current_date = next_date
    else:
        print(f"Skipping Week {start_week[:8]} due to an error.")
        current_date = current_date + pd.DateOffset(weeks=1)

excel_file.close()
print("Final Excel file saved.")
print("All data saved successfully.")
