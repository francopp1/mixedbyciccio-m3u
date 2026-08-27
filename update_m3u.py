import requests

def update_playlist():
    url = "https://streamfree.top/api/v1/streams"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        streams = data.get("streams", [])
    except Exception as e:
        print(f"Errore nel recupero delle API: {e}")
        streams = []

    lines = ["#EXTM3U\n"]
    for s in streams:
        name = s.get("name", "Evento Sportivo")
        category = s.get("category", "Generale").capitalize()
        league = s.get("league", "")
        embed_url = s.get("embed_url", "")
        thumb_url = s.get("thumbnail_url", "")
        
        display_name = f"{name} ({league})" if league else name
        lines.append(f'#EXTINF:-1 tvg-logo="{thumb_url}" group-title="{category}", {display_name}')
        lines.append(f'{embed_url}\n')

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Playlist aggiornata con successo! Eventi trovati: {len(streams)}")

if __name__ == "__main__":
    update_playlist()
