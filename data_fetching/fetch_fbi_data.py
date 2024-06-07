import requests
import psycopg2
from psycopg2.extras import execute_batch
import os


def fetch_data():
    url = 'https://api.fbi.gov/wanted/v1/list'
    response = requests.get(url)
    return response.json()['items']


def clean_data(items):
    cleaned_items = []
    for item in items:
        cleaned_items.append({
            'title': item.get('title'),
            'description': item.get('description'),
            'url': item.get('url'),
            'reward_text': item.get('reward_text'),
            'poster_url': item.get('images', [{}])[0].get('original', '') if item.get('images') else '',
            'subjects': ', '.join(item.get('subjects', [])),
            'publication': item.get('publication'),
            'nationality': item.get('nationality'),
            'hair': item.get('hair'),
            'eyes': item.get('eyes'),
            'height': item.get('height'),
            'weight': item.get('weight'),
            'sex': item.get('sex'),
            'scars_and_marks': item.get('scars_and_marks'),
            'remarks': item.get('remarks'),
        })
    return cleaned_items


def store_data(items):
    conn = psycopg2.connect(
        dbname='fbi_db',
        user='postgres',
        password='password',
        host='db'
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


if __name__ == '__main__':
    data = fetch_data()
    cleaned_data = clean_data(data)
    store_data(cleaned_data)
