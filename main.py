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

    with st.expander("About this app", expanded=True):
        st.info("This development is a python code of one of the most important hospitals in Argentina, [Hospital de Clinicas]. This app finds next appointments with specified doctors, based on personal codes served by the Hospital.")
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

# Display badge
st.markdown("""
    <div style="display: flex; align-items: center;">
        <img src="https://raw.githubusercontent.com/peteciank/public_files/main/mugshot_light.png" alt="Profile Picture" style="border-radius: 50%; margin-right: 20px;width: 50px; height: 50px;">
        <div>
            <p style="font-weight: bold; margin-bottom: 5px;">Created by Pete Ciank</p>
            <p style="margin: 0;">Streamlit enthusiast, Tech Lover, Product and Project Manager 💪</p>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.expander("📃 Check my personal links, Resume, Cover Letter and More", expanded=False):
    st.markdown('📖 My [LinkedIn](https://www.linkedin.com/in/pedrociancaglini/) Profile.')
    st.markdown('🌎 My [Website](https://sites.google.com/view/pedrociancaglini)')
    st.markdown('👩‍💻 My [Github](https://github.com/peteciank/)')
    st.markdown('🔽 [Download](https://github.com/peteciank/public_files/blob/main/Ciancaglini_Pedro_Resume_v24.pdf) my Resume')
    st.markdown('🔽 [Download](https://github.com/peteciank/public_files/blob/main/Cover%20Letter.pdf) my Letter')

if __name__ == "__main__":
    main()
