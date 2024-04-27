from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def test_selenium():
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get('http://localhost:8501')

    assert "Streamlit" in browser.title

    username = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.ID, "text_input_1"))
    )
    username.send_keys('username')

    password = browser.find_element(By.ID, 'text_input_2')
    password.send_keys('username' + Keys.RETURN)

    time.sleep(3)

    browser.refresh()

    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "p"))
    )
    elements = browser.find_elements(By.TAG_NAME, 'p')

    logout_button = None
    for e in elements:
        if (e.text == 'Logout'):
            logout_button = e

    assert logout_button.is_displayed()

    elements = browser.find_elements(By.TAG_NAME, 'p')

    menu_item_tierlist = None
    for e in elements:
        if (e.text == 'Tierlist'):
            menu_item_tierlist = e

    menu_item_tierlist.click()

    # time.sleep(3)

    # add_category_button = None
    # for e in elements:
    #     if (e.text == 'Add category'):
    #         add_category_button = e

    # assert add_category_button.is_displayed()

    # add_category_button.click()

    # name_category = browser.find_element(By.ID, 'text_input_9')
    # name_category.send_keys('test category' + Keys.TAB + Keys.RETURN)
