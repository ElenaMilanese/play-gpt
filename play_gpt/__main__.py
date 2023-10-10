from play_gpt.gpt import GPTPlaylist
from play_gpt.spotify import SpotifyPlaylistCreator


gpt_playlist = GPTPlaylist()

sp_playlist_creator = SpotifyPlaylistCreator()


if __name__ == "__main__":
    
    input_guidelines = "las canciones más conocidas de películas de studio ghibli"
    
    playlist = gpt_playlist.generate_playlist(input_guideline=input_guidelines)
    name = gpt_playlist.generate_playlist_name(input_guideline=input_guidelines)
    
    spotify_songs = sp_playlist_creator.search_songs(playlist)
    
    playlist_id = sp_playlist_creator.create_playlist(spotify_songs, name)


