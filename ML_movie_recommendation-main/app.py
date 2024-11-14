import pickle
import streamlit as st
import pandas as pd
import gdown
import os

# Function to download the similarity file from Google Drive
def download_similarity_file():
    url = 'https://drive.google.com/file/d/1gzYVPG0WorxjKUk-27T9nWYrzeF9d6R0/view?usp=drive_link'  # Replace with your file ID
    output = 'model/similarity.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Function to recommend movies
def recommend(movie, movies, similarity):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = [movies.iloc[i[0]].title for i in distances[1:6]]

    return recommended_movie_names

# Streamlit app header
st.header('Movie Recommender System')

# Load movie list
try:
    movies_dict = pickle.load(open('model/movie_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except FileNotFoundError:
    st.error("Movie list file not found.")
    st.stop()

# Download and load similarity data
download_similarity_file()
try:
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Similarity file not found.")
    st.stop()

# Extract movie titles from the movies DataFrame
movie_list = movies['title'].values

# Select movie from dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie, movies, similarity)
    if recommended_movie_names:
        st.write("Recommended Movies:")
        for name in recommended_movie_names:
            st.text(name)
