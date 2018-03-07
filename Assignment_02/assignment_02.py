from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
import numpy as np
import random
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import bs4

row_data = []
row_head = []
data = []
def random_delay():
    time.sleep(random.uniform(0.5, 5))
driver = webdriver.Chrome(executable_path=r'C:\Users\Class2018\Desktop\BIA 660\chromedriver.exe')

def extract_stats_data(driver):
    # your code here, you remember how to use BeautifulSoup, yes? It's soup time.
    # let me show you something cool
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(data_html, "html5lib")
    soup.thead
    wait = WebDriverWait(driver, 10)
    normal_delay = random.normalvariate(2, 0.5)
    for t in soup.thead.findAll('th'):
        t.replace('▲', '').replace('▼', '')
        row_head.append(t.text)
        random_delay()
    soup.tbody
    for t in soup.tbody.findAll('td'):
        t.replace('▲', '').replace('▼', '')
        row_data.append(t.text)
        random.delay()
    data = pd.DataFrame(row_data, columns=row_head)
    pass

def scrape_all(driver):
    # may any
    id_of_pagination_div = "pagination"
    pagination_div = driver.find_element_by_id(id_of_pagination_div)
    buttons = pagination_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(buttons, "html5lib")
    while soup.fieldset[-1] == "paginationWidget-next":
        extract_stats_data(driver)
        random_delay()
        ActionChains(driver).move_to_element(soup.fieldset[-1]).click().perform()
        random_delay()
    if soup.fieldset[-1] != "paginationWidget-next":
        extract_stats_data(driver)
        random_delay()
        ActionChains(driver).move_to_element(soup.fieldset[-1]).click().perform()
        random_delay()
        pass
    pass

def random_delay():
    time.sleep(random.uniform(0.5, 5))


def open_page():
    driver.get('http://www.mlb.com')
    random_delay()
    pass

def select_element_by_text(elements, text):
    for e in elements:
        if e.text == text:
            return e
    return None

def get_2017_site():
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    random_delay()
    stats_header_bar.click()
    random_delay()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    random_delay()
    stats_line_items[0].click()
    random_delay()

    [li.text for li in stats_line_items]

    reg_season_stats_2017 = select_element_by_text(stats_line_items, '2017 Regular Season Stats')
    random_delay()
    ActionChains(driver).move_to_element(reg_season_stats_2017).click().perform()
    random_delay()

    pass


def get_2015_site():
    stats_header_bar = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item--stats')
    random_delay()
    stats_header_bar.click()
    random_delay()
    stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
    random_delay()
    stats_line_items[0].click()
    random_delay()

    [li.text for li in stats_line_items]

    reg_season_stats_2017 = select_element_by_text(stats_line_items, '2015 Regular Season Stats')
    random_delay()
    ActionChains(driver).move_to_element(reg_season_stats_2017).click().perform()
    random_delay()

    pass


def select_AL():
    id_of_div = "sp_hitting-1"
    al_div = driver.find_element_by_id(id_of_div)
    options = al_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(options, "html5lib")
    for label in soup.findall('fieldset'):
        if label.value == "AL":
            ActionChains(driver).move_to_element(label).click().perform
            random_delay()
        pass
    pass


def select_NL():
    id_of_div = "sp_hitting-1"
    al_div = driver.find_element_by_id(id_of_div)
    options = al_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(options, "html5lib")
    for label in soup.findall('fieldset'):
        if label.value == "NL":
            ActionChains(driver).move_to_element(label).click().perform
            random_delay()
        pass
    pass


def select_teams():
    id_of_div = "top_nav"
    top = driver.find_element_by_id(id_of_div)
    options = top.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(options, "html5lib")
    for t in soup.ul.findAll('li'):
        if t.id == "st_parent":
            ActionChains(driver).move_to_element(t).click().perform
            random_delay()
        pass
    pass

def select_HR():
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(data_html, "html5lib")
    for t in soup.thead.findAll('th'):
        if t.index == 10:
            ActionChains(driver).move_to_element(t).click().perform
            random_delay()
            pass
    pass

def answer_question_one():
    select_teams()
    select_HR()
    scrape_all()
    answer = data[0][0]
    np.savetxt("answer_1.csv", answer, header = None)
    pass

def select_first_inning():
    id_of_div = "sp_hitting-1"
    al_div = driver.find_element_by_id(id_of_div)
    options = al_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(options, "html5lib")
    for label in soup.findall('fieldset'):
        if label.value == "sp_hitting_hitting_splits":
            ActionChains(driver).move_to_element(label).click().perform
            random_delay()
            first_inning = select_element_by_text(label, 'First Inning')
            random_delay()
            ActionChains(driver).move_to_element(first_inning).click().perform()
            random_delay()

def scrape_and_answer_question_2():
    select_AL()
    random_delay()
    scrape_all()
    random_delay()
    AL_averages = data.columns('HR')
    AL_total = 0
    AL_count = 0

    for t in AL_averages:
        AL_total = AL_total + t
        count = count + 1
        pass

    AL_average = AL_total / count
    answer_one = ['2a', 'AL', AL_average]

    select_NL()
    scrape_all()
    NL_averages = data.columns('HR')
    NL_total = 0
    NL_count = 0

    for t in AL_averages:
        NL_total = NL_total + t
        count = count + 1
        pass

    NL_average = NL_total / count
    answer_two = ['2a', 'NL', AL_average]

    if AL_average > NL_average:
        answer_2a = answer_one
        pass
    else:
        answer_2a = answer_two
        pass

    select_first_inning()
    random_delay()
    scrape_all()
    random_delay()

    select_AL()
    scrape_all()
    AL_averages = data.columns('HR')
    AL_total = 0
    AL_count = 0

    for t in AL_averages:
        AL_total = AL_total + t
        count = count + 1
        pass

    AL_average = AL_total / count
    answer_three = ['2a', 'AL', AL_average]

    select_NL()
    scrape_all()
    NL_averages = data.columns('HR')
    NL_total = 0
    NL_count = 0

    for t in AL_averages:
        NL_total = NL_total + t
        count = count + 1
        pass

    NL_average = NL_total / count
    answer_four = ['2a', 'NL', AL_average]

    if AL_average > NL_average:
        answer_2b = answer_three
        pass
    else:
        answer_2b = answer_four
        pass

    Question_two_answers = [answer_2a , answer_2b]
    np.savetxt("answer_2.csv", Question_two_answers, header=None)
    pass

def get_full_name():
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(data_html, "html5lib")
    for x in soup.tbody.findAll('td'):
        if x.index == 1:
        ActionChains(driver).move_to_element(x).click().perform()
        random_delay()
        pass

    id_of_div = "player-vitals"
    al_div = driver.find_element_by_id(id_of_div)
    options = al_div.get_attribute('innerHTML')
    soup = bs4.BeasutifulSoup(options, "html5lib")
    for span in soup.findall('h1'):
        player_name = span.text
    return player_name

def answer_question_three():
    scrape_all()
    random_delay()
    team = data[0][3]
    pos = data[0][4]
    name = get_full_name()
    answer = [name, team, pos]
    np.savetxt("answer_3.csv", answer, header=None)
    pass

def main():
    open_page()
    get_2015_site()

    answer_question_one(data)

    scrape_and_answer_question_2()

    get_2017_site()
    answer_question_three()

    answer_question_five(data)
    scrape_all()
    answer_question_four(data)
if __name__ == '__main__':
    main()