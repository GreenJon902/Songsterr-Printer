# pip install ddgs googlesearch-python selenium
#
# Requires you to have a spotify developer account (this is free and anyone can do it).

import ddgs
import tempfile
import threading
import requests
import json
import base64
import os
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from googlesearch import search
from selenium.webdriver.support.wait import WebDriverWait


def underlined(string: str) -> str:
    """
    Underlines any text surrounded by __ in the given string.
    """

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

def get_search_results(search_query: str) -> list[str]:
    """
    Returns the first 10 results for the given search_query.
    This returns them in the order given by the search engine.
    """

    try:
        return [result["href"] for result in ddgs.DDGS().text(search_query, max_results=10)]  # Use duck duck go as google is currently broken
    except ddgs.exceptions.DDGSException:
        return []

def find_songsterr_links(tracks: list[tuple[str, list[str]]], instrument: str) -> list[tuple[str, str, str]]:
    """
    tracks: list[tuple[track-name, list[artist-name]]]
    instrument: the name of the instrument we are searching for.
    return: list[tuple[artist-name, track-name, songsterr-link]]
    
    Finds songsterr links for the given tracks. This checks each one with the user to ensure it is correct.
    
    This returns tracks in the order that they were given. Skipped items are None in the return list.
    """
    found = list()
    for track, artists in tracks:
        for artist in artists:
            
            # Get top results from google
            search_query = "site:songsterr.com " + artist + " " + track + " " + instrument + " tab"
            response = get_search_results(search_query)
            if len(response) == 0:
                print("No results for \"" + search_query + "\"")
            
            # Let the user select the correct result
            for result in response:
                action = input(underlined("Found (for " + search_query + "): " + result + ". [__A__ccept/__N__ext/__M__ove on]? ")).upper()
                if action == "A":
                    break
                elif action == "N":
                    continue
                elif action == "M":
                    action = None
                    break
                else:
                    error
            if action is not None:  # If not None then result is the songsterr link
                found.append((artist, track, result))
            else:
                found.append(None)
    return found


def request(type, url, headers=None, data=None):
    """
    type: POST or GET.
    """
    if type == "POST":
        r = requests.post(url, headers=headers, data=data)
    elif type == "GET":
        r = requests.get(url, headers=headers, data=data)
    return json.loads(r.text)

def find_songs_in_album() -> list[tuple[str, list[str]]]:
    """
    Allows the user to enter some information to find an album, and then gets the names of all the songs in that album.
    return: list[tuple[track-name, list[artist-name]]]
    """
    
    # Get spotify token
    token = input("Spotify token (or none to generate one): ")

    if token == "":
        r = request("POST", "https://accounts.spotify.com/api/token", headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }, data={
            "grant_type": "client_credentials",
            "client_id": input("ID: "),
            "client_secret": input("Secret: ")
        })
        token = r["access_token"]
    
    # Get album data
    r = request("GET", f"https://api.spotify.com/v1/albums/{input('Album ID: ')}", headers={
        "Authorization": f"Bearer {token}"
    })
    return [(track["name"], [artist["name"] for artist in track["artists"]]) for track in r["tracks"]["items"]], r["name"]


lock = threading.Lock()
def download_songsterr(args):
    """
    Runs the https://raw.githubusercontent.com/GreenJon902/Songsterr-Printer/refs/heads/main/single.js and saves to the given path
    args: (url, path)
    """
    url, path = args
    print(f"Downloading {url}...")

    chrome_options = Options()
    #``chrome_options.binary_location = "./chrome-linux64/chrome"
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')  # sometimes helps too
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0")
    chrome_options.add_argument("--window-size=1100,1080")

    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")


    driver = webdriver.Chrome(
        #service=Service("./chromedriver-linux64/chromedriver", log_path="./chromedriver.log"),
        options=chrome_options,
    )
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "tablature"))
    )

    script = open("single.js", "r").read()
    print(1)
    driver.execute_script(script)
    print(2)
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
    with open(path, "wb") as f:
        f.write(pdf_data)

    print("PDF saved as " + path)

def download_multiple_songsterr(tracks: list[tuple[str, str]]):
    """
    Downloads all of the given tracks.
    tracks: list[tuple[songsterr-url, save-path]]
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_songsterr, tracks)
        for result in results:
            print(result)

if __name__ == "__main__":
    download_multiple_songsterr([("https://www.songsterr.com/a/wsa/plot-in-you-divide-drum-tab-s583489", "out.pdf")])
    
else:
    songs, album_name = find_songs_in_album()
    instrument = input("Instrument: ")
    links = filter(lambda x: x[1] is not None, enumerate(find_songsterr_links(songs, instrument)))
    download_multiple_songsterr([(link[2], f"./out/{n:02}-{link[0]}-{album_name}-{link[1]}-{instrument}.pdf") for n, link in links])
    

