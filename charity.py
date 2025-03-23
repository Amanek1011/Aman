import aiohttp
from bs4 import BeautifulSoup

async def get_charity():
    url = 'https://2gis.kg/bishkek/search/%D0%91%D0%BB%D0%B0%D0%B3%D0%BE%D1%82%D0%B2%D0%BE%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D1%84%D0%BE%D0%BD%D0%B4%D1%8B?m=74.6161%2C42.872342%2F11.76'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    sections = soup.find_all('div', class_="_awwm2v")
                    for i in sections:
                        name = i.find('a',class_='_1rehek')
                        view = i.find('span',class_='_oqoid')
                        return name , view

    except Exception as e:
        print(f"Error during request or parsing: {e}")
        return "Произошла ошибка при запросе данных."

