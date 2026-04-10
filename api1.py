import streamlit as st
import requests

st.title("🌦️ Weather App")

api_key = "3ced0f180200e383496b881267b46bc8"

# 👉 Input
city = st.text_input("Enter cities (comma separated):")

# 👉 Get Weather Button
if st.button("Get Weather"):

    if city:
        cities = city.split(",")

        for c in cities:
            c = c.strip()

            if c == "":
                continue

            url = f"https://api.openweathermap.org/data/2.5/weather?q={c}&appid={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                temp = data["main"]["temp"] - 273.15
                weather = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]

                # 👉 Display UI
                st.subheader(f"📍 {data['name']}")
                st.metric("🌡️ Temperature", f"{round(temp,2)} °C")
                st.write(f"🌦️ Condition: {weather}")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind: {wind}")
                st.write("---")

                # 👉 Save History
                with open("history.txt", "a") as f:
                    f.write(f"{data['name']} - {round(temp,2)}°C\n")

            else:
                st.error(f"{c} ❌ not found")

    else:
        st.warning("Please enter a city ⚠️")


# 👉 Show History Button
if st.button("Show History"):
    try:
        with open("history.txt", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.warning("No history found yet 📂")