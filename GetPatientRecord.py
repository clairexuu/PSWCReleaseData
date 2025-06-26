from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time


def change_patient_year(driver, year):
    print(f"📅 Changing patient year to {year}...")
    wait = WebDriverWait(driver, 10)

    # Wait for the select dropdown to appear
    year_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "change_year_to")))

    # Use Select to choose the year
    Select(year_dropdown).select_by_value(str(year))

    # Click the "Change Year" button
    change_button = driver.find_element(By.CSS_SELECTOR, 'form#change-year input[type="submit"]')
    change_button.click()

    # Wait for page to reload (e.g., URL or table content changes)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))
    print(f"✅ Changed to year {year}.")

# --- USER CONFIG ---
EMAIL = "xinyix26@uw.edu"
PASSWORD = "DataCX1"

# --- SETUP ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# --- STEP 1: Login ---
driver.get("https://www.wrmd.org/signin")
wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

# --- STEP 2: Go to Patient List Page ---
wait.until(EC.url_contains("/dashboard"))
driver.get("https://www.wrmd.org/lists")
# change_patient_year(driver, 2024)  # or any other year
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))

# --- STEP 3: Determine Total Pages ---
time.sleep(2)
pagination_links = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li a[href^="#"]')
page_numbers = [int(p.text) for p in pagination_links if p.text.strip().isdigit()]
total_pages = max(page_numbers)
print(f"Total pages: {total_pages}")

# --- STEP 4: Loop Through Pages and Check Boxes ---
for page in range(1, total_pages + 1):
    print(f"Processing page {page}...")

    # Wait for table to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))
    time.sleep(1)

    # Check all checkboxes on the current page
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"][name="patient"]')
    print(f"  Found {len(checkboxes)} checkboxes.")
    for checkbox in checkboxes:
        try:
            if checkbox.is_displayed() and checkbox.is_enabled():
                if not checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(0.1)  # give time for the UI to register the click
                    # Double-check: if still not selected, click again
                    if not checkbox.is_selected():
                        driver.execute_script("arguments[0].click();", checkbox)
                        print("    🔁 Retried checkbox click")
        except Exception as e:
            print(f"    ⚠️ Failed to click a checkbox: {e}")

    # Go to next page, if not last
    if page < total_pages:
        next_page = driver.find_element(By.CSS_SELECTOR, f'ul.pagination li a[href="#"]')
        pages = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li a[href^="#"]')
        for p in pages:
            if p.text.strip() == str(page + 1):
                driver.execute_script("arguments[0].click();", p)
                break

        # Wait for the next page to load
        time.sleep(1)

# --- Done ---
print("All checkboxes on all pages are now checked.")
time.sleep(3)
input("Press Enter to close the browser when finished export")
driver.quit()