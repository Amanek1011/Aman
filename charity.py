from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

charity_data = [
    {"name": "Международный комитет Красного Креста",
     "description": 'Наша работа по защите людей, пострадавших от конфликта', "address": "Улица Панфилова, 144",
     "website": "https://www.icrc.org/en"},
    {"name": "Алтын уя", "description": "Максатыбыз, тилегибиз, аракетибиз – ОКУБАГАН БАЛА КАЛБАСЫН!",
     "address": "Улица Мичурина, 80",
     "website": "http://altynuya.org/"},
    {"name": "Элим Барсынбы?",
     "description": "Основная миссия фонда оказание помощи всем нуждающим людям проживающим в Кыргызской Республике.",
     "address": "Улица Исакеева, 18/3",
     "website": "https://www.instagram.com/elimbarsynby_official/"},
    {"name": "Фонтан жизни",
     "description": "Мы — местная благотворительная организация, целью которой является предоставление комплексной помощи (физической, эмоциональной, духовной) бездомным в Бишкеке, Кыргызстан",
     "address": "Улица Васильева, 163",
     "website": "https://www.fountainoflife.kg/"},
    {"name": "SOS",
     "description": "SOS Детские Деревни – негосударственная социальная организация, на протяжении 60 лет защищающая права и интересы детей.",
     "address": "Улица Минина, 47",
     "website": "https://www.soskyrgyzstan.kg/"},
    {"name": "Taiwan Fund for Children and Families",
     "description": "ОБФ «Тайваньский Благотворительный Фонд» Мы заботимся о будущем детей уже сегодня",
     "address": "Улица Юдахина, 65/1",
     "website": "https://www.instagram.com/tfcfkyrgyzstan/"},
    {"name": "Коломто", "description": "Приют для бездомных людей", "address": "Проспект Жибек-Жолу, 413",
     "website": "Нету страницы"},
    {"name": "World share",
     "description": "Международная неправительственная организация по оказанию помощи и развитию.",
     "address": "Улица Ибраимова, 115/4",
     "website": "http://worldshare.kg/"},
    {"name": "Help the Children-SKD",
     "description": "«Help the Children – SKD» оказывает помощь детям, страдающим онкологическими, гематологическими и иммунологическими заболеваниями и их семьям.",
     "address": "4-й микрорайон, 26/1",
     "website": "https://www.deti.kg/"},
    {"name": "Бабушка Эдопшн",
     "description": "Фонд оказывающий финансовую поддержку одиноким пожилым людям, живущим в крайней нищете.",
     "address": "Московская улица, 39",
     "website": "https://babushkaadoption.org/ru/%d0%b3%d0%bb%d0%b0%d0%b2%d0%bd%d0%b0%d1%8f/"}
]

async def get_charity(index: int):
    if index < len(charity_data):
        charity = charity_data[index]
        charity_info = (f"🏠 Название: {charity['name']}\n"
                        f"📌 Описание: {charity['description']}\n"
                        f"📍 Адрес: {charity['address']}\n"
                        f"🌐 Сайт: {charity['website']}")

        buttons = []
        if index + 1 < len(charity_data):
            buttons.append([InlineKeyboardButton(text="Еще", callback_data=f"next:{index + 1}")])

        markup = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

        return charity_info, markup
    return None, None


