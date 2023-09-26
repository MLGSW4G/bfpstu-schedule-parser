import sys
import os
from json import load
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def read_config():
    try:
        if getattr(sys, 'frozen', False):  # For proper work with PyInstaller
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(application_path, "config.json")

        with open(config_path, 'r', encoding='UTF-8') as file:
            config = load(file)
        return config
    except Exception as e:
        print(f"Error reading config.json: {e}")
        return None


def create_dict_tr(tr):
    dict_tr = {
        tr[0]: tr[1:]
    }
    return dict_tr


def tr_to_dict_tr(dict_tr):
    for key, value in dict_tr.items():
        return (f'{key: <23}{value[0]: <7}{value[1]: <10}{value[2]: <5}{value[3]: <9}{value[4]: <48}{value[5]: <4}'
                f'{value[6]: <9}{value[7]: <35}')


def tr_to_list(soup, number):
    tr = soup.find_all('tr', {'class': 'reportitem'})[number].text
    tr_list = tr.split('\n')[1:-1]

    tr_list = [list_item.strip() for list_item in tr_list]  # Strip all the elements in the list

    if len(tr_list[1]) < 5:  # If the time is less than 10:00, add a zero to its beginning
        tr_list[1] = '0' + tr_list[1]

    return tr_list


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument('--headless')  # Headless launch (No browser window opened)
    driver = webdriver.Chrome(options=options)

    driver.get(url)  # Load the web page

    if date_from != "":
        date_from_element = (driver.find_element
                             (By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/input[1]"))
        date_from_element.clear()
        date_from_element.send_keys(date_from)

    if date_to != "":
        date_to_element = (driver.find_element
                           (By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[1]/td[2]/input[4]"))
        date_to_element.clear()
        date_to_element.send_keys(date_to)

    dropdown_element = driver.find_element(By.XPATH, "//*[@id='Name1']")
    form_button = driver.find_element(By.XPATH,
                                      "/html/body/form/table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/input")

    select = Select(dropdown_element)  # Create a Select instance
    select.select_by_visible_text(group)  # Select the desired option by its value

    form_button.click()  # Click on the "Cформировать" button

    soup = BeautifulSoup(driver.page_source, 'lxml')

    tr_elements_list = soup.find_all('tr', {'class': 'reportitem'})

    driver.quit()  # Cleanup and close the web driver

    print(f'{headers[0]: <23}{headers[1]: <7}{headers[2]: <10}{headers[3]: <5}{headers[4]: <9}{headers[5]: <48}'
          f'{headers[6]: <4}{headers[7]: <9}{headers[8]: <35}')  # Print table headers

    #   Дата   Начало    Окончание   Пара    Группа    Дисциплина   Тип     Ауд     Преподаватель
    for tr in tr_elements_list:
        tr_list = tr.text.split('\n')[1:-1]
        tr_list = [list_item.strip() for list_item in tr_list]
        if len(tr_list[1]) < 5:
            tr_list[1] = '0' + tr_list[1]
        print(tr_to_dict_tr(create_dict_tr(tr_list)))


if __name__ == '__main__':
    config = read_config()
    default_values = {
        "window_size": "mode 150, 300",
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
    window_size = config.get('window_size', default_values['window_size']) or default_values['window_size']
    date_from = config.get('date_from', default_values['date_from']) or default_values['date_from']
    date_to = config.get('date_to', default_values['date_to']) or default_values['date_to']
    headers = config.get('headers', default_values['headers']) or default_values['headers']
    url = config.get('url', default_values['url']) or default_values['url']
    group = config.get('group', default_values['group']) or default_values['group']

    os.system(window_size)
    main()
    input('\nPress any key to exit...\n')
