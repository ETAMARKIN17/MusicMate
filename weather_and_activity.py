import requests


# Function to fetch weather forecast for a specified city
def weather_forecast(city, api_key):
    """
    Fetches weather forecast for a specified city using WeatherAPI.

    Args:
    - city (str): Name of the city for which weather forecast is requested.
    - api_key (str): API key for WeatherAPI.

    Returns:
    - Tuple containing weather statistics (temperature in Fahrenheit and weather condition) and city name.
    """
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        city_from_response = json_response['location']['name']
        region_from_response = json_response['location']['region']
        fahrenheit = json_response['current']['temp_f']
        weather = json_response['current']['condition']['text']
        return (fahrenheit, weather), city_from_response
    else:
        print("Error, status code:", response.status_code)
        print("Please try again with a valid city name")


# Function to prompt user for their activity
def users_activity():
    """
    Prompts user to input their current activity.

    Returns:
    - String containing user's activity.
    """
    while True:
        activity = input("In a few words, what activity will you be doing (limit 50 characters)? ")
        if len(activity) <= 50:
            return activity
        else:
            print("Character limit exceeded. Please enter the activity again with a shorter description")
