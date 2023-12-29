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
    ids = st.text_input("Enter the IDs separated by semicolons (e.g., 4753;4754;4764;4766;4844)")

    if st.button('Start Fetching Data'):
        id_list = ids.split(';')  # Split the input string into a list of IDs.

        # Create a placeholder for the DataFrame and countdown.
        data_placeholder = st.empty()
        countdown_placeholder = st.empty()

        while True:
            results = []  # Initialize a list to store the results temporarily.

            for appointment_id in id_list:
                response_data = fetch_data(appointment_id)  # Fetch the data for the given ID.
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time.

                # Initialize variables for date, hour, and status.
                first_available = ""
                status = ""

                # Check the response data and determine the status and first available appointment.
                if response_data and response_data.get('appointment') != []:
                    appointment = response_data.get('appointment')[0]  # Assuming the first one is the earliest.
                    date = appointment.get('date')
                    hour = appointment.get('hour')
                    if date and hour:
                        first_available = f"{date} {hour}"
                        status = "Appointment Available"
                    else:
                        status = "No Appointment"
                else:
                    status = "No Appointment"

                # Append the result to the results list.
                results.append({"Time": time_now, "ID": appointment_id, "Status": status, "First Available": first_available})

            # Create a DataFrame from the results list.
            df = pd.DataFrame(results)

            # Function to color the status.
            def color_status(val):
                color = 'red' if val == "No Appointment" else 'green'
                return f'background-color: {color}'

            # Clear previous data and display the new DataFrame with updated styling method.
            data_placeholder.empty()
            data_placeholder.dataframe(df.style.map(color_status, subset=['Status']))

            # Countdown to the next refresh.
            for remaining in range(5, 0, -1):
                countdown_placeholder.text(f"Next refresh in: {remaining} seconds")
                time.sleep(1)

            # Clear countdown at the end of the cycle.
            countdown_placeholder.empty()

if __name__ == "__main__":
    main()
