import sys
import os
from json import load
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def read_config():
    application_path = ""  # Prevent an error from being raised
    try:
        if getattr(sys, 'frozen', False):  # For proper work with PyInstaller
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(application_path, "config.json")

        with open(config_path, 'r', encoding='UTF-8') as file:
            return load(file)
    except Exception as e:
        print(f"Error reading config.json: {e}")
        return None


def format_tr_data(tr_element):
    tr_list = tr_element.text.split('\n')[1:-1]
    tr_list = [list_item.strip() for list_item in tr_list]

    if len(tr_list[1]) < 5:
        tr_list[1] = '0' + tr_list[1]

    date, start, end, pair, group, discipline, lesson_type, room, teacher = tr_list

    return (f'{date: <23}{start: <7}{end: <10}{pair: <5}{group: <9}'
            f'{discipline: <48}{lesson_type: <4}{room: <9}{teacher: <35}')


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if headless_launch:
        options.add_argument('--headless')  # Don't open any browser windows

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    if date_from:
        date_from_element = (driver.find_element
                             (By.XPATH, "/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/input[1]"))
        date_from_element.clear()
        date_from_element.send_keys(date_from)

    if date_to:
        date_to_element = (driver.find_element
                           (By.XPATH, "/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/input[4]"))
        date_to_element.clear()
        date_to_element.send_keys(date_to)

    dropdown_element = driver.find_element(By.XPATH, "//*[@id='Name1']")
    form_button = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/input")

    select = Select(dropdown_element)  # Create a Select instance
    select.select_by_visible_text(group)  # Select the desired option by its value

    form_button.click()  # Click on the "Cформировать" button

    soup = BeautifulSoup(driver.page_source, 'lxml')

    tr_elements_list = soup.find_all('tr', {'class': 'reportitem'})

    driver.quit()  # Cleanup and close the web driver

    print(f'{headers[0]: <23}{headers[1]: <7}{headers[2]: <10}{headers[3]: <5}{headers[4]: <9}{headers[5]: <48}'
          f'{headers[6]: <4}{headers[7]: <9}{headers[8]: <35}')  # Print table headers

    #   Дата   Начало    Окончание   Пара    Группа    Дисциплина   Тип     Ауд     Преподаватель
    for tr_element in tr_elements_list:
        print(format_tr_data(tr_element))


if __name__ == '__main__':
    config = read_config()
    default_values = {
        "headless_launch": False,
        "window_size": "mode 160, 300",
        "date_from": "",
        "date_to": "",
        "headers": [
            "Дата",
            "Начало",
            "Окончание",
            "Пара",
            "Группа",
            "Дисциплина",
            "Тип",
            "Ауд",
            "Преподаватель"
            ],
        "url": "raspisanie.bf.pstu.ru",
        "group": "ПОВТ-23д"
    }

    # Use default values if values from config file are empty
    headless_launch = config.get('headless_launch', default_values['headless_launch'])
    window_size = config.get('window_size', default_values['window_size']) or default_values['window_size']
    os.system(window_size)  # Apply the window size
    date_from = config.get('date_from', default_values['date_from']) or default_values['date_from']
    date_to = config.get('date_to', default_values['date_to']) or default_values['date_to']
    headers = config.get('headers', default_values['headers']) or default_values['headers']
    url = config.get('url', default_values['url']) or default_values['url']
    group = config.get('group', default_values['group']) or default_values['group']

    main()
    input('\nPress any key to exit...\n')
