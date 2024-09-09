from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

CHROMEDRIVER_PATH = "chromedriver.exe"

def configure_driver():
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    chrome_options.add_argument("--log-level=3")  # Reduce logging
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging port
    
    # Configure the WebDriver using the specified chromedriver executable path
    service = Service(CHROMEDRIVER_PATH)  # Update with your actual path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_website(website):
    print("Starting headless browser for scraping...")
    driver = configure_driver()
    try:
        driver.get(website)
        print("Navigated to the website. Waiting for captcha to solve (if any)...")
        
        # You can add WebDriverWait if needed to wait for elements
        
        print("Scraping page content...")
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error occurred: {e}")
        return ""
    finally:
        driver.quit()  # Make sure to close the driver to free resources

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
