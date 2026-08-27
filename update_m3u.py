import requests
import re

def extract_m3u8_url(embed_url):
    """Apre la pagina embed dell'evento e cerca il vero flusso .m3u8 con i token"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://streamfree.top/"
    }
    try:
        response = requests.get(embed_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Cerca nel codice sorgente un indirizzo che finisce con .m3u8 e contiene i token
            match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Impossibile estrarre m3u8 da {embed_url}: {e}")
    
    # Se fallisce l'estrazione, restituisce l'embed_url come fallback
    return embed_url

def update_playlist():
    api_url = "https://streamfree.top/api/v1/streams"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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
        
        # Estrae il flusso diretto .m3u8 con i token
        direct_stream_url = extract_m3u8_url(embed_url) if embed_url else ""
        
        # Formattazione M3U con il Referer richiesto dai server di streaming
        m3u_lines.append(f'#EXTINF:-1 tvg-logo="{thumb_url}" group-title="{category}", {display_name}')
        m3u_lines.append('#EXTVLCOPT:http-referrer=https://streamfree.top/')
        m3u_lines.append(f'{direct_stream_url}\n')

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
        
    print(f"Playlist aggiornata correttamente. Canali inseriti: {len(streams)}")

if __name__ == "__main__":
    update_playlist()
