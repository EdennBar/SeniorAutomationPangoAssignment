import requests
import configparser
class ApiHelper:
    def __init__(self) :
        config = configparser.ConfigParser()
        config.read("../config/config.ini")
        self.API_KEY = config['API']['API_KEY']
        self.BASE_URL =  config['WEATHER']['BASE_URL']


    
    weather_data = {}
    weather_data_multiple_cities= {}

    
    def append_weather_data(self, data):
        self.weather_data.update(data)
    
    def get_current_weather(self, params):
        url = f"{self.BASE_URL}?q={params['city']}&units={params['celsius']}&lang={params['lang']}&appid={self.API_KEY}"
        response = requests.get(url)
        return response

    def get_current_weather_of_multiple_cities_by_id(self, params):
        city_ids = ",".join(params['id'])
        url = f"http://api.openweathermap.org/data/2.5/group?id={city_ids}&units=metric&appid={self.API_KEY}"
        response = requests.get(url)
        return response