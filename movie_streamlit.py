import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')


st.header('Content based Recommendation')

movies_dict = pickle.load(open('_divya.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity_scores = pickle.load(open('similarity_scores_divya.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7adc9ce829fe7efaa84a446ad79ad152&language=en.US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def content_based_recommend(movie):
    movies_list = list(movies['title'])
    ind = movies_list.index(movie)
    similarity_scores_list = list(similarity_scores[ind])
    d = {}
    l = []
    recommended_movies = []
    recommended_movies_posters = []
    for i in similarity_scores_list:
        d[i] = similarity_scores_list.index(i)
    d = dict(sorted(d.items(), reverse=True))
    for i in d.values():
        l.append(i)
    l = l[1:6]
    for i in l:
        recommended_movies.append(movies['title'].iloc[i])
        recommended_movies_posters.append(fetch_poster(movies['movie_id'].iloc[i]))
    return recommended_movies, recommended_movies_posters

selected_movie = st.selectbox('Choose one movie', movies['title'].values)
btn = st.button('Recommend')
if btn:
    names, posters = content_based_recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


st.header('Popularity Based Recommendation')

popular_movies_dict = pickle.load(open('popular_movies_dict_divya.pkl','rb'))
popular_movies = pd.DataFrame(popular_movies_dict)
l = []
for i in range(popular_movies.shape[0]):
    for j in popular_movies['genres'].iloc[i]:
        l.append(j)
s = set(l)
l = list(s)
list_of_genres = sorted(l)

genre1 = st.selectbox('Choose first genre', list_of_genres)
genre2 = st.selectbox('Choose second genre', list_of_genres)
bttn = st.button('Recommend based on popularity')

def popularity_based_recommend(genre1, genre2):
    l = []
    recommended_movies = []
    recommended_movies_posters = []
    for i in range(popular_movies.shape[0]):
        if (genre1 in popular_movies['genres'].iloc[i]) and (genre2 in popular_movies['genres'].iloc[i]):
            l.append(i)
    df = popular_movies.iloc[l]
    df = df.sort_values('popularity', ascending=False)
    df = df.reset_index()
    for i in range(5):
        recommended_movies.append(df['title'].iloc[i])
        recommended_movies_posters.append(fetch_poster(popular_movies['movie_id'].iloc[i]))
    return recommended_movies, recommended_movies_posters

if bttn:
    names, posters = popularity_based_recommend(genre1, genre2)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])