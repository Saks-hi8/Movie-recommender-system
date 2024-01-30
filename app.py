import os

import streamlit as st
import pickle
import requests
from PIL import Image
import base64

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2347dadb241970157f590a3ed018b966&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:23]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

movies = pickle.load(open('/Users/sakshichavan/PycharmProjects/Movie-reccomender-system/movie_list.pkl', 'rb'))
similarity = pickle.load(open('/Users/sakshichavan/PycharmProjects/Movie-reccomender-system/similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Top recommendations for your Movie Picks!',
    movies['title'].values
)

# Load your background image
background_image = Image.open('/Users/sakshichavan/Downloads/netflixteaser.png')

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64('/Users/sakshichavan/Downloads/netflix2.png')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-position: center;
background-size: cover;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_columns = 4
    num_rows = len(names) // num_columns + (1 if len(names) % num_columns > 0 else 0)

    for row in range(num_rows):
        cols = st.columns(num_columns)
        for col in range(num_columns):
            index = row * num_columns + col
            if index < len(names):
                with cols[col]:
                    st.text(names[index])
                    st.image(posters[index])
