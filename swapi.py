from pathlib import Path
import requests


class APIRequester():
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url=None):
        if url is None:
            url = f'{self.base_url}/'
        else:
            url = f'{self.base_url}{url}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')


class SWRequester(APIRequester):
    def get_sw_categories(self):
        response = self.get()
        if response is not None:
            categories = response.json().keys()
            return categories
        else:
            return None

    def get_sw_info(self, sw_type):
        url = f'/{sw_type}/'
        response = self.get(url)
        return response.text


def save_sw_data():
    sw_requester = SWRequester('https://swapi.dev/api')
    Path("data").mkdir(exist_ok=True)
    categories = sw_requester.get_sw_categories()
    if categories is not None:
        for category in categories:
            response = sw_requester.get_sw_info(category)
            with open(f'data/{category}.txt', 'w', encoding='utf-8') as f:
                f.write(response)


save_sw_data()
