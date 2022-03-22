import streamlit as st
import pickle
import pandas as pd
import requests
import ast

def fetch_poster(id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=99d21cf0dec75e8da0ee5188a0fdc538'.format(id))
    data=response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        id=movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from Api
        recommended_movies_posters.append(fetch_poster(id))
    return recommended_movies , recommended_movies_posters
def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L
    movies['crew'] = movies['crew'].apply(fetch_director)
    index = movies[movies['director'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_director_name= []
    recommended_director_poster = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_director_poster.append(fetch_poster(movie_id))
        recommended_director_name.append(movies.iloc[i[0]].title)

    return recommended_director_name,recommended_director_poster

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender system')

selected_movie_name = st.selectbox(
         'How would you like to be contacted?',
         movies['title'].values)

if st.button('Recommend'):
    names, posters= recommend(selected_movie_name)
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

if st.button('Show Recommendation'):
    selected_movie_name = st.selectbox(
        'How would you like to be contacted?',
        movies['director'].values)
    recommended_director_name,recommended_director_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_director_name[0])
        st.image(recommended_director_posters[0])
    with col2:
        st.text(recommended_director_name[0])
        st.image(recommended_director_posters[0])
    with col3:
        st.text(recommended_director_name[0])
        st.image(recommended_director_posters[0])

    with col4:
        st.text(recommended_director_name[0])
        st.image(recommended_director_posters[0])

    with col5:
        st.text(recommended_director_name[0])
        st.image(recommended_director_posters[0])

