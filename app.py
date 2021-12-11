import streamlit as st
import pickle
import pandas as pd
import requests

api_key = 'de3b2483c3be60a1c800f9d93277ca88'

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US")
    data = response.json()
    poster = data["poster_path"]
    return f'http://image.tmdb.org/t/p/w500{poster}'

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    movie_posters=[]
    for movie in movies_list:
        movie_id=movies.iloc[movie[0]]['id']
        movie_posters.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[movie[0]].title)
    return recommend_movies, movie_posters



st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Movie you want to select for recommendations',
    (movies['title'].values))

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)[0]
    posters=recommend(selected_movie_name)[1]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
