# pip install google pymupdf selenium

import base64
import json
import tempfile
import threading

import fitz
import requests
from googlesearch import search
from selenium.webdriver.support.wait import WebDriverWait


def f(string):
    ret = ""
    i = 0
    u = False
    while i < len(string):
        if i < len(string) - 1 and string[i:i+2] == "__":
            i += 2
            ret += "\u001b[0m" if u else "\u001b[4m"
            u = not u
        else:
            ret += string[i]
            i += 1
    return ret

def re(type, url, headers=None, data=None):
    if type == "POST":
        r = requests.post(url, headers=headers, data=data)
    elif type == "GET":
        r = requests.get(url, headers=headers, data=data)
    print(r, r.text)
    return json.loads(r.text)

_input = []
_i = 0
__input = input
def input(string):
    global _i
    if _i < len(_input):
        print(string, end="")
        _i += 1
        return _input[_i - 1]
    return __input(string)


token = input("Token (or none to generate one): ")

if token == "":
    r = re("POST", "https://accounts.spotify.com/api/token", headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, data={
        "grant_type": "client_credentials",
        "client_id": input("ID: "),
        "client_secret": input("Secret: ")
    })
    token = r["access_token"]

instrument = input("Instrument (e.g. drum tab): ")

tracks = []

r = re("GET", f"https://api.spotify.com/v1/albums/{input('Album ID: ')}/tracks", headers={
    "Authorization": f"Bearer {token}"
})
for track in r["items"]:
    for artist in track["artists"]:
        s = "songsterr " + artist["name"] + " " + track["name"] + " " + instrument
        response = list(search(s, num=10, stop=10, pause=0))
        print(response)
        for result in response:
            action = input(f("Found (for " + s + "): " + result + ". [__A__ccept/__N__ext/__M__ove on]?")).upper()
            if action == "A":
                break
            elif action == "N":
                continue
            elif action == "M":
                action = None
                break
            else:
                error
        if action is not None:
            tracks.append(result)
print(tracks)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re as regex

lock = threading.Lock()

def download_songsterr(url):
    print(f"Downloading {url}...")

    chrome_options = Options()
    chrome_options.binary_location = "./chrome-linux64/chrome"
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')  # sometimes helps too
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0")
    chrome_options.add_argument("--window-size=1100,1080")

    temp_dir = tempfile.mkdtemp()
    import os
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")


    driver = webdriver.Chrome(
        service=Service("./chromedriver-linux64/chromedriver", log_path="./chromedriver.log"),
        options=chrome_options,
    )
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "tablature"))
    )

    script = open("single.js", "r").read()
    driver.execute_async_script(script)
    result = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        # You can add options like landscape, paperWidth, paperHeight, etc.
    })

    logs = driver.get_log('browser')
    for entry in logs:
        print(entry)

    pdf_data = base64.b64decode(result['data'])

    # Save PDF to file
    with lock:
        if not os.path.exists("out"):
            os.mkdir("out")
    name = regex.compile(r"https:\/\/www\.songsterr\.com\/a\/wsa\/(.+)-s[0-9]*")
    name = name.search(url).groups()[0]
    print(f"Saving to {name}")
    with open("out/" + name + ".pdf", "wb") as f:
        f.write(pdf_data)
    if not os.path.exists(f"out/{name}"):
        os.mkdir(f"out/{name}")
    pdf_file = fitz.open("out/" + name + ".pdf")
    print(f"No. pages: {len(pdf_file)}")
    for page_number in range(len(pdf_file)):
        page = pdf_file[page_number]
        pix = page.get_pixmap(dpi=200)  # You can change the DPI
        pix.save("out/" + name + f"/{name}-{page_number}.png")

    print("PDF saved as output.pdf")


from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(download_songsterr, tracks)
    for result in results:
        print(result)

