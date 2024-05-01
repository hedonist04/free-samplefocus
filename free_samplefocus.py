import requests 
import json

from lxml import html
from pathlib import Path


# URL семплов для загрузки
SAMPLE_URLS = []

# Теперь требует User-Agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' 

# Папка для загруженных файлов
OUTPUT_FOLDER = 'output'


def extract_info(url):
    resp = requests.get(
        url, headers={ 'User-Agent': USER_AGENT }
    )
    resp.raise_for_status()

    tree = html.fromstring(resp.content)
    container = tree.xpath(f'//div[@class="sample-hero-waveform-container"]')[0]

    # Все данные о семпле находятся в этом аттрибуте
    # Из кучи имеющихся данных выбираем только url и название файла
    s = json.loads(container.attrib['data-react-props'])['sample']
    return s['sample_mp3_url'], s['sample_original_filename']


def download_audio(audio_url, file_name):
    out_path = Path(OUTPUT_FOLDER) / file_name
    out_path.parent.mkdir(exist_ok=True)

    resp = requests.get(
        audio_url, headers={ 'Referer': 'https://samplefocus.com/' }, stream=True
    )
    resp.raise_for_status()

    block_size = 1000 # 1 KB
    with open(out_path, 'wb') as f:
        for data in resp.iter_content(block_size):
            f.write(data)


def main():
    if not SAMPLE_URLS:
        print('Нечего загружать')
        return

    for u in SAMPLE_URLS:
        print('Извлечение информации о файле из', u)
        audio_url, file_name = extract_info(u)
        print(f'Найдено {audio_url=} {file_name=}')

        print('Загрузка файла...')
        download_audio(audio_url, file_name)


if __name__ == '__main__':
    main()

