import csv
import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Lire le fichier CSV
with open('utilisateurs.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    users = [row for row in csv_reader]

# URL de la page de connexion iCloud
url = "https://appleid.apple.com/sign-in"
chrome_options = Options()
chrome_options.add_argument("--incognito")

async def process_user(user):
    apple_id = user['apple_id']
    temp_password = user['temp_password']
    a2f_code = user['a2f_code']
    new_password = user['new_password']

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    sleep(5)

    try:
        try:
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))
        except:
            pass

        apple_id_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "account_name_text_field"))
        )
        apple_id_field.send_keys(apple_id)
        apple_id_field.send_keys(Keys.RETURN)
        sleep(5)

        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "password_text_field"))
        )
        password_field.send_keys(temp_password)
        password_field.send_keys(Keys.RETURN)

        a2f_fields = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".form-security-code-input"))
        )

        for i, digit in enumerate(a2f_code):
            a2f_fields[i].send_keys(digit)

        sleep(5)
        try:
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))
        except:
            pass

        current_password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".current-password input"))
        )
        current_password_field.send_keys(temp_password)
        new_password_field1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".new-password input"))
        )
        new_password_field1.send_keys(new_password)

        new_password_field2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".confirm-password input"))
        )
        new_password_field2.send_keys(new_password)
        new_password_field2.send_keys(Keys.RETURN)
        sleep(5)
        try :
            new_password_field2.send_keys(Keys.RETURN)
        except:
            pass
        sleep(5)
        try :
            new_password_field2.send_keys(Keys.RETURN)
        except:
            pass
        sleep(3)

        print(f"Mot de passe changé pour {apple_id}")

        users.remove(user)
        with open('utilisateurs.csv', mode='w', newline='') as file:
            fieldnames = ['apple_id', 'temp_password', 'a2f_code', 'new_password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        print(f"Erreur lors du traitement de {apple_id}: {e}")

    finally:
        driver.quit()

def run_process_user(user):
    asyncio.run(process_user(user))

async def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, run_process_user, user)
            for user in users
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())