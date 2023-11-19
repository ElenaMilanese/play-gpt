from play_gpt.gpt import GPTPlaylist
from play_gpt.spotify import SpotifyPlaylistCreator


if __name__ == "__main__":
    
    gpt_playlist = GPTPlaylist()

    sp_playlist_creator = SpotifyPlaylistCreator()
    
    input_guidelines = input("¿Cómo querés que sea la playlist?\n")
    
    playlist = gpt_playlist.generate_playlist(input_guideline=input_guidelines)
    name = gpt_playlist.generate_playlist_name(input_guideline=input_guidelines)
    
    spotify_songs = sp_playlist_creator.find_songs(playlist)
    
    playlist_id = sp_playlist_creator.create_playlist(spotify_songs, name)


