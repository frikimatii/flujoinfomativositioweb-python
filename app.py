from flask import Flask, render_template, jsonify
import json
import os
from threading import Thread, Lock
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

# Lock para garantizar escritura segura en el archivo JSON
lock = Lock()
filename = 'data.json'

app = Flask(__name__)

# Funciones de scraping
def read_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"infobae": [], "LaNacion": [], "TN": [], "Clarin": []}

def write_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_news(data, source, title, url, img_url, alt_text):
    if data[source] and title == data[source][-1]['title']:
        print(f"La última noticia de {source} es igual a la anterior.")
        return False
    data[source].append({
        'id': len(data[source]) + 1,
        'title': title,
        'url': url,
        'img_url': img_url,
        'alt_text': alt_text,
        'source': source
    })
    return True

def scrape_tn():
    base_url = 'https://tn.com.ar/ultimas-noticias/'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        link = soup.find('a', class_='card__image')
        img = soup.find('img', class_='image')

        if link and img:
            url = urljoin(base_url, link.get('href'))
            title = link.get('title')
            img_url = img.get('src')
            alt_text = img.get('alt')

            with lock:
                data = read_json(filename)
                if update_news(data, 'TN', title, url, img_url, alt_text):
                    write_json(data, filename)
                    print(f"Noticia de TN guardada: {title}")

    except requests.RequestException as e:
        print(f"Error al obtener la noticia de TN: {e}")

def scrape_infobae():
    base_url = 'https://www.infobae.com/ultimas-noticias/'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        link = soup.find('a', class_='feed-list-card')
        img = soup.find('img', class_='feed-list-image')
        titulo = soup.find('h2', class_='feed-list-card-headline-lean')

        if link and img and titulo:
            url = urljoin(base_url, link.get('href'))
            img_url = re.sub(r'\s\d{3}w$', '', img.get('src'))
            alt_text = img.get('alt')
            title = titulo.text.strip()

            with lock:
                data = read_json(filename)
                if update_news(data, 'infobae', title, url, img_url, alt_text):
                    write_json(data, filename)
                    print(f"Noticia de InfoBae guardada: {title}")

    except requests.RequestException as e:
        print(f"Error al obtener la noticia de InfoBae: {e}")

def scrape_lanacion():
    base_url = 'https://www.lanacion.com.ar/ultimas-noticias/'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        container = soup.find('article', class_='mod-article')

        if container:
            title_element = container.find('h2', class_='com-title')
            title = title_element.text.strip() if title_element else None
            link = container.find('a', class_='com-link')
            url = urljoin(base_url, link.get('href')) if link else None
            img = container.find('img', class_='com-image')
            img_url = re.sub(r'\s\d{3}w$', '', img.get('src')) if img else None
            alt_text = img.get('alt') if img else None

            if title and url and img_url and alt_text:
                with lock:
                    data = read_json(filename)
                    if update_news(data, 'LaNacion', title, url, img_url, alt_text):
                        write_json(data, filename)
                        print(f"Noticia de La Nación guardada: {title}")

    except requests.RequestException as e:
        print(f"Error al obtener la noticia de La Nación: {e}")

def scrape_clarin():
    base_url = 'https://www.clarin.com/ultimo-momento/'
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article = soup.find('article', class_='sc-ca635c60-0 dJfTkK')

        if article:
            title_element = article.find('h2')
            title = title_element.text.strip() if title_element else None
            link = article.find('a')
            url = urljoin(base_url, link.get('href')) if link else None
            img = article.find('img')
            img_url = img.get('src') if img else None
            alt_text = img.get('alt') if img else None

            if title and url and img_url and alt_text:
                with lock:
                    data = read_json(filename)
                    if update_news(data, 'Clarin', title, url, img_url, alt_text):
                        write_json(data, filename)
                        print(f"Noticia de Clarín guardada: {title}")

    except requests.RequestException as e:
        print(f"Error al obtener la noticia de Clarín: {e}")

def main_scraper():
    while True:
        threads = [
            Thread(target=scrape_tn),
            Thread(target=scrape_infobae),
            Thread(target=scrape_lanacion),
            Thread(target=scrape_clarin)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        print("Esperando 1 minuto para la próxima actualización...")
        time.sleep(60)

# Rutas de la aplicación Flask
@app.route('/')
def index():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except FileNotFoundError:
        news = {"infobae": [], "LaNacion": [], "TN": [], "Clarin": []}
    return render_template('index.html', news=news)

@app.route('/api/news')
def api_news():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except FileNotFoundError:
        news = {"infobae": [], "LaNacion": [], "TN": [], "Clarin": []}
    return jsonify(news)

@app.route('/data.json')
def get_data():
    # Aquí deberías cargar y devolver los datos del archivo data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    # Crear y ejecutar un hilo para el scraper
    scraper_thread = Thread(target=main_scraper)
    scraper_thread.daemon = True
    scraper_thread.start()

    # Ejecutar la aplicación Flask
    app.run(debug=True)
