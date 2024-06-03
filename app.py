import pickle
import streamlit as st
import requests

# Define the function to fetch movie posters from TMDB
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=67db5741473e5319402f633043f6e384&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/original" + path
    return full_path

# Define the recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_titles = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movie_titles.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_titles, recommended_movie_posters

# Load the pickled data
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))

# Streamlit application
st.header("Movies Recommendation System Using Machine Learning")

movie_list = movies['title'].values

selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)

if st.button('Recommend'):
    recommended_titles, recommended_posters = recommend(selected_movie)
    st.write('Movies similar to "'+selected_movie+'".' )
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(recommended_posters[0])
        st.write(recommended_titles[0])
    with col2:
        st.image(recommended_posters[1])
        st.write(recommended_titles[1])
    with col3:
        st.image(recommended_posters[2])
        st.write(recommended_titles[2])
    with col4:
        st.image(recommended_posters[3])
        st.write(recommended_titles[3])
    with col5:
        st.image(recommended_posters[4])
        st.write(recommended_titles[4])
         
 