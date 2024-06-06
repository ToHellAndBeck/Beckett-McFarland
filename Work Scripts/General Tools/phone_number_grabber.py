from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_phone_numbers(file_path):
    print("Starting WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    with open(file_path, 'r') as file:
        for number in file:
            number = number.strip()
            url = f"https://www.walmart.com/store/{number}"
            print(f"Accessing URL: {url}")
            driver.get(url)
            
            # Wait for the page to load
            print("Waiting for page to load...")
            time.sleep(20)  # Increase or decrease based on your internet speed

            try:
                print("Trying to find phone number...")
                # Extract phone number
                phone_number = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div/span[4]/a").text
                print(f"Store {number} Phone: {phone_number}")
            except Exception as e:
                print(f"Failed to find phone number for store {number}: {e}")

    print("Closing WebDriver...")
    driver.quit()

# Example usage
get_phone_numbers(r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\sites.txt")
