import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv() 

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI= 'http://localhost:8501'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )
)

st.set_page_config(page_title='ON REPEAT!', page_icon='🎵')
st.title('ON REPEAT!')
st.write('Lagi dengerin apaansih?!')
st.image('.\GOL4doEa4AAGndP.jpeg', use_column_width=True)

top_tracks = sp.current_user_top_tracks(limit=15, time_range='medium_term')
track_ids= [track['id'] for track in top_tracks['items']]
audio_features = sp.audio_features(track_ids)

df = pd.DataFrame(audio_features)
df['track_name'] = [track['name'] for track in top_tracks['items']]
df = df[['track_name','danceability', 'energy', 'valence', 'mode']]
df.set_index('track_name', inplace=True)

st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height=500)