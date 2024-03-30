# UkTop100Scrape
This project scrapes data for every top 100 song from the start of the UK Top 100 charts to the latest week, capturing decades of music history in detail. This saves each week's data into its own sheet within an Excel file.

Please note that the first couple of years and the total number of songs it follows each week fluctuates quite dramatically, starting at 15, dropping to 13, and then eventually making its way up to reviewing the top 100.


``` python

import requests
from bs4 import BeautifulSoup
import pandas as pd

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
excel_file = pd.ExcelWriter("top_100_songs_1952_to_2024.xlsx", engine="xlsxwriter")

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
