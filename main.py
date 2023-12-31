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
    st.title('🏥 Buscador de Turnos')

    # Input for IDs.
    ids = st.text_input("Ingresar los IDs de los Medicos separados por comas (e.g., 4753;4754;4764;4766;4844;5799)", value="4753;4754;4764;4766;4844;5799")

    if st.button('🔎 Buscar Turnos'):
        id_list = ids.split(';')  # Split the input string into a list of IDs.

        # Create a placeholder for the DataFrame and countdown.
        data_placeholder = st.empty()
        countdown_placeholder = st.empty()

        while True:
            results = []  # Initialize a list to store the results temporarily.

            for appointment_id in id_list:
                response_data = fetch_data(appointment_id)  # Fetch the data for the given ID.
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time.

                # Check if the 'appointment' field is non-empty and extract the date and hour.
                if response_data and response_data.get('appointment') and isinstance(response_data['appointment'], dict):
                    appointment_info = response_data['appointment']
                    appointment_date = appointment_info.get('date', 'N/A')
                    appointment_hour = appointment_info.get('hour', 'N/A')
                    status = "HAY TURNOS! 🔥"
                    color = "green"
                else:
                    appointment_date = 'N/A'
                    appointment_hour = 'N/A'
                    status = "SIN TURNOS 😒"
                    color = "red"

                # Append the result to the results list.
                results.append({
                    "Time": time_now,
                    "ID": appointment_id,
                    "Status": status,
                    "Appointment Date": appointment_date,
                    "Appointment Hour": appointment_hour
                })

            # Create a DataFrame from the results list.
            df = pd.DataFrame(results)

            # Function to color the status.
            def color_status(val):
                color = 'red' if val == "SIN TURNOS 😒" else 'green'
                return f'background-color: {color}'

            # Clear previous data and display the new DataFrame.
            data_placeholder.empty()
            data_placeholder.dataframe(df.style.applymap(color_status, subset=['Status']))

            # Countdown to the next refresh.
            for remaining in range(5, 0, -1):
                countdown_placeholder.text(f"Next refresh in: {remaining} seconds")
                time.sleep(1)

            # Clear countdown at the end of the cycle.
            countdown_placeholder.empty()

if __name__ == "__main__":
    main()