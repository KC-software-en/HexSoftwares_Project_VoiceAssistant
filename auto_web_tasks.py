# import selenium for automated web searches
from selenium import webdriver

# import re to remove brackets & improve readability from text 
import re

# import By for locating elements in Selenium
from selenium.webdriver.common.by import By

# import WebDriverWait to give YT time to locate title element
# https://selenium-python.readthedocs.io/waits.html#explicit-waits
from selenium.webdriver.support.wait import WebDriverWait

# import expected_conditions
from selenium.webdriver.support import expected_conditions as EC

# import time to give YouTube time to play its videos
import time

###########################################################################
###########################################################################

# create a class to conduct an automated wikipedia search with selenium
class WikiBot():
    def __init__ (self):        
        # initiate webdriver 
        self.driver = webdriver.Edge()
    
    # set query as the search parameter of the search method
    def wiki_search(self, query):
        """A method to search for information on Wikipedia.

        :param query: A search term for Wikipedia
        :type query: str
        """
        #
        self.query = query
        # initiate driver
        self.driver.get(url="https://www.wikipedia.org/")
        self.driver.implicitly_wait(0.5)
        # locate search box by inspecting web page elements & copying xpath
        # https://selenium-python.readthedocs.io/locating-elements.html#locating-by-xpath
        search_box = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        # click on search box
        search_box.click()
        # send query to search box
        search_box.send_keys(query)
        # locate search button 
        search_button = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button/i')
        # click on search button to submit query
        search_button.click()
        # locate the 1st paragraph of the wiki search result by its xpath
        # use .text property to extract the actual text content from web element
        # https://medium.com/hackerdawn/scraping-from-wikipedia-using-python-and-selenium-3d64af60975d
        first_paragraph = self.driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[2]').text        
        # remove brackets containing references from 1st paragraph and replace with empty str         
        first_paragraph = re.sub("[\(\[].*?[\)\]]", "", first_paragraph)
        # close driver
        self.driver.quit()
        # return the text of the 1st paragraph for the search result
        return first_paragraph

# create a class to play a YouTube video
class YouTubeVideo():
    def __init__(self):
        # initiate webdriver 
        self.driver = webdriver.Edge()

    # create a method to calculate the time allowed for the YouTube video to play
    def calculate_video_duration(self, video_duration_text):   
        """Calculate th time allowed for the YouTube video to play.

        :param video_duration_text: The text property of the video duration's xpath.
        :type video_duration_text: str
        :return: Return the time to use as an argument in sleep().
        :rtype: int
        """
        # convert time to seconds
        # split the str at ':' creating a list of sections in the duration    
        duration_sections = video_duration_text.split(":")

        # use try-except block to calculate seconds
        try:            
            # initialise the times in the event some videos don't have certain variable, ensuring no calculation error
            hours, minutes, seconds = 0, 0, 0
            
            # if the video has hours, minutes & seconds
            if len(duration_sections) == 3:
                # assign duration_sections to the tuple
                hours, minutes, seconds = map(int, duration_sections)

            # if the video has minutes & seconds
            elif len(duration_sections) == 2:
                # assign duration_sections to the tuple
                minutes, seconds = map(int, duration_sections)
            
            # if the video has seconds
            elif len(duration_sections) == 1:
                # assign duration_sections to second
                # access the index (the 1st & only number in the list)
                seconds = int(duration_sections[0])

            # print error if the format doe not have sections for the calculations
            else:
                print("Invalid format for duration.")
                # return a default of 30 seconds
                return 30
        
        # exception handling for error before adding the int
        except Exception as e:
            print(f"Error calculating video duration: {e}.")
            # return a default of 30 seconds
            return 30

        # calculate the seconds for the video duration
        video_duration_seconds = (hours * 3600) + (minutes * 60) + seconds
        # add extra time for adverts
        advertisements = 15
        # return the duration to sleep
        return video_duration_seconds + advertisements
        
    # create a method to play the YouTube video
    def play_video(self, query):
        """A method to play the YouTube video.

        :param query: The string input used as the search term in YouTube.
        :type query: str
        """
        # store query param as an instance variable
        self.query = query
        # go to YouTube url search result page, copy url (excluding search term because only that changes)
        # concatenate query to the url
        self.driver.get(url="https://www.youtube.com/results?search_query=" + self.query)
        # locate the title element for the 1st search result by its xpath
        video = self.driver.find_element(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
        # allow time for the element location
        time.sleep(4)
        # wait for results 
        try:
            element = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]/yt-formatted-string'))
            )
        
            # click on the title
            video.click()            
            
            # locate the time element
            video_duration = self.driver.find_element(By.XPATH, '//*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/div[1]/badge-shape/div')
            # extract text property for duration calculation
            video_duration_text = video_duration.text
            calculate_time = self.calculate_video_duration(video_duration_text)
            # use sleep() to allow video to finish playing
            time.sleep(calculate_time)                        
            
        except Exception as e:
            print(f"Error playing the YouTube video.: {e}")
        
        finally:    
            # close driver        
            self.driver.quit()



