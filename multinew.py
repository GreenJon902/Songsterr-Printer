# pip install ddgs

import ddgs


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

    return [result["href"] for result in ddgs.DDGS().text(search_query, max_results=10)]  # Use duck duck go as google is currently broken

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
            search_query = "songsterr " + artist + " " + track + " " + instrument
            response = get_search_results(search_query)
            assert len(response) > 0, "No results for \"" + search_query + "\""
            
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

if __name__ == "__main__":
    print(find_songsterr_links([("funeral derangements", ["ice nine kills"])], "drum score"))

