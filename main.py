import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# Function to fetch data from the API for a given ID.
def fetch_data(appointment_id):
    url = f"https://api.hospitaldeclinicas.uba.ar/api/appointments/appointment/first/{appointment_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response if successful.
    else:
        return None  # Returns None if not successful.

def main():
    st.title('Multiple API Data Fetcher')

    # Input for IDs.
    ids = st.text_input("Enter the IDs separated by semicolons (e.g., 4753;4754;4755)")

    if st.button('Start Fetching Data'):
        id_list = ids.split(';')  # Split the input string into a list of IDs.

        while True:
            results = []  # Initialize a list to store the results temporarily.

            for appointment_id in id_list:
                data = fetch_data(appointment_id)  # Fetch the data for the given ID.
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time.

                # Determine the status.
                if data:
                    status = "Appointment Available"
                    color = "green"
                else:
                    status = "No Appointment"
                    color = "red"

                # Append the result to the results list.
                results.append({"Time": time_now, "ID": appointment_id, "Status": status})

            # Create a DataFrame from the results list.
            df = pd.DataFrame(results)

            # Display the DataFrame with color-coded statuses.
            def color_status(val):
                color = 'red' if val == "No Appointment" else 'green'
                return f'background-color: {color}'

            st.dataframe(df.style.applymap(color_status, subset=['Status']))

            time.sleep(5)  # Wait for 5 seconds before fetching again.

if __name__ == "__main__":
    main()
