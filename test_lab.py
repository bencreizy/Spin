from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
# This keeps the browser open even after the script finishes
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Snap to Right Side
driver.set_window_rect(x=960, y=0, width=960, height=1080)

driver.get("https://gitlab.com/users/sign_in")

print("Status: Resonant. Window locked. Manual intervention ready.")
