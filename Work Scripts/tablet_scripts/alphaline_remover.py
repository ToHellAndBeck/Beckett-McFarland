from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def wait_for_element_to_be_clickable(driver, locator):
    return WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator))

def click_button(driver, locator):
    try:
        button = wait_for_element_to_be_clickable(driver, locator)
        if button:
            button.click()
    except Exception as e:
        print(f"Error clicking button: {locator}", e)

def login(driver, email, password):
    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.ENTER)

def hover_and_click_element(driver, target_title):
    # Find the element to hover over
    item_locator = (By.XPATH, f"//div[@id='explorerListbox']//span[@title='{target_title}']")
    try:
        item = wait_for_element_to_be_clickable(driver, item_locator)

        
        ActionChains(driver).move_to_element(item).perform()
        print(f"Hovered over item with title '{target_title}'")
    except Exception as e:
        print(f"Error hovering over item with title '{target_title}': {e}")

    # Click on the hovered element
    try:
        # Wait for the element to be clickable again after the hover
        item = wait_for_element_to_be_clickable(driver, item_locator)
        item.click()
        print(f"Clicked on item with title '{target_title}'")
    except Exception as e:
        print(f"Error clicking item with title '{target_title}': {e}")

def hover_and_click_elements_after_all_devices(driver, target_titles):
    # Find and click on 'All Devices' button
    all_devices_button_locator = (By.XPATH, "//span[text()='All Devices']")
    all_devices_button = wait_for_element_to_be_clickable(driver, all_devices_button_locator)
    all_devices_button.click()

    # Wait for the list to load
    loading_locator = (By.XPATH, '//span[contains(@title, "218417")][@style="display: block;"]')
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(loading_locator))

    # Hover over and click on elements after 'All Devices' based on provided titles
    for target_title in target_titles:
        hover_and_click_element(driver, target_title)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

mass_labor_url = 'https://alpha-line.appspot.com/manage_devices'
driver.get(mass_labor_url)

email_address = 'rollout.admins@wachter.com'
password = 'Wachter10'

# Login
login(driver, email_address, password)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def wait_for_element_to_be_clickable(driver, locator):
    return WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator))

def click_button(driver, locator):
    try:
        button = wait_for_element_to_be_clickable(driver, locator)
        if button:
            button.click()
    except Exception as e:
        print(f"Error clicking button: {locator}", e)

def login(driver, email, password):
    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.ENTER)

def hover_and_click_element(driver, target_title):
    # Find the element to hover over
    item_locator = (By.XPATH, f"//div[@id='explorerListbox']//span[@title='{target_title}']")
    try:
        item = wait_for_element_to_be_clickable(driver, item_locator)

        
        ActionChains(driver).move_to_element(item).perform()
        print(f"Hovered over item with title '{target_title}'")
    except Exception as e:
        print(f"Error hovering over item with title '{target_title}': {e}")

    # Click on the hovered element
    try:
        # Wait for the element to be clickable again after the hover
        item = wait_for_element_to_be_clickable(driver, item_locator)
        item.click()
        print(f"Clicked on item with title '{target_title}'")
    except Exception as e:
        print(f"Error clicking item with title '{target_title}': {e}")

def hover_and_click_elements_after_all_devices(driver, target_titles):
    # Find and click on 'All Devices' button
    all_devices_button_locator = (By.XPATH, "//span[text()='All Devices']")
    all_devices_button = wait_for_element_to_be_clickable(driver, all_devices_button_locator)
    all_devices_button.click()

    # Wait for the list to load
    loading_locator = (By.XPATH, '//span[contains(@title, "218417")][@style="display: block;"]')
    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(loading_locator))

    # Hover over and click on elements after 'All Devices' based on provided titles
    for target_title in target_titles:
        hover_and_click_element(driver, target_title)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

mass_labor_url = 'https://alpha-line.appspot.com/manage_devices'
driver.get(mass_labor_url)

email_address = 'rollout.admins@wachter.com'
password = 'Wachter10'

# Login
login(driver, email_address, password)

print("Clicking on 'Manage Devices' button")
manage_devices_button_locator = (By.XPATH, '//a[text()="Manage Devices"]')
click_button(driver, manage_devices_button_locator)

# User input: Provide multiple phone numbers separated by commas
user_input_numbers = "2632768, 2128470"  
numbers_to_click = [number.strip() for number in user_input_numbers.split(',')]

# Click on elements after clicking on 'All Devices'
hover_and_click_elements_after_all_devices(driver, numbers_to_click)



time.sleep(60)
# Close the browser window
driver.quit()
