!pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Kullanıcı bilgileri
USERNAME = "xxxxxxxxxxx"
PASSWORD = "xxxxxxxxxxxxxx"

# Instagram giriş URL'si
INSTAGRAM_URL = "https://www.instagram.com"

# Selenium WebDriver'ı başlat
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Arka planda çalıştırmak için yorum satırı yap
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def login():
    driver.get(INSTAGRAM_URL)
    time.sleep(3)

    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Giriş sonrası bekleme
    time.sleep(5)


def get_follow_list(url):
    driver.get(url)
    time.sleep(5)

    try:
        # "Takipçi / Takip edilen" listesinin yüklenmesini bekle
        scroll_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] ul")))
    except:
        print(f"❌ {url} yüklenirken hata oluştu!")
        return set()

    last_height, height = 0, 1

    while last_height != height:
        last_height = height
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(2)
        height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)

    users = [user.text.split("\n")[0] for user in scroll_box.find_elements(By.TAG_NAME, "li")]
    return set(users)


def find_non_followers():
    login()

    following_url = f"{INSTAGRAM_URL}/{USERNAME}/following/"
    followers_url = f"{INSTAGRAM_URL}/{USERNAME}/followers/"

    following = get_follow_list(following_url)
    followers = get_follow_list(followers_url)

    non_followers = following - followers

    print("🔎 Seni takip etmeyenler:")
    for user in non_followers:
        print(user)

    driver.quit()


if __name__ == "__main__":
    find_non_followers()
