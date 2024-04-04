# UkTop100Scrape
This project consists of two versions: one that scrapes data for every weekly UK top 100 singles from the start of the single charts (back in 1952) to the latest week, and the other scrapes data for every weekly top 100 albums from the start of the album charts (back in 1956), again to the latest week, capturing decades of music history in detail. This saves each week's data into its own sheet within an Excel file.

This is designed to save the song (or album) title, artist, current position for each week, position the previous week, peak, and total weeks on the chart. Since it's a lot of data and can take some time to download, I've set up error handling that allows it to skip a week if there's an error instead of just stopping (which it did for me many times).

Please note that the first couple of years and the total number of songs it follows each week fluctuates quite dramatically. For instance, the singles chart starts at the top 15, drops to 12 the next week, and then eventually making its way up and up until itsreviewing the top 100 every week.

You should be able to run this code directly (except for a few packages that need to be installed beforehand).


This version is for the UK top 100 singles chart

``` python


####### UK top 100 weekly singles chart data scrape script #######


### Imports ###

import requests
from bs4 import BeautifulSoup
import pandas as pd


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
        week_info = week_info_element.get_text(strip=True)
        print("Week Information:", week_info)
        # Finds all <div> elements with the specified class, each representing a chart item
        chart_items = soup.find_all("div", class_="chart-item")
        top_100_songs = []

        for index, chart_item in enumerate(chart_items, start=1):
            song_data = {}
            # Skips the item if it's classified as a chart advertisement
            if "chart-ad" in chart_item.get("class", []):
                continue

            # Extracts the song name, cleaning up any markers like "New" or "RE"
            song_name_elem = chart_item.find("a", class_="chart-name")
            if song_name_elem:
                song_title = song_name_elem.get_text(strip=True)
                song_data["Song"] = song_title.replace("New", "").replace("RE", "").strip()
            else:
                song_data["Song"] = None

            # Extracts the artist name
            artist_name_elem = chart_item.find("a", class_="chart-artist")
            song_data["Artist"] = artist_name_elem.get_text(strip=True) if artist_name_elem else None
            
            # Extracts the song's position on the chart
            position_elem = chart_item.find("strong")
            song_data["Position"] = position_elem.get_text(strip=True) if position_elem else str(index)
            
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

# Base URL for fetching data
base_url = "https://www.officialcharts.com/charts/singles-chart/"
# Define the start and end dates for data extraction
start_date = pd.Timestamp("1952-11-14")
end_date = pd.Timestamp("2024-03-29")

# Create an Excel writer object for exporting data
excel_file = pd.ExcelWriter("top_100_songs_1952_to_2024.xlsx", engine="xlsxwriter") # This saves the xlsx to the current working directory. Change at your leisure

current_date = start_date
while current_date <= end_date:
    start_week = current_date.strftime("%Y%m%d") + "/7501/"
    print(f"Processing week: {start_week[:8]}")
    url = base_url + start_week
    week_data = extract_week_data(url)

    if week_data is not None:
        next_date = current_date + pd.DateOffset(weeks=1)
        week_start_date = start_week[:8]
        sheet_name = f"Week {week_start_date}"  # Sheet name based on the week
        # Saves each week's data to a separate sheet in the Excel file
        week_data.to_excel(excel_file, sheet_name=sheet_name, index=False)
        print(f"Week {week_start_date} data saved successfully.")
        current_date = next_date
    else:
        print(f"Skipping Week {start_week[:8]} due to an error.")

excel_file.close()
print("Final Excel file saved.")
print("All data saved successfully.")

```

This version is for the UK top 100 album charts

``` python

####### UK top 100 weekly album chart data scrape script #######

### Imports ###

import requests
from bs4 import BeautifulSoup
import pandas as pd


### Main Code ###

# Defines a function to extract album data from the specified URL.
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
            # Skips advertisement entries.
            if "chart-ad" in chart_item.get("class", []):
                continue

            # Extracts the album name, handling missing data with a default value.
            album_name_elem = chart_item.find("a", class_="chart-name")
            album_title = album_name_elem.get_text(strip=True) if album_name_elem else "Unknown Album"
            album_data["Album"] = album_title.replace("New", "").replace("RE", "").strip()

            # Extracts the artist name, again handling missing data with a default value.
            artist_name_elem = chart_item.find("a", class_="chart-artist")
            album_data["Artist"] = artist_name_elem.get_text(strip=True) if artist_name_elem else "Unknown Artist"
            
            # Extracts the album's chart position, defaulting to the index if missing.
            position_elem = chart_item.find("strong")
            album_data["Position"] = position_elem.get_text(strip=True) if position_elem else str(index)
            
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

# Sets the base URL for the album chart and the date range for data extraction.
base_url = "https://www.officialcharts.com/charts/albums-chart/"
start_date = pd.Timestamp("1956-07-29")
end_date = pd.Timestamp("2024-03-29")

# Initializes an Excel writer for exporting the data.
excel_file = pd.ExcelWriter("top_100_albums_1956_to_2024.xlsx", engine="xlsxwriter")

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
        sheet_name = f"Week {week_start_date}"  # Names the sheet based on the week.
        week_data.to_excel(excel_file, sheet_name=sheet_name, index=False)
        print(f"Week {week_start_date} data saved successfully.")
        current_date = next_date
    else:
        # Skips weeks where data could not be extracted due to errors.
        print(f"Skipping Week {start_week[:8]} due to an error.")

# Finalizes the Excel file and prints a success message.
excel_file.close()
print("Final Excel file saved.")
print("All data saved successfully.")

```
