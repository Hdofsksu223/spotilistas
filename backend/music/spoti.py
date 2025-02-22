import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Song, SpotiEx, SpotiNoex
from requests.exceptions import ReadTimeout, ConnectionError
import time
from django.db.models import Q
from datetime import datetime

class SpotifyHandler:
    def __init__(self):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(),
            requests_timeout=20
        )
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"progress_{self.timestamp}.txt"

    def log_message(self, message):
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    def search_and_categorize(self):
        songs = Song.objects.exclude(
            id__in=SpotiEx.objects.values_list('id', flat=True)
        ).exclude(
            id__in=SpotiNoex.objects.values_list('id', flat=True)
        )

        processed_count = 0
        errors_count = 0

        self.log_message(f"Search started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for song in songs:
            try:
                query = f"{song.title} {song.artist}"
                self.log_message(f"Processing: {query}")
                results = self.spotify.search(q=query, type='track', limit=1)

                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    spotify_artist = track['artists'][0]['name'].lower()
                    original_artist = song.artist.lower()

                    self.log_message(f"Spotify result - Title: {track['name']}, Artist: {track['artists'][0]['name']}")

                    if spotify_artist == original_artist:
                        duplicate_exists = SpotiEx.objects.filter(
                            Q(title=track['name']) & 
                            Q(artist=track['artists'][0]['name'])
                        ).exists()

                        if not duplicate_exists:
                            SpotiEx.objects.create(
                                title=track['name'],
                                artist=track['artists'][0]['name'],
                                link=track['external_urls']['spotify']
                            )
                            self.log_message(f"Added to SpotiEx: {track['name']} by {track['artists'][0]['name']}")
                        else:
                            self.log_message(f"Skipped (duplicate in SpotiEx): {track['name']} by {track['artists'][0]['name']}")
                    else:
                        self.log_message(f"Artist mismatch - Spotify: {spotify_artist}, Original: {original_artist}")
                        duplicate_exists = SpotiNoex.objects.filter(
                            Q(title=song.title) & 
                            Q(artist=song.artist)
                        ).exists()

                        if not duplicate_exists:
                            SpotiNoex.objects.create(
                                title=song.title,
                                artist=song.artist,
                                link=song.link
                            )
                            self.log_message(f"Added to SpotiNoex (artist mismatch): {song.title} by {song.artist}")
                        else:
                            self.log_message(f"Skipped (duplicate in SpotiNoex): {song.title} by {song.artist}")
                else:
                    duplicate_exists = SpotiNoex.objects.filter(
                        Q(title=song.title) & 
                        Q(artist=song.artist)
                    ).exists()

                    if not duplicate_exists:
                        SpotiNoex.objects.create(
                            title=song.title,
                            artist=song.artist,
                            link=song.link
                        )
                        self.log_message(f"Added to SpotiNoex (no results): {song.title} by {song.artist}")
                    else:
                        self.log_message(f"Skipped (duplicate in SpotiNoex): {song.title} by {song.artist}")
                processed_count += 1
                
                self.log_message(f"Progress: {processed_count}/{len(songs)} songs processed. Errors: {errors_count}\n")
                
                time.sleep(0.5)

            except (ReadTimeout, ConnectionError) as e:
                errors_count += 1
                self.log_message(f"Error processing song {song.title}: {str(e)}")
                if not SpotiNoex.objects.filter(
                    Q(title=song.title) & 
                    Q(artist=song.artist)
                ).exists():
                    SpotiNoex.objects.create(
                        title=song.title,
                        artist=song.artist,
                        link=song.link
                    )
                    self.log_message(f"Added to SpotiNoex (after error): {song.title} by {song.artist}")
                continue

        final_message = f'Processed {processed_count} songs successfully. Errors: {errors_count}'
        self.log_message(f"\nFinal result: {final_message}")
        self.log_message(f"Search completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return {
            'success': True,
            'message': final_message
        }
