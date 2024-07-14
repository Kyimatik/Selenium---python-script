import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule
from selenium_stealth import stealth

# Параметры для Telegram
TOKEN = "&"
group_id = "&"

# Функция для отправки сообщения в Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": group_id,
        "text": text
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")  # Запускаем браузер в максимальном размере
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

    
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver

def job():
    driver = create_driver()
    target_months = ["August", "September"]
    target_year = "2024"

    try:
        driver.get("any website")
        time.sleep(1)

        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button') and text()='OK']"))
        )
        ok_button.click()

        email_input = driver.find_element(By.ID, "user_email")
        email_input.clear()
        email_input.send_keys("toktobaevemil06@gmail.com")

        password_input = driver.find_element(By.ID, "user_password")
        password_input.clear()
        password_input.send_keys("AIZHAN2003")

        label = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='policy_confirmed']"))
        )
        label.click()
        password_input.send_keys(Keys.ENTER)
        time.sleep(2)

        scroll_element = driver.find_element(By.XPATH, '//*[@id="appointments_consulate_address"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", scroll_element)
        time.sleep(2)

        calendar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "appointments_consulate_appointment_date"))
        )
        calendar_button.click()
        send_message("Календарь открыт.")

        while True:
            month_year_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "ui-datepicker-title"))
            )
            month_year_text = month_year_element.text
            send_message(f"Текущий месяц и год: {month_year_text}")
            month, year = month_year_text.split()
            if month in target_months and year == target_year:
                break
            next_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-next")
            next_button.click()
            time.sleep(1)

        available_dates = driver.find_elements(By.XPATH, "//a[contains(@class, 'ui-state-default')]")
        date_selected = False
        for date in available_dates:
            day = int(date.text)
            if month == "September" and day > 15:
                send_message(f"Дата {date.text} {month} превышает 15 сентября. Пропускаем.")
                continue

            date.click()
            send_message(f"Дата {date.text} {month} выбрана.")
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "appointments_consulate_appointment_time")))
            time_select = Select(driver.find_element(By.ID, "appointments_consulate_appointment_time"))
            time_select_options = time_select.options
            if len(time_select_options) > 1:
                time_select.select_by_index(1)  # Выбор первого доступного времени (кроме "Выберите время")
                send_message("Время выбрано.")
                submit_button = driver.find_element(By.ID, "appointments_submit")
                submit_button.click()
                send_message("Кнопка 'Перезаписаться' нажата.")
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button alert')]"))
                )
                confirm_button.click()
                send_message("Кнопка 'Подтвердить' нажата.")
                date_selected = True
                break
            elif len(time_select_options) == 1:
                time_select.select_by_index(0)
                send_message("Время выбрано.")
                submit_button = driver.find_element(By.ID, "appointments_submit")
                submit_button.click()
                send_message("Кнопка 'Перезаписаться' нажата.")
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button alert')]"))
                )
                confirm_button.click()
                send_message("Кнопка 'Подтвердить' нажата.")
                break
            else:
                send_message(f"Нет доступного времени для даты {date.text} {month}.")
        if not date_selected:
            send_message(f"Нет доступного времени для всех дат в {month}.")
    except Exception as e:
        send_message(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

# Планирование задачи
schedule.every(120).seconds.do(job)

# Бесконечный цикл для выполнения задач
# Бесконечный цикл для выполнения задач
while True:
    schedule.run_pending()
    time.sleep(1)

# test.py code 
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""
Не уходи смиренно, в сумрак вечной тьмы,
Пусть тлеет бесконечность в яростном закате.
Пылает гнев на то, как гаснет смертный мир,
Пусть мудрецы твердят, что прав лишь тьмы покой.
И не разжечь уж тлеющий костёр.

"""
