import re
from time import sleep
import random
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import argparse
import datetime

import selenium
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def clean_text(text):
    text = re.sub(r';+', ',', text)
    return text


def clean_mark(text):
    if text.endswith('k'):
        text = float(text[:-1]) * 1000
    return int(text)


def clean_date(text):
    for fmt in ('%d %b, %H:%M', '%d %b %Y, %H:%M'):
        try:
            date = datetime.datetime.strptime(text, fmt)
            if date.year == 1900:
                date = date.replace(year=2022)
            return date.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            pass
    raise ValueError(f'No valid date format for {text} found')


def parse_url(url):
    chunk_suffix = random.randint(0, 100000)
    jokes_dict = dict()
    last_i = 0

    ops = webdriver.ChromeOptions()
    ops.add_argument('headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=ops)
    action = webdriver.ActionChains(driver)

    driver.get(url)

    print(f'chunk_suffix={chunk_suffix}')

    for _ in range(100000):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.posts-list.lm-list-container')))

        posts_list = driver \
            .find_element(By.CSS_SELECTOR, '.posts-list.lm-list-container') \
            .find_elements(By.CSS_SELECTOR, '.card.card-body.border.p-2.px-1.px-sm-3.post-container')

        for i in range(last_i, len(posts_list)):

            joke_obj = posts_list[i]

            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView();", joke_obj)

            # Text & date
            try:
                joke_id = joke_obj.id
                joke_text = joke_obj.find_element(By.CSS_SELECTOR, ".post-text").text
                joke_text = clean_text(joke_text)

                joke_date = joke_obj.find_element(By.CSS_SELECTOR, '.text-muted.m-0').text
                joke_date = clean_date(joke_date)
            except (NoSuchElementException, StaleElementReferenceException):
                continue

            if joke_id in jokes_dict:
                continue
            # Mark
            try:
                joke_mark = joke_obj.find_element(By.CSS_SELECTOR, '.uil-corner-up-right').find_element(By.XPATH, '..').text
                joke_mark = clean_mark(joke_mark)
            except (NoSuchElementException, StaleElementReferenceException):
                joke_mark = 0

            if len(joke_text) > 0:
                jokes_dict[joke_id] = (joke_id, joke_text, joke_date, joke_mark)
            sleep(random.random())

        last_i = i
        print(f'\r{len(jokes_dict)}', end="")
        pd.DataFrame(jokes_dict.values(), columns=['id', 'joke_text', 'joke_date', 'joke_mark']) \
            .to_csv(f'../data/parsed-stat-dataset/parsed_chunk_{chunk_suffix}.csv',
                    index=False, sep=';')

        # Wait next button and click
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-light.border.lm-button.py-1.min-width-220px'))).click()

        sleep(random.random() + 3)

    print(f'Final length = {len(jokes_dict)}')
    driver.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Input url for site')

    parser.add_argument('--urls', type=str, nargs='+', help='url for site')
    args = parser.parse_args()

    for url in args.urls:
        print(url)
        try:
            parse_url(url)
        except TimeoutException:
            print(f' jokes parsed.')

