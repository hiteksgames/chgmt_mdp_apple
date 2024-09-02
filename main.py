import csv
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Lire le fichier CSV
with open('utilisateurs.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    users = [row for row in csv_reader]

# Configurer Selenium pour utiliser Chrome
driver = webdriver.Chrome()

# URL de la page de connexion iCloud
url = "https://appleid.apple.com/sign-in"

for user in users:
    apple_id = user['apple_id']
    temp_password = user['temp_password']
    a2f_code = user['a2f_code']
    new_password = user['new_password']

    # Démarrer le navigateur et ouvrir la page de connexion
    driver.get(url)

    sleep(5)

    try:
        try:
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))
        except:
            pass

        # Attendre que le champ de l'identifiant Apple soit disponible
        apple_id_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "account_name_text_field"))
        )
        apple_id_field.send_keys(apple_id)
        apple_id_field.send_keys(Keys.RETURN)

        sleep(5)

        # Attendre l'affichage du champ du mot de passe
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "password_text_field"))
        )
        password_field.send_keys(temp_password)
        password_field.send_keys(Keys.RETURN)

        # Attendre l'affichage des champs du code A2F
        a2f_fields = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".form-security-code-input"))
        )

        # Entrer le code A2F chiffre par chiffre
        for i, digit in enumerate(a2f_code):
            a2f_fields[i].send_keys(digit)

        sleep(5)

        try:
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe"))
        except:
            pass

        # Attendre l'apparition du champ pour le mot de passe actuel
        current_password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".current-password input"))
        )
        current_password_field.send_keys(temp_password)

        # Attendre l'apparition du champ pour le nouveau mot de passe
        new_password_field1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".new-password input"))
        )
        new_password_field1.send_keys(new_password)

        # Attendre l'apparition du champ pour confirmer le nouveau mot de passe
        new_password_field2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".confirm-password input"))
        )
        new_password_field2.send_keys(new_password)

        sleep(5)
        # Soumettre le formulaire en appuyant sur Entrée dans le champ de confirmation
        new_password_field2.send_keys(Keys.RETURN)

        sleep(5)
        new_password_field2.send_keys(Keys.RETURN)

        print(f"Mot de passe changé pour {apple_id}")

        sleep(15)

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Erreur lors du traitement de {apple_id}: {e}")
        sleep(5)
        driver.quit()
        continue

    finally:
        driver.switch_to.default_content()

# Fermer le navigateur
driver.quit()