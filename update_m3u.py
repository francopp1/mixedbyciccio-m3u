import requests

def update_playlist():
    api_url = "https://streamfree.top/api/v1/streams"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        streams = data.get("streams", [])
    except Exception as e:
        print(f"Errore durante la chiamata API: {e}")
        streams = []

    m3u_lines = ["#EXTM3U\n"]
    
    for s in streams:
        name = s.get("name", "Evento Sportivo")
        category = s.get("category", "Generale").capitalize()
        league = s.get("league", "")
        embed_url = s.get("embed_url", "")
        thumb_url = s.get("thumbnail_url", "")
        
        display_name = f"{name} ({league})" if league else name
        
        # Formattazione standard M3U per liste dinamiche
        m3u_lines.append(f'#EXTINF:-1 tvg-logo="{thumb_url}" group-title="{category}", {display_name}')
        m3u_lines.append(f'{embed_url}\n')

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
        
    print(f"Playlist generata con successo. Eventi attivi inseriti: {len(streams)}")

if __name__ == "__main__":
    update_playlist()
