from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS
import threading

class Language:

    def __init__(self, name: str, rating: str, diff: str, pos2024: str, pos2023: str) -> None:
        self.name = name
        self.rating = rating
        self.diff = diff
        self.pos2024 = pos2024
        self.pos2023 = pos2023
        self.link = ""

    def gather_aditional_info(self):
        for res in DDGS().text(f'{self.name} programming language', max_results=1):
            self.link = res["href"]

    def __str__(self) -> str:
        return f"2024 position: {self.pos2024} Language: {self.name}, rating: {self.rating} (diff: {self.diff}), 2023 position: {self.pos2023}<br> <a href={self.link}> Click this note to learn more about {self.name}</a><br><br>"

r = requests.get('https://www.tiobe.com/tiobe-index/')
html_doc = r.text

def row_cells(row): return [cell.contents for cell in row]

soup = BeautifulSoup(html_doc, 'html5lib')

languages = []

table = soup.find(attrs={"id": "top20"})
content = table.find("tbody")
rows =  content.find_all("tr")
for row in rows:
    data = row.find_all("td")
    languages.append(
        Language(
            data[4].text,
            data[5].text,
            data[6].text,
            data[0].text,
            data[1].text,
        )
    )

lck = threading.Lock()
n = 0
def run(target):
    target()
    lck.acquire()
    global n
    n += 1
    print(f"{n:3}", end="\r")
    lck.release()

for l in languages:
    t = threading.Thread(target=run, args=[l.gather_aditional_info])
    t.start()

while(True):
    lck.acquire()
    if(n == len(languages)): break
    lck.release()



with open("output.md", "w") as f:
    f.write("<H1>The Most Popular Programming Languages</H1> <p>Release date: 02.03.2024<br>Author: Mateusz Roman</p>")
    for l in languages:
        f.write(str(l))