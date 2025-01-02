# import requests to use the API for weather
import requests

# import json to work with the data retrieved from the openweathermap.org API
import json  

# import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv

# import os to access environment variables
import os

# import datetime to get the date, time
from datetime import datetime,timedelta

#####################################################################################################################

# define a parent class that makes API calls to openweathermap
class WeatherApiCalls():    
    def __init__(self):
        # put api key in .env file
        # load api key from .env file
        load_dotenv()
        # use try-except defense in a loop to retrieve the API key
        while True:
            # try to fetch the environment variable for weather
            # break the loop
            try:
                self.api_key = os.getenv('WEATHER_API_KEY')
                break
            # except if the environment variable was not found
            # continue loop
            # then check the .env file to see it's there
            except KeyError as e:
                print(f"{e} \nWeather API key not found in .env file.")
                continue

    # define a method that makes an API call to OpenWeatherMap.org for the co-ordinates of Cape Town
    def call_coord_api(self):
        """A method that calls the OpenWeatherMap.org API & fetches the co-ordinates for Cape Town.

        :return: Return the JSON response for Cape Town's co-ordinates.
        :rtype: dict
        """
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
        """A method that calls the OpenWeatherMap.org API & fetches the weather for Cape Town.

        :return: Return the JSON response for Cape Town's weather.
        :rtype: dict
        """      
        # copy coord from the city_coordinates.txt saved in call_coord_api() method
        latitude = -33.9288301
        longitude = 18.4172197
        # set the units used in South Africa as metric
        units = 'metric'
        # exclude unwated data from the json response
        exclude = 'minutely,hourly,daily,alerts'
        # construct the OpenWeatherMap.org API url for the one call api 3.0
        weather_api_call = f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units={units}&exclude={exclude}&appid={self.api_key}'        

        # store url in a variable as a json response
        response = requests.get(weather_api_call)

        # check if the get request was successful
        # parse the JSON content of the response using the .json() method
        try:
            # with a status code 200, the data can be parsed with json()            
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

# create derived/subclass of WeatherApiCalls to get items from the json_response
class CurrentConditions(WeatherApiCalls):
    def __init__(self):
        # return a tempory object of the parent class so that its methods can be called
        super().__init__()        

    # create a method to get the current temperature
    def temperature(self):
        """A method that returns the current temperature in Cape Town.

        :return: Return the temperature in degrees Celsius.
        :rtype: int
        """
        # call the method to collect json data for the weather in cape town
        json_response = super().call_weather_api() 
        # retrieve the temperature float from the json response dictionary with get()  
        # put default values if no key found, note its a dict & float as seen from the json_response
        current_temp = json_response.get("current", {}).get("temp", 0.0)
        # round the temperature
        round_temp = round(current_temp)
        # return the temperature
        return round_temp
    
    # create a method to get the weather description
    def weather_description(self):
        """A method that returns the current weather description in Cape Town.

        :return: Return the phrase that describes present weather conditions.
        :rtype: str
        """
        # call the method to collect json data for the weather in cape town
        json_response = super().call_weather_api() 
        # retrieve the description from the json response by indexing the dictionary
        # put default values if no key found, note its a dict, list & str as seen from the json_response
        # idx 0 for weather since the dict value is the 1st in the list
        description = json_response.get("current", {}).get("weather", [])[0].get("description", "")
        # return the description
        return description

# call method to find the location of selected city - cape town
# comment out coordinates after initial method was called because it does not need repetition       
# coordinates = weather.call_coord_api()

