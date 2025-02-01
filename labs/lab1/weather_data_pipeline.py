import requests
import csv

URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&past_days=10&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"


### Part 1. Read Operation (Extract)

def fetch_weather_data():
    """Fetches weather data for the past 10 days."""
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data

    else:
        print("Failed to fetch data:", response.status_code)
        return None

### Part 2. Write Operation (Load)
def save_to_csv(data, filename):
    """Saves weather data to a CSV file."""
    
    headers = ["DateTime", "Temp (°C)","Humidity (%)", "Wind Speed (m/s)"]

    #extract hourly data
    time_list = data["hourly"]["time"]
    temperature_list = data["hourly"]["temperature_2m"]
    humidity_list = data["hourly"]["relative_humidity_2m"]
    wind_speed_list = data["hourly"]["wind_speed_10m"]

    with open(filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write header row


        # Writing each row
        for i in range(len(time_list)):
            writer.writerow([
                time_list[i],
                temperature_list[i],
                humidity_list[i],
                wind_speed_list[i]
            ])
    

### Part 3. Cleaning Operation (Transform)
def clean_data(input_file, output_file):
    """ clean the data based on the following rules:
        1. Temperature should be between 0 and 60°C
        2. Humidity should be between 0% and 80%
        3. Wind speed in a betweeen 3 and 150
    """

    ### TODO: complete rest of the code
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)  # Read header row
        writer.writerow(headers)  # Write header to new file

        for row in reader:
            date_time, temp, humidity, wind_speed = row

            temp = float(temp)
            humidity = float(humidity)
            wind_speed = float(wind_speed)

            # Apply cleaning rules
            if 0 <= temp <= 60 and 0 <= humidity <= 80 and 3 <= wind_speed <= 150:
                writer.writerow(row)  # Keep the valid row
    print(f"Cleaned data saved to {output_file}")
            

### Part 4. Aggregation Operation 
def summarize_data(filename):
    """Summarizes weather data including averages and extremes."""
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read header row
        data = list(reader)  # Convert CSV data to list

        # Ensure we have data
        if not data:
            print("No data available to summarize.")
            return

        # Extract values from columns
        temperatures = [float(row[1]) for row in data if row[1] != "N/A"]
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        total_records = len(temperatures)
        humidities = [float(row[2]) for row in data if row[2] != "N/A"]
        wind_speeds = [float(row[3]) for row in data if row[3] != "N/A"]

        # Compute statistics
        avg_temp = sum(temperatures) / len(temperatures) if temperatures else 0
        avg_humidity = sum(humidities) / len(humidities) if humidities else 0
        avg_wind_speed = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0

        # Print summary
        print("📊 Weather Data Summary 📊")
        print(f"Total Records: {total_records}")
        print(f"🌡️ Average Temperature: {avg_temp:.2f}°C")
        print(f"🔥 Max Temperature: {max_temp:.2f}°C")
        print(f"❄️ Min Temperature: {min_temp:.2f}°C")
        print(f"💧 Average Humidity: {avg_humidity:.1f}%")
        print(f"💨 Average Wind Speed: {avg_wind_speed:.2f} m/s")



if __name__ == "__main__":
    weather_data = fetch_weather_data()
    if weather_data:
        save_to_csv(weather_data, "weather_data.csv")
        print("Weather data saved to weather_data.csv")
        clean_data("weather_data.csv", "cleaned_data.csv")
        #print("Weather data clean saved to cleaned_data.csv")
        summarize_data("cleaned_data.csv")
        

