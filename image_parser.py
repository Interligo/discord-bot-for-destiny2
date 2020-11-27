import requests
from bs4 import BeautifulSoup as bs


URL = 'http://babenki.info/siski/7487-krasivaya-golaya-grud-78-foto.html'


def get_images():
    """Function parsing shared link to find photos."""
    session = requests.Session()
    response = session.get(URL)

    image_list = []

    if response.status_code == 200:
        soup = bs(response.content, "lxml")
        photos = soup.find_all('a')

        for photo in photos:
            url_photo = photo.find('img')

            try:
                link = url_photo['src']

                if link.endswith(('.jpg', '.png')):
                    pass
                else:
                    link = link[(link.find('uploads') - 1):(len(link) - 12)]

                image_list.append(link)
            except TypeError:
                pass

    else:
        return 'Сайт не отвечает на запросы.'

    return image_list
