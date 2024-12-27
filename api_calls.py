# import requests to use the API for weather
import requests

# import json to work with the data retrieved from the open trivia db API
import json  

#####################################################################################################################


class WeatherApiCalls():    
    def __init__(self):
        # put in env file ###################
        self.api_key = 'fccc12b66bb2eee64c79eb57ac4503cf'

    def call_coord_api(self):
        # name of city
        city_name = 'Cape Town'
        # no. of locations returned in API response
        limit = '3'
        # http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
        coord_api_call = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={self.api_key}'

        # store url in a variable as a json response
        response = requests.get(coord_api_call)

        # check if the get request was successful
        # parse the JSON content of the response using the .json() method
        if response.status_code == 200:
            json_response = response.json()
    
            # write coordinates for the city to a json file
            with open("city_coordinates", "w") as c:
                json.dump(json_response, c, indent=4)

            # return the JSON content 
            return json_response

        # check if the get request was unsuccessful
        else:
            # print error if unsuccessful request
            # return None to signal that there's no valid data to work with
            error_message = f"Unable to retrieve the coordinates - Status code:{response.status_code}"
            print(error_message)
            return None

    # make API call to OpenWeatherMap.org to get access to current weather
    # {lat}{lon}{part}{api key} respectively
    # place co-ordinates of city, exlcude unwanted data, insert personal API key generated after subscribing to One Call API 3.0
    def call_weather_api(self):        
        latitude = -33.9288301
        longitude = 18.4172197
        exclude = 'minutely,hourly,daily,alerts'
        ##weather_api_call = f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude={exclude}&appid={self.api_key}'
        weather_api_call = 'https://api.openweathermap.org/data/3.0/onecall?lat=-33.9288301&lon=18.4172197&exclude=minutely,hourly,daily,alerts&appid=fccc12b66bb2eee64c79eb57ac4503cf'

        # store url in a variable as a json response
        response = requests.get(weather_api_call)

        # check if the get request was successful
        # parse the JSON content of the response using the .json() method
        try:
            ##if response.status_code == 200:
            print(f"Status code:{response.status_code}")
            json_response = response.json()

            # write current weather for the city to a json file
            with open("cape_town_weather", "w") as f:
                json.dump(json_response, f, indent=4)

            # return the JSON content 
            return json_response

        # check if the get request was unsuccessful
        except Exception as e:
            # print error if unsuccessful request
            # return None to signal that there's no valid data to work with
            error_message = f"Unable to retrieve the current weather - Status code:{response.status_code}\n{e}"
            print(error_message)
            return None

# create an instance of WeatherApiCalls class
weather = WeatherApiCalls() 

# call method to find the location of selected city - cape town
# comment out coordinate after initial method was called because it does not need repetition       
# coordinates = weather.call_coord_api()

# # call method to retrieve the current weather in cape town
current_weather = weather.call_weather_api()