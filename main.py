import streamlit as st
import requests
import time

# Function to fetch data from the API.
def fetch_data():
    url = "https://api.hospitaldeclinicas.uba.ar/api/appointments/appointment/first/4753"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response if successful.
    else:
        return "Error fetching data"  # Returns an error message if not successful.

def main():
    # Streamlit app title.
    st.title('API Data Fetcher')

    # Container to hold the data.
    data_container = st.empty()

    # Button to start the data fetching process.
    if st.button('Start Fetching Data'):
        while True:
            data = fetch_data()  # Fetch the data from the API.
            data_container.json(data)  # Display the data as JSON in the app.
            time.sleep(5)  # Wait for 5 seconds before fetching again.

if __name__ == "__main__":
    main()
