"""***************************************************************************************
*    Title: Mood based music recommendation in Python with Spotify API
*    Author: Burak Öztürk
*    Date: November 5, 2021
*    Availability: https://www.linkedin.com/pulse/mood-based-music-recommendation-python-spotify-api-burak-öztürk/
*    THE CODE FROM THE ABOVE SOURCE HAS BEEN MODIFIED
***************************************************************************************"""

import sys
import authorisation   # which one is created just now
import pandas as pd
import time
import numpy as np
from numpy.linalg import norm

user_feeling = input("How are you feeling? (happy, sad, angry, calm, anxious, restless): ")         # questions are here just for now
desired_mood = input("How would you like to feel? (happy, sad, angry, calm, anxious, restless): ")
# lets authorize and retrieve spotify object
spotify = authorisation.get_spotify_client(session)

genres = spotify.recommendation_genre_seeds()

data_dict = {
  "id":[], 
  "genre":[], 
  "track_name":[], 
  "artist_name":[],
  "valence":[],
  "energy":[],
  "user_feeling": [],  # added this to column
  "desired_mood": [],# <-- this too 
}
  
  
# Get recommendation for each genre
for genre in genres:
    recs = spotify.recommendations(genres=[genre], limit=10) 
    recs = eval(recs.model_dump_json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]

  
  for track in recs:
      data_dict["id"].append(track["id"])
      data_dict["genre"].append(genre)
      track_meta = spotify.track(track["id"])
      data_dict["track_name"].append(track_meta.name)
      data_dict["artist_name"].append(track_meta.album.artists[0].name)
      try:
        track_features = spotify.track_audio_features(track["id"])
      except tekore.TooManyRequests as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds.")
        time.sleep(e.retry_after)
        track_features = spotify.track_audio_features(track["id"])
        
      data_dict["valence"].append(track_features.valence)
      data_dict["energy"].append(track_features.energy)
      data_dict["user_feeling"].append(user_feeling) 
      data_dict["desired_mood"].append(desired_mood)
      time.sleep(1)

def get_mood_vector(feeling):
    mood_mapping = {
        "happy": [0.8, 0.9],
        "sad": [0.2, 0.1],
        "angry": [0.2, 0.8],
        "calm": [0.7, 0.3],
        "anxious": [0.4, 0.6],
        "restless": [0.5, 0.7],
    }
    return mood_mapping.get(feeling, [0.5, 0.5])  # Default to a neutral mood

def get_track_mood_vector(valence, energy, user_feeling_vec, desired_mood_vec):
    # Combine valence, energy, user_feeling_vec, desired_mood_vec
    track_vector = [
        valence * 0.5 + user_feeling_vec[0] * 0.2 + desired_mood_vec[0] * 0.3,
        energy * 0.5 + user_feeling_vec[1] * 0.2 + desired_mood_vec[1] * 0.3,
    ]
    return track_vector

def recommend(track_id, ref_df, spotify, n_recs=5):
    features = spotify.track_audio_features(track_id)
    vector = np.array(features["user_mood_vec"])

    ref_df["distances"] = ref_df["user_mood_vec"].apply(lambda x: norm(vector - np.array(x)))

    df_sorted = ref_df.sort_values(by="distances", ascending=True)

    df_sorted = df_sorted[df_sorted["id"] != track_id]

    return df_sorted.iloc[:n_recs]

# store data in pandas dataframe
df = pd.DataFrame(data_dict)

# drop duplicates
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
df.to_csv("arousal_dataset.csv", index = False)

# combine valence, energy, and mood vectors into a new column
df["mood_vec"] = df.apply(lambda row: get_track_mood_vector(row["valence"], row["energy"], get_mood_vector(row["user_feeling"]), get_mood_vector(row["desired_mood"])), axis=1)
