import requests 
import json

from lxml import html
from pathlib import Path

import config


def extract_info(url):
    resp = requests.get(
        url, headers={ 'User-Agent': config.USER_AGENT }
    )
    resp.raise_for_status()

    tree = html.fromstring(resp.content)
    container = tree.xpath(f'//div[@class="sample-hero-waveform-container"]')[0]

    # Все данные о семпле находятся в этом аттрибуте
    # Из кучи имеющихся данных выбираем только url и название файла
    s = json.loads(container.attrib['data-react-props'])['sample']
    return s['sample_mp3_url'], s['sample_original_filename']


def download(url):
    url, file_name = extract_info(url)
    out_path = Path(config.OUTPUT_FOLDER) / file_name
    out_path.parent.mkdir(exist_ok=True)

    print(f"Загрузка", file_name)

    resp = requests.get(
        url, headers={ 'Referer': 'https://samplefocus.com/' }, stream=True
    )
    resp.raise_for_status()

    block_size = 1000 # 1 KB
    with open(out_path, 'wb') as f:
        for data in resp.iter_content(block_size):
            f.write(data)


def main():
    if not config.SAMPLE_URLS:
        print('Нечего загружать')
        return

    for u in config.SAMPLE_URLS:
        download(u)


if __name__ == '__main__':
    main()

