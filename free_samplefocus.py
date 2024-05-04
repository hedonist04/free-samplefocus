import requests 
import json
import random

from lxml import html
from pathlib import Path


# URL семплов для загрузки
SAMPLE_URLS = []

# Теперь требует User-Agent
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' 
]

# Папка для загруженных файлов
OUTPUT_DIR = 'output'


def extract_sample_info(sample_url):
    resp = requests.get(
        sample_url, headers={ 'User-Agent': random.choice(USER_AGENTS) }
    )
    resp.raise_for_status()

    tree = html.fromstring(resp.content)
    container = tree.xpath(f'//div[@class="sample-hero-waveform-container"]')[0]
    # Все данные о семпле находятся в этом аттрибуте
    props = container.attrib['data-react-props']

    return json.loads(props)['sample']


def download_sample_audio(mp3_url, out_path):
    resp = requests.get(
        mp3_url, headers={ 'Referer': 'https://samplefocus.com/' }, stream=True
    )
    resp.raise_for_status()

    # 1 KB
    block_size = 1000
    with open(out_path, 'wb') as f:
        for data in resp.iter_content(block_size):
            f.write(data)


def main():
    if not SAMPLE_URLS:
        print('Нечего загружать')
        return

    counter = 1
    for url in SAMPLE_URLS:
        sample_info = extract_sample_info(url)

        mp3_url = sample_info['sample_mp3_url']
        file_name = sample_info['name'] + '.mp3'
        out_path = Path(OUTPUT_DIR) / file_name

        print('[{}] загружаем в "{}"'.format(counter, out_path))
        out_path.parent.mkdir(exist_ok=True)
        download_sample_audio(mp3_url, out_path)

        counter += 1


if __name__ == '__main__':
    main()

