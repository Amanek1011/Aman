import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


async def get_news_today():
    current_data = datetime.now().strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={current_data}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    sections = soup.find_all('div', class_="Tag--articles")

                    if not sections:
                        print("No articles found with class 'Tag--articles'.")
                        return "Не удалось найти новости."

                    news_list = []

                    for tag in sections:
                        tags = tag.find_all('div', class_="Tag--article")
                        if not tags:
                            print("No articles found in the section.")
                            return "В разделе не найдено ни одной статьи."

                        for i in tags:
                            try:
                                site = i.find('a', class_='ArticleItem--name')['href']
                                title = i.find('a', class_='ArticleItem--name').text.strip()
                                time = i.find('div', class_='ArticleItem--time').text.strip()
                                news_list.append(f'🕑 {time} | {title}'
                                                 f'  {site}')
                            except Exception as e:
                                print(f"Error extracting article data: {e}")

                    if not news_list:
                        print("No news articles were successfully parsed.")
                        return "Новости не найдены."

                    return "\n\n".join(news_list)

                else:
                    print(f"Failed to retrieve the page. Status code: {response.status}")
                    return "Ошибка при загрузке новостей."

    except Exception as e:
        print(f"Error during request or parsing: {e}")
        return "Произошла ошибка при запросе данных."



async def get_data_today():
    current_data = datetime.now().strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={current_data}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    data = soup.find('span',class_='PaginatorDate--today-text').text
                    return f' {data.replace('  ','')}'
                else:
                    print('Не получилось получить дату')
    except Exception as e:
        print(e)


async def get_news_yesterday():
    current_data = datetime.now()
    yesterday = current_data - timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={formatted_yesterday}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    sections = soup.find_all('div', class_="Tag--articles")

                    if not sections:
                        print("No articles found with class 'Tag--articles'.")
                        return "Не удалось найти новости."

                    news_list = []

                    for tag in sections:
                        tags = tag.find_all('div', class_="Tag--article")
                        if not tags:
                            print("No articles found in the section.")
                            return "В разделе не найдено ни одной статьи."

                        for i in tags:
                            try:
                                site = i.find('a', class_='ArticleItem--name')['href']
                                title = i.find('a', class_='ArticleItem--name').text.strip()
                                time = i.find('div', class_='ArticleItem--time').text.strip()
                                news_list.append(f'🕑 {time} | {title}'
                                                 f'  {site}')
                            except Exception as e:
                                print(f"Error extracting article data: {e}")

                    if not news_list:
                        print("No news articles were successfully parsed.")
                        return "Новости не найдены."

                    return "\n\n".join(news_list)

                else:
                    print(f"Failed to retrieve the page. Status code: {response.status}")
                    return "Ошибка при загрузке новостей."

    except Exception as e:
        print(f"Error during request or parsing: {e}")
        return "Произошла ошибка при запросе данных."

async def get_data_yesterday():
    current_data = datetime.now()
    yesterday = current_data - timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={formatted_yesterday}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    data = soup.find('span',class_='PaginatorDate--today-text').text
                    return f' {data.replace('  ','')}'
                else:
                    print('Не получилось получить дату')
    except Exception as e:
        print(e)

async def send_long_message(message, text):
    max_length = 4096
    while len(text) > max_length:
        await message.answer(text[:max_length], disable_web_page_preview=True)
        text = text[max_length:]
    if text:
        await message.answer(text, disable_web_page_preview=True)
