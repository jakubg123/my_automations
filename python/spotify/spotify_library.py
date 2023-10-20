from time import sleep
from pytube import YouTube
from spotify_functions import *
from spotify_settings import EMAIL, PASSWORD, DISCORD_ID


if __name__ == '__main__':

    spotify_titles ,playlist = get_spotify_links(DISCORD_ID) # my discord channel id
    youtube_links = [] 

    for song, authors in spotify_titles.items():
        print(f"{song} {authors}")
        query = f"{song} {' '.join(authors)}"
        youtube_links.append(search_google(query))

    for item in youtube_links:
        download_youtube_audio(item,playlist)





