import pytest
from ..utilities.api_helpers import ApiHelper

from ..utilities.db_helpers import DatabaseHelper

@pytest.fixture(scope="module")
def api():
    return ApiHelper()

@pytest.fixture(scope="module")
def db():
    return DatabaseHelper()

"""
1. Add a test case that verifies get_current_weather with Celsius Metric and language English
	1. Validte Status Code
	2. Insert the response of temperature, feels_like for each city to DB
	3. Verify temperature and feels_like from DB are equal to API response 
"""

@pytest.mark.parametrize("city", ["London", "Paris", "New York", "Tokyo"])
def test_get_weather_data(api, city):
    params = {
        "city": city,
        "celsius": "metric",
        "lang": "en"
    }
    response = api.get_current_weather(params)
    assert response.status_code == 200, f"Failed to get weather data for {city}"
    api.weather_data[city] = response.json()
    print( api.weather_data)
    

def test_insert_weather_data(db, api):
    for city, data in api.weather_data.items():
        db.insert_weather_data(city, data["main"]["temp"], data["main"]["feels_like"])
        

def test_temperature_and_feels_like_equal_in_db_and_api(db, api):
    for city, data in api.weather_data.items():
        db_data = db.get_weather_data(city)
        assert db_data["temperature"] == data["main"]["temp"]
        assert db_data["feels_like"] == data["main"]["feels_like"]

"""
2. Add a negative test that verifies the temperature entered into
 the database is not equal to the temperature returned from the API response
"""      

def test_temperature_not_equal(db, api):
    bias = 100
    for city, data in api.weather_data.items():
        db_data = db.get_weather_data(city)
        db_temperature = db_data.get("temperature")
        altered_api_weather_data = data["main"]["temp"] + bias
        assert db_temperature != altered_api_weather_data, (
            f"Expected temperatures to mismatch for {city}, but they matched.\n"
            f"DB Temperature: {db_temperature}, API Temperature: {altered_api_weather_data}"
        )


@pytest.mark.parametrize("city, incorrect_db_temperature, feels_like", [("London", 100, 99)])
def test_negative_test_temperature_update_in_db_by_incorrect_value(db, api, city, incorrect_db_temperature, feels_like):
    db.insert_weather_data(city, incorrect_db_temperature, feels_like)
    correct_api_temperature = api.weather_data["London"]["main"]["temp"]
    db_data = db.get_weather_data(city)
    incorrect_db_temperature_from_db = db_data["temperature"]
    
    assert incorrect_db_temperature_from_db != correct_api_temperature, (
        f"Expected temperatures to mismatch. "
        f"DB Temperature: {incorrect_db_temperature_from_db}, "
        f"API Temperature: {correct_api_temperature}"
    )

"""
3. Add a test case that uses Weather Data for Multiple cities by using the City ID parameter 

Example of the API
https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}

	1. Insert the response of temperature, feels_like for each city to DB 
	2. Create a new column in DB that contains an average of temperature, feels_like for each city 
	3. Assert the data that was inserted into DB is equal to the one from the response except for the average temperature
	4. Print the city with the highest average temperature
""" 
# london :2643743
# Paris: 6942553
# new york : 5128638
# tokyo: 1850147
def test_get_weather_data_for_multiple_cities(api):
    params = {
        "id": ["2643743","6942553","5128638","1850147"]
    }
    response = api.get_current_weather_of_multiple_cities_by_id(params)
    assert response.status_code == 200
    api.weather_data_multiple_cities = response.json()


def test_insert_for_multiple_cities(db, api):
    for city_data in api.weather_data_multiple_cities["list"]:
        city_name = city_data["name"]
        temperature = city_data["main"]["temp"]
        feels_like = city_data["main"]["feels_like"]
        db.insert_weather_data(city_name, temperature, feels_like)
        

def test_create_average_column(db):
    if not "average" in db.get_column_names("weather_data"):
       db.add_average_column()
    

    
def test_calculate_average(db):
    db.update_average()


def test_inserted_db_data_equal_to_response(api, db):   
    for city_data in api.weather_data_multiple_cities["list"]:
        city_name = city_data["name"]
        temperature_api = city_data["main"]["temp"]
        feels_like_api = city_data["main"]["feels_like"]
        db_data = db.get_weather_data(city_name)
        assert db_data["temperature"] == temperature_api, f"Temperature for {city_name} should match"
        assert db_data["feels_like"] == feels_like_api, f"Feels Like for {city_name} should match"


def test_highest_temperature(db):
    print(db.highest_temperature())
    



