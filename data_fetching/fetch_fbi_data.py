import requests
import psycopg2
from psycopg2.extras import execute_batch
import os
import pandas as pd
import re
from bs4 import BeautifulSoup


def fetch_data():
    url = 'https://api.fbi.gov/wanted/v1/list'
    response = requests.get(url)
    return response.json()['items']


def clean_data(items):
    cleaned_items = []
    for item in items:
        cleaned_item = {
            'title': item.get('title', 'No Title'),
            'description': item.get('description', 'No Description'),
            'url': item.get('url', 'No URL'),
            'reward_text': item.get('reward_text', 'No Reward'),
            'poster_url': item.get('images', [{}])[0].get('original', 'No Poster URL') if item.get('images') else 'No Poster URL',
            'subjects': ', '.join(item.get('subjects', ['No Subjects'])),
            'publication': item.get('publication', 'No Publication Date'),
            'nationality': item.get('nationality', 'No Nationality'),
            'hair': item.get('hair', 'No Hair Description'),
            'eyes': item.get('eyes', 'No Eye Description'),
            'height': item.get('height', 'No Height'),
            'weight': item.get('weight', 'No Weight'),
            'sex': item.get('sex', 'No Sex'),
            'scars_and_marks': item.get('scars_and_marks', 'No Scars and Marks'),
            'remarks': clean_html(item.get('remarks', 'No Remarks')),
        }
        cleaned_items.append(cleaned_item)
    return cleaned_items


def clean_html(raw_html):
    if raw_html is None:
        return 'No Remarks'
    else:
        # Remove HTML tags using BeautifulSoup
        cleaned_text = BeautifulSoup(raw_html, "html.parser").get_text()
        return cleaned_text


def store_data(items):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='post123',
        host='localhost'
    )
    cursor = conn.cursor()
    query = """
    INSERT INTO fbi_wanted (title, description, url, reward_text, poster_url, subjects, publication, nationality, hair, eyes, height, weight, sex, scars_and_marks, remarks)
    VALUES (%(title)s, %(description)s, %(url)s, %(reward_text)s, %(poster_url)s, %(subjects)s, %(publication)s, %(nationality)s, %(hair)s, %(eyes)s, %(height)s, %(weight)s, %(sex)s, %(scars_and_marks)s, %(remarks)s)
    ON CONFLICT (uid) DO NOTHING;
    """
    execute_batch(cursor, query, items)
    conn.commit()
    cursor.close()
    conn.close()


def save_to_dataframe(items):
    df = pd.DataFrame(items)
    df.to_csv('cleaned_fbi_wanted_data.csv', index=False)
    print("Data saved to cleaned_fbi_wanted_data.csv")
    return df


if __name__ == '__main__':
    data = fetch_data()
    cleaned_data = clean_data(data)
    store_data(cleaned_data)
    df = save_to_dataframe(cleaned_data)