class NewsApiCalls():
    def __init__(self):        
        # put api key in .env file
        # load api key from .env file
        load_dotenv()
        # use try-except defense in a loop to retrieve the API key
        while True:
            # try to fetch the environment variable for news
            # break the loop
            try:
                self.api_key = os.getenv('NEWS_API_KEY')
                print("Got API key")##
                break
            # except if the environment variable was not found
            # continue loop
            # then check the .env file to see it's there
            except KeyError as e:
                print(f"{e} \nNews API key not found in .env file.")
                continue

    def call_news_api(self):
        # select endpoint (everything is the alternative) 
        self.endpoint = 'top-headlines'
        # country for south africa
        self.country = 'za'
        # the category for which you want headlines
        self.category = 'general'
        
        # set the oldest date to 24 hours ago
        # use timedelta() to subtract 24 hours from the current time
        # https://docs.python.org/3/library/datetime.html#timedelta-objects
        # format the result into a str for ISO 8601 format 
        self.latest_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        
        # date & time for newest article allowed
        # get the current time
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes  
        # format the result into a str for ISO 8601 format       
        self.newest_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')        
        
        # 2-letter ISO-639-1 code for desired language you want for articles        
        self.language = 'en'
        # sort search results by popularity in the response
        self.sortBy = 'popularity'

        # construct the newsapi.org API url for SA
        # e.g. GET https://newsapi.org/v2/top-headlines?country=de&category=business&apiKey=4029e8b4afb943f2b44d67ed177bdddf
        # e.g.GET https://newsapi.org/v2/everything?q=apple&from=2024-12-28&to=2024-12-28&sortBy=popularity&apiKey=4029e8b4afb943f2b44d67ed177bdddf
        self.sa_news_api_call = f'https://newsapi.org/v2/{self.endpoint}?country={self.country}&category={self.category}&from={self.latest_time}&to={self.newest_time}&language={self.language}&sortBy={self.sortBy}&apiKey={self.api_key}'
        print("Made API call for SA")##

    # 
    def store_json_response(self):
        # store url in a variable as a json response
        sa_response = requests.get(self.sa_news_api_call)

        # check if the get request was successful
        # parse the JSON content of the response using the .json() method
        try:
            # with a status code 200, the data can be parsed with json()            
            self.sa_json_response = sa_response.json()                        
                        
            # if there are no news results for SA
            if self.sa_json_response.get("totalResults", 0) == 0:
                # save a str stating there are no results for SA
                no_sa_news = "There is no news for South Africa on newsapi.org."
                print(no_sa_news)##
                
                # try doing an api call for the USA's latest news
                try:
                    # construct the newsapi.org API url for USA as a backup       
                    # overwrite country to USA
                    self.country = 'us'
                    self.usa_news_api_call = f'https://newsapi.org/v2/{self.endpoint}?country={self.country}&category={self.category}&from={self.latest_time}&to={self.newest_time}&language={self.language}&sortBy={self.sortBy}&apiKey={self.api_key}'
                    print("Made API call for USA")##

                    # store url in a variable as a json response
                    usa_response = requests.get(self.usa_news_api_call)

                    # with a status code 200, the data can be parsed with json()            
                    self.usa_json_response = usa_response.json()

                    # write latest news for USA to a json file
                    with open("usa_news.txt", "w") as f:
                        json.dump(self.usa_json_response, f, indent=4)
                        print("Wrote latest news for USA to a .txt file.")##

                    # return the feedback that there is no news for SA & the JSON content for USA
                    return no_sa_news, self.usa_json_response
                
                # check if the get request was unsuccessful
                except Exception as e:
                    # print error if unsuccessful request
                    # return None to signal that there's no valid data to work with
                    error_message = f"Unable to retrieve the latest news in USA - Status code:{usa_response.status_code}\n{e}"
                    print(error_message)
                    return None
            
            else:
                # write latest news for SA to a json file
                with open("sa_news.txt", "w") as f:
                    json.dump(self.sa_json_response, f, indent=4)
                    print("Wrote latest news for SA to a .txt file.")##                                                               

                # return the JSON content 
                return self.sa_json_response

        # check if the get request was unsuccessful
        except Exception as e:
            # print error if unsuccessful request
            # return None to signal that there's no valid data to work with
            error_message = f"Unable to retrieve the latest news in SA - Status code:{sa_response.status_code}\n{e}"
            print(error_message)
            return None
        
    def sa_articles(self):
        # number of articles that are popular in SA in the last 24 hours
        num_of_articles = self.sa_json_response.get("totalResults", 0)
        print(f"num_of_articles {num_of_articles}")##
        
        articles = self.sa_json_response.get("articles", [])
        # idx 5 most recently published news articles that are popular in SA
        # get their titles & url
        top_five_articles = articles[:5]
        top_five_article_titles = [article.get("title", "") for article in top_five_articles]
        # use enumerate() to number the 5 titles when printing
        for i, title in enumerate(top_five_article_titles, start=1):
            print(f"{i}. {title}\n")                    
        
        top_five_article_url = [article.get("url", "") for article in top_five_articles]
        # use enumerate() to number the 5 titles when printing
        for i, url in enumerate(top_five_article_url, start=1):
            print(f"({i}). {url}\n") 

        # return the no. of articles, top 5 titles & their 5 urls
        return num_of_articles, top_five_article_titles, top_five_article_url
    
    def usa_articles(self):
        # number of articles that are popular in USA in the last 24 hours
        num_of_articles = self.usa_json_response.get("totalResults", 0)
        print(f"num_of_articles {num_of_articles}")##
        
        articles = self.usa_json_response.get("articles", [])
        # idx 5 most recently published news articles that are popular in USA
        # get their titles & url
        top_five_articles = articles[:5]

        # use list comprehension to get() the title of 5 articles in the list of articles dict
        top_five_article_titles = [article.get("title", "") for article in top_five_articles]
        # use enumerate() to number the 5 titles when printing
        for i, title in enumerate(top_five_article_titles, start=1):
            print(f"{i}. {title}\n")                    
        
        # use list comprehension to get() the url of 5 articles in the list of articles dict
        top_five_article_url = [article.get("url", "") for article in top_five_articles]
        # use enumerate() to number the 5 titles when printing
        for i, url in enumerate(top_five_article_url, start=1):
            print(f"({i}). {url}\n") 

        # return the no. of articles, top 5 titles & their 5 urls
        return num_of_articles, top_five_article_titles, top_five_article_url
        