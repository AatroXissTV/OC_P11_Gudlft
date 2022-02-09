# functional_test.py
# created 09/02/2022 at 10:10 by Antoine 'AatroXiss' BEAUDESSON
# last modified 09/02/2022 at 10:10 by Antoine 'AatroXiss' BEAUDESSON

""" functional_test.py

To do:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.16"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# local application imports
import server

# other imports

# constants

SERVICE = Service(ChromeDriverManager().install(), log_path='tests/functional_test/chromedriver.log')  # noqa


def test_hp_complete_path():
    """
    Test a complete Happy Path of a user.
        - The user get to the homepage
        - The user logs in
        - The user is logged in and can see the future competitions
        - The user select a competition a book a place
        - The user successfully book a place
        - The user logs out

    """

    # configs
    driver = webdriver.Chrome(service=SERVICE)

    # Get index page
    driver.get('http://127.0.0.1:5000/')
    driver.implicitly_wait(2)

    # Login with a user
    email = server.load_clubs()[0]['email']
    login = driver.find_element(By.NAME, 'email')
    login.send_keys(email)
    login.submit()
    driver.implicitly_wait(2)

    # Verify if the user is logged in
    assert ("Welcome, " + email) in driver.find_element(By.TAG_NAME, 'h2').text

    # Select a competition
    select_comp = driver.find_element(By.LINK_TEXT, 'Book Places')
    select_comp.click()
    driver.implicitly_wait(2)

    # verify if the user is in the book place page
    assert ('Spring Festival') in driver.find_element(By.TAG_NAME, 'h2').text

    # book a place
    book = driver.find_element(By.NAME, 'places')
    book.send_keys('1')
    book.submit()
    driver.implicitly_wait(2)

    # assert 'Great-booking complete!' in driver.find_element(By.XPATH, '/html/body/ul[1]/li[1]')  # noqa

    # Logout
    logout = driver.find_element(By.LINK_TEXT, 'Logout')
    logout.click()
    driver.implicitly_wait(2)

    # Verify if the user is logged out
    assert 'GUDLFT Registration' in driver.title

    # Close the browser
    driver.quit()
