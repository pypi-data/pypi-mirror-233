from bs4 import BeautifulSoup
from selenium import webdriver
import selenium

def static_value(value):
    def return_function(html_object):
        return value
    return return_function

def does_html_object_exist(attributes, object_type):
    def return_function(html_object):
        if get_element_with_attributes(attributes)(html_object).find(object_type) is not None:
            return 1
        return 0
    return return_function

def get_text_of_element_with_attributes(attributes, remove_strings=[]):
    def return_function(html_object):
        return_string = get_element_with_attributes(attributes)(html_object).text
        for remove_string in remove_strings:
            return_string = return_string.replace(remove_string, '')
        return return_string
    return return_function

def get_url_of_element_with_attributes(attributes):
    def return_function(html_object):
        return get_element_with_attributes(attributes)(html_object).find('a')['href']
    return return_function

def get_text_of_element_with_type(type_name):
    def return_function(html_object):
        return get_element_with_type(type_name)(html_object).text
    return return_function

def get_element_with_type(type_name):
    def return_function(html_object):
        return html_object.find(type_name)
    return return_function

def get_element_with_attributes(attributes):
    def return_function(html_object):
        return html_object.find(attrs=attributes)
    return return_function

def get_tr_of_table_with_id(table_id):
    def return_function(soup):
        return soup.find(id=table_id).find("tbody").find_all("tr")
    return return_function

def get_tr_of_stats_table():
    def return_function(soup):
        return soup.find(attrs={'class': 'stats_table'}).find('tbody').find_all('tr')
    return return_function

def row_has_link(html_object):
    return html_object.find("a") is not None

def fetch_soup_from_page(url):
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1200x600')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            page = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except selenium.common.exceptions.TimeoutException:
            print("Failing url: url")
            print("Timed out loading page, trying again")
        except selenium.common.exceptions.WebDriverException:
            print("failing url: " + str(url))
            print("Web Driver Error, trying again")
