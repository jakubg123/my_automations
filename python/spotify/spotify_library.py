from time import sleep
from pytube import YouTube
from spotify_functions import *
from spotify_settings import EMAIL, PASSWORD, SPOTIFY_ID 
from spotify_google import *
if __name__ == '__main__':

    google_drive_directory='1WtZQs_w7Xqdup4_fWqvKWUb6CFI-zTsS' # only my credentials user has access to this directory so it's not the end of the world to leave it like that.
    format='video/mp4'

    spotify_titles ,playlist = get_spotify_links(SPOTIFY_ID) # my spotify channel id
    youtube_links = [] 

    for song, authors in spotify_titles.items():
        print(f"{song} {authors}")
        query = f"{song} {' '.join(authors)}"
        youtube_links.append(search_google(query))

    for url in youtube_links:
        download_youtube_audio(url,playlist)
        upload_file(f'{playlist}', format ,google_drive_directory)



