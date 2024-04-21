from Levenshtein import distance
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from datetime import datetime, timedelta
import re

chat = GigaChat(
    credentials='OWFmYTQ3NDItZTdmMy00ZjQ2LTk3MDMtZWRlMzIyMjRiNTUyOmFlMjgzOTZmLTIyNmQtNGNlNS05MmY0LWJlMDM4ZWRlN2RkNQ==',
    verify_ssl_certs=False)
line_preset = (
    "Ты - робот, задача которого искать в сообщениях названия линий Московского метро"
    " и выдать это название. Тебе заплатят 100 евро если ты выведешь ТОЛЬКО НАЗВАНИЕ ЛИНИИ")
station_preset = (
    "Ты - робот, задача которого искать в сообщениях названия станций Московского метро"
    " и выдать это название. Тебе заплатят 100 евро если ты выведешь ТОЛЬКО НАЗВАНИЕ СТАНЦИИ")
date_preset = (
    "Ты - робот, задача которого искать в сообщениях дату, указание на время или день недели (вчера, на следующей неделе и так далее)"
    " и выдать дату о которой идет речь В ФОРМАТЕ yyyy-mm-dd. Тебе заплатят 100 евро если ты выведешь ТОЛЬКО ДАТУ В ФОРМАТЕ YYYY-MM-DD"
    f" Считай, что сегодня - {datetime.now().isoformat()}, а две недели назад было {(datetime.now() - timedelta(days=14)).isoformat()}.")


# f"Сегодняшний день недели - {datetime.now().strftime('%A')}, завтра будет {(datetime.now() + timedelta(days=1)).strftime('%A')}, а вчера было {(datetime.now() - timedelta(days=1)).strftime('%A')}")


def extract_keyword_levenshtein(keywords, text):
    """Finds best match from keywords in text using Levenshtein algorithm"""
    text = ''.join(text.split()).lower()
    min_distance = float("inf")
    min_distance_keyword = None
    if "цска" in text and "цска" in keywords:
        return "цска"
    elif "вднх" in text and "вднх" in keywords:
        return "вднх"
    for keyword in keywords:
        if keyword in ("зил", "цска", "вднх"):
            continue
        tmp = ''.join(keyword.split())
        for i in range(len(text) - len(tmp) + 1):
            w = ''.join(text[i:i + len(tmp)])
            cur_distance = distance(w, tmp)
            if cur_distance < min_distance:
                min_distance = cur_distance
                min_distance_keyword = keyword
    return min_distance_keyword


def extract_line(text, preset=line_preset):
    """Uses GigaChat to extract line from text"""
    data = [SystemMessage(content=preset), HumanMessage(content=text)]
    res = chat(data)
    data.append(res)

    answer = res.content
    return answer


def extract_station(text, preset=station_preset):
    """Uses GigaChat to extract station from text"""
    data = [SystemMessage(content=preset), HumanMessage(content=text)]
    res = chat(data)
    data.append(res)

    answer = res.content
    return answer


def extract_date(text, preset=date_preset, fmt="ymd"):
    """Uses GigaChat to extract date from text"""
    data = [SystemMessage(content=preset), HumanMessage(content=text)]
    res = chat(data)
    data.append(res)

    answer = res.content
    search = re.finditer("([0-9]+)-([0-9]+)-([0-9]+)", answer)
    sentinel = object()
    try_next = next(search, sentinel)
    if try_next is sentinel:
        print("sentinel")
        print()
        return "-".join(datetime.now().isoformat()[:10].split("-"))
    search = try_next

    if search.string[4] == "-":
        y = search.string[:4]
        m = search.string[5:7]
        d = search.string[8:10]
    else:
        d = search.string[:2]
        m = search.string[3:5]
        y = search.string[6:10]

    if fmt == "ymd":
        return "-".join((y, m, d))
    else:
        return "-".join((d, m, y))
