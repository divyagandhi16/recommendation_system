import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Book Recommender System')

books_ratings_dict = pickle.load(open('books_ratings_dict_f.pkl','rb'))
books_ratings = pd.DataFrame(books_ratings_dict)
similarity_scores = pickle.load(open('books_similarity_scores.pkl','rb'))
pt = pickle.load(open('books_ratings_pivot.pkl','rb'))

def recommend(book):
    books_list = list(pt.index)
    ind = books_list.index(book)
    similarity_scores_list = list(similarity_scores[ind])
    d = {}
    l = []
    book_name = []
    book_image = []
    for i in similarity_scores_list:
        d[i] = similarity_scores_list.index(i)
    d = dict(sorted(d.items(), reverse=True))
    for i in d.values():
        l.append(i)
    l = l[1:6]
    for i in l:
        book_name.append(pt.index[i])
        book_image.append(books_ratings[books_ratings['Book-Title'] == pt.index[i]]['Image-URL-M'].unique()[0])
    return book_name, book_image

selected_book = st.selectbox('Choose one book', books_ratings['Book-Title'].unique())
btn = st.button('Recommend')
if btn:
    names, posters = recommend(selected_book)
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