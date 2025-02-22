from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets
from .models import Song
from .serializers import SongSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scraper import scrape_playlist
from .spoti import SpotifyHandler

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

@api_view(['POST'])
def scrape_playlist_view(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required'}, status=400)
    
    try:
        # Explicitly call scrape_playlist function
        scraped_songs = scrape_playlist(url)
        
        if scraped_songs:
            return Response({
                'message': 'Scraping completed successfully',
                'songs': scraped_songs
            })
        else:
            return Response({
                'error': 'No songs were found or there was an error scraping'
            }, status=400)
            
    except Exception as e:
        return Response({
            'error': f'Error during scraping: {str(e)}'
        }, status=500)

@api_view(['POST'])
def scrape_songs(request):
    try:
        # The url parameter is kept for compatibility but not used
        songs = scrape_playlist(request.data.get('url', ''))
        return Response({'message': 'Scraping successful', 'songs': songs})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def scrape_view(request):
    try:
        # Call scrape_playlist with a dummy URL since we're using local file
        songs = scrape_playlist('dummy-url')
        return JsonResponse({'message': 'Scraping successful', 'songs': songs}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def search_spotify(request):
    handler = SpotifyHandler()
    result = handler.search_and_categorize()
    return Response(result)
