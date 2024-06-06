from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta


arrivalTime = input("When did get to work?: ")
jobNumber = input('Job Number: ')
laborHours = input('How many hours did you work each day?: ')
if jobNumber == 'ROLLOUT':
    jobPhase = '9999'
else:
    jobPhase = '0000'
def wait_for_element_to_be_clickable(driver, xpath):
    try:
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return button
    except Exception as e:
        print(xpath, e)
 
def click_button(driver, xpath):
    try:
        button = wait_for_element_to_be_clickable(driver, xpath)
        if button:
            button.click()
    except Exception as e:
        print(xpath, e)
 
def input_text(driver, element_id, text):
    try:
        # Find the email input field by its ID
        email_input = driver.find_element(By.ID, element_id)
        # Clear the input field if needed
        email_input.clear()
        # Input the email address
        email_input.send_keys(text)
        email_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"An error occurred: {e}")
 
# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
mass_labor_url = 'https://trust.wachter.com/Labor/MassEditProxy.aspx'
 
employee_dropdown_xpath = '//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_cboEmployees_Input"]'
rcb_list_xpath = '/html/body/form/div[1]/div/div/ul'
email_element_id = 'i0116'
dropdown_input_id = 'ctl00_cphMain_RoundContainer1_MassEditControl1_cboEmployees_Input'
driver.get(mass_labor_url)
login_button_xpath = '//*[@id="slide-5-layer-8"]'
click_button(driver, login_button_xpath)
wachter_login_button_xpath = '//*[@id="ctl00_cphMain_ssoLoginControl_btnSingleSignOnLogin"]'
click_button(driver, wachter_login_button_xpath)
next_button_path = '//*[@id="idSIButton9"]'
wait_for_element_to_be_clickable(driver, next_button_path)
email_address = 'beckett.mcfarland@wachter.com'
input_text(driver, email_element_id, email_address)
sign_in_button_xpath = '//*[@id="idSIButton9"]'
wait_for_element_to_be_clickable(driver, sign_in_button_xpath)
password_element_id = 'i0118'
password = 'Ozymandias99!'
input_text(driver, password_element_id, password)
stay_signed_in_button_xpath = '//*[@id="idSIButton9"]'
click_button(driver, stay_signed_in_button_xpath)
select_employee_button_xpath = '//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_btnSelectEmployee"]'
select_employee_button = wait_for_element_to_be_clickable(driver, select_employee_button_xpath)
select_employee_dropdown_xpath = '//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_cboEmployees_Arrow"]'
element_to_hover_over = driver.find_element(By.XPATH, select_employee_dropdown_xpath)
hover = ActionChains(driver).move_to_element(element_to_hover_over)
hover.perform()
element_to_hover_over.click()
time.sleep(3)
employee_to_select_xpath = '//*[contains(text(), "Beckett")]'
employee_element = driver.find_element(By.XPATH, employee_to_select_xpath)
employee_element.click()

# Simulate pressing Enter without targeting a specific element
element = driver.find_element(By.XPATH, '//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_btnSelectEmployee"]')
element.send_keys(Keys.RETURN)

click_button(driver, select_employee_button_xpath)
input_text(driver, 'ctl00_cphMain_RoundContainer1_MassEditControl1_txtRowsToAdd', '5')
click_button(driver, '//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_btnAddTenRows"]')
time.sleep(5)
'''
for values in range(23):
 # Add a small delay between key presses
    driver.switch_to.active_element.send_keys(Keys.TAB)
'''
today = datetime.now()
days_until_monday = (today.weekday() - 0) % 7
monday_date = today - timedelta(days=days_until_monday)
start_date = monday_date
time.sleep(5)
for i in range(5):
    # Update the date for each iteration
    current_date = start_date + timedelta(days=i)

    # Update the control number for each iteration
    control_number = 4 + i

    # Construct the XPATHs with the updated date and control_number
    date_xpath = f'//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_grdMassLaborProxyControl_ctl00_ctl{control_number:02d}_tzArrivalDate_TZDatePicker_dateInput"]'
    time_xpath = f'//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_grdMassLaborProxyControl_ctl00_ctl{control_number:02d}_tzArrivalDate_TZTimePicker_dateInput"]'
    job_number_xpath = f'//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_grdMassLaborProxyControl_ctl00_ctl{control_number:02d}_txtJobNumber"]'
    job_phase_xpath = f'//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_grdMassLaborProxyControl_ctl00_ctl{control_number:02d}_txtPhase"]'
    labor_hours_xpath = f'//*[@id="ctl00_cphMain_RoundContainer1_MassEditControl1_grdMassLaborProxyControl_ctl00_ctl{control_number:02d}_tstbMinutesLabor"]'

    # Perform the actions with the constructed XPATHs
    driver.find_element(By.XPATH, date_xpath).clear()
    driver.find_element(By.XPATH, date_xpath).send_keys(current_date.strftime('%m/%d/%Y'))

    driver.find_element(By.XPATH, time_xpath).clear()
    driver.find_element(By.XPATH, time_xpath).send_keys(arrivalTime)

    driver.find_element(By.XPATH, job_number_xpath).clear()
    driver.find_element(By.XPATH, job_number_xpath).send_keys(jobNumber)

    driver.find_element(By.XPATH, job_phase_xpath).clear()
    driver.find_element(By.XPATH, job_phase_xpath).send_keys(jobPhase)

    driver.find_element(By.XPATH, labor_hours_xpath).clear()
    driver.find_element(By.XPATH, labor_hours_xpath).send_keys(laborHours)
time.sleep(60)
