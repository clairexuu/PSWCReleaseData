from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()

YEAR = 2025

# --- USER CONFIG ---
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# --- SETUP ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# --- STEP 1: Login ---
driver.get("https://www.wrmd.org/signin")
wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

# --- STEP 2: Go to Patient List Page with specified year ---
wait.until(EC.url_contains("/dashboard"))
print(f"📅 Navigating to year {YEAR}...")
driver.get(f"https://www.wrmd.org/lists?change_year_to={YEAR}")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))
time.sleep(2)  # Give extra time for page to fully load

# --- STEP 3: Determine Total Pages ---
pagination_links = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li a[href^="#"]')
page_numbers = [int(p.text) for p in pagination_links if p.text.strip().isdigit()]
total_pages = max(page_numbers) if page_numbers else 1
print(f"Total pages: {total_pages}")

# Determine page order
page_range = range(1, total_pages + 1)

# --- STEP 4: Loop Through Pages and Check Boxes ---
for page in page_range:
    print(f"Processing page {page}...")

    # Navigate to specific page using URL
    driver.get(f"https://www.wrmd.org/lists?change_year_to={YEAR}&page={page}")

    # Wait for table to fully load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table')))
    time.sleep(2)  # Give extra time for dynamic content to load

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

# --- Done ---
print("All checkboxes on all pages are now checked.")
time.sleep(3)
input("Press Enter to close the browser when finished export")
driver.quit()