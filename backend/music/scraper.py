import requests
from bs4 import BeautifulSoup
from .models import Song

def scrape_playlist(url):
    """
    Scrapes a playlist from a local HTML file and saves songs to the database.
    URL parameter kept for compatibility but currently not used.
    Returns a list of scraped songs.
    """
    try:
        # # Send GET request to the URL
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        # }
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()

        # # Save raw HTML content to files
        # with open('achetemele.txt', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        
        # with open('achetemele.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)

        # Read from local HTML file instead
        with open('C:/Users/ignac/Escritorio/Trabajos/spotilistas/backend/music/templates/pizarra2.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        with open('achetemele.txt', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open('achetemele.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Update selectors to match the SoundCloud HTML structure
        song_elements = soup.select('.playableTile__description')
        songs_data = []

        for song_el in song_elements:
            # Extract title, artist, and link from each song element
            title_el = song_el.select_one('.playableTile__mainHeading')
            artist_el = song_el.select_one('.playableTile__usernameHeading')
            
            if title_el and artist_el:
                song_data = {
                    'title': title_el.text.strip(),
                    'link': title_el['href'] if title_el.has_attr('href') else '',
                    'artist': artist_el.text.strip()
                }
                
                # Create or update song in database
                song, created = Song.objects.get_or_create(
                    title=song_data['title'],
                    artist=song_data['artist'],
                    defaults={'link': song_data['link']}
                )
                songs_data.append(song_data)

        return songs_data

    except Exception as e:
        print(f"Error scraping playlist: {str(e)}")
        return [] 