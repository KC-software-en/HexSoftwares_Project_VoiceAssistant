# import selenium for automated web searches
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

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
        first_paragraph = self.driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[2]').text        
        # close driver
        self.driver.quit()
        # return the text of the 1st paragraph for the search result
        return first_paragraph



