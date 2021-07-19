from bs4 import BeautifulSoup
import text2emotion as te
import requests


def get_quote(emotion):
    page = requests.get(
        "http://www.quotationspage.com/random.php")
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(id="content")
    quote = content.find(class_="quote").get_text()

    while (te.get_emotion(quote)[emotion] < 0.9):
        quote = get_quote(emotion)

    return quote
