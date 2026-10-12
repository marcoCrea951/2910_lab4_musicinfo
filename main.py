import time
import requests


BASE_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "Lab3/1.0.0 (cream1@etsu.edu)"
}

def search_artist_by_name(artist_name):
    endpoint = "/artist/"
    full_url = BASE_URL + endpoint
    
    params = {
        "query": f"artist:{artist_name}",  # Fixed variable name here
        "fmt": "json"
    }

    try:
        response = requests.get(full_url, headers=HEADERS, params=params)
        time.sleep(1)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Server responded with status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_artist_album(artist_mbid):
    endpoint = "/release-group"
    full_url = BASE_URL + endpoint

    params = {
        "artist": artist_mbid,
        "type": "album",
        "fmt": "json"
    }

    try:
        response = requests.get(full_url, headers=HEADERS, params=params)
        time.sleep(1)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Server responded with status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_track_list(release_group_mbid):
    endpoint = "/release"
    full_url = BASE_URL + endpoint

    params = {
        "release-group": release_group_mbid,
        "inc": "recordings",
        "fmt": "json"
    }

    try:
        response = requests.get(full_url, headers=HEADERS, params=params)
        time.sleep(1)

        if response.status_code == 200:
            data = response.json()
            releases = data.get("releases", [])
            if releases:
                media = releases[0].get("media", [])
                if media:
                    return media[0].get("tracks", [])
            return []
        else:
            return f"Error: Server responded with status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    while True:
        print("\n--- MusicBrainz Discography Explorer ---")
        user_input = input("Enter an artist name to search ('q' to quit) (e.g., Queen, Nirvana): ").strip()

        if user_input.lower() == 'q':
            print("Exiting...")
            break

        data = search_artist_by_name(user_input)
        
        print("\n--- API Response Result ---")
        if isinstance(data, dict):
            artists = data.get("artists", [])
            
            if not artists:
                print("No matching artists found.")
            else:
                print(f"Top results for '{user_input}':\n")
                top_artists = artists[:5]
                
                for idx, artist in enumerate(top_artists, start=1):
                    name = artist.get("name", "Unknown")
                    country = artist.get("country", "N/A")
                    disambiguation = artist.get("disambiguation", "")
                    mbid = artist.get("id")
                    
                    extra_info = f" ({disambiguation})" if disambiguation else ""
                    print(f"{idx}. {name}{extra_info} | Country: {country}")
                    print(f"   MBID: {mbid}\n")

                artist_choice = input("Select # 1-5: ").strip()

                if artist_choice.isdigit() and 1 <= int(artist_choice) <= len(top_artists):
                    selected_artist = top_artists[int(artist_choice) - 1]
                    artist_mbid = selected_artist.get("id")

                    print(f"\nFetching albums for {selected_artist.get('name')}...")
                    album_data = get_artist_album(artist_mbid)
                    # added a feature if artists have more than a few albums
                    # press 'm' for more
                    # acts as if youre clicking "see more"
                    if isinstance(album_data, dict):
                        albums = album_data.get("release-groups", [])
                        if not albums:
                            print("No albums found for this artist.")
                        else:
                            print(f"\nAlbums by {selected_artist.get('name')} ({len(albums)} total found):\n")
                            
                            page_size = 7
                            current_index = 0
                            album_choice = None

                            while current_index < len(albums):
                                batch_albums = albums[current_index : current_index + page_size]
                            
                                
                                print(f"--- Albums ({current_index + 1} to {current_index + len(batch_albums)}) ---")
                                for idx, album in enumerate(batch_albums, start=1):
                                    title = album.get("title", "Unknown Title")
                                    date = album.get("first-release-date", "Unknown Date")
                                    print(f"{idx}. {title} ({date})")

                                if current_index + page_size < len(albums):
                                    action = input("\nType 'm' to show more results: ")
                                    if action == 'm':
                                        current_index += page_size
                                        print()
                                        continue
                                    else:
                                        album_choice = action
                                        break
                                else:
                                    album_choice = input("\nSelect an album number to see the tracklist: ")
                                    break
                            
                            if album_choice.isdigit() and 1 <= int(album_choice) <= len(batch_albums):
                                selected_album = batch_albums[int(album_choice) - 1]
                                album_mbid = selected_album.get('id')

                                print(f"\nFetching tracks for '{selected_album.get('title')}'...")
                                tracks = get_track_list(album_mbid)

                                if isinstance(tracks, list) and tracks:
                                    print(f"\n--- Tracklist ---")
                                    for track in tracks:
                                        title = track.get("title", "Unknown Title")
                                        number = track.get("number", "?")
                                        
                                        length_ms = track.get("length")
                                        if length_ms:
                                            length_sec = length_ms // 1000
                                            minutes = length_sec // 60
                                            seconds = length_sec % 60
                                            time_str = f"({minutes}:{seconds:02d})"
                                        else:
                                            time_str = "(Unknown length)"
                                            
                                        print(f"{number}. {title} {time_str}")
                                else:
                                    print("No tracks found or error retrieving tracklist.")
                            else:
                                print("Invalid album selection.")
                    else:
                        print("Invalid artist selection.")
                else:
                    print("Invalid artist selection choice.")
        else:
            print(data)

        cont = input("\nWould you like to search for another artist? (y/n): ").strip().lower()
        if cont != 'y':
            print("Exiting...")
            break
        print("\n" + "="*40 + "\n")