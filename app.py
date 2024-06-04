import pickle
import streamlit as st
import requests
import pandas as pd

# Define the function to fetch movie posters from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=67db5741473e5319402f633043f6e384&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path'] is not None:
        path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/original" + path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Image"
    release_year = data['release_date'].split('-')[0] if 'release_date' in data else 'N/A'
    release_year = release_year
    home_url = data['homepage'] if 'homepage' in data and data['homepage'] else '#'
    imdb_rating = data['vote_average'] if 'vote_average' in data else 'N/A'

    return full_path, release_year, home_url, imdb_rating

# Define the recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_titles = []
    recommended_movie_posters = []
    recommended_movie_release_date = []
    recommended_movie_homepage = []
    for i in distances[1:11]:  # Fetch 10 movies instead of 5
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movie_titles.append(movies.iloc[i[0]].title)
        movie_poster, release_date, homepage, imdb = fetch_poster(movie_id)

        recommended_movie_posters.append(movie_poster)
        recommended_movie_release_date.append(release_date)
        recommended_movie_homepage.append(homepage)
    return recommended_movie_titles, recommended_movie_posters, recommended_movie_release_date, recommended_movie_homepage

def search_movie(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[index]['movie_id']
    movie_title = movies.iloc[index].title
    movie_poster, release_date, homepage, imdb = fetch_poster(movie_id)
    return movie_title, movie_poster, release_date, homepage, imdb

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
    search_title, search_poster, release_date, search_home, search_imdb = search_movie(selected_movie)
    
    st.markdown(
            f'''
            <div style="display: flex;  align-items: left;  text-align:center;">
            <div style="margin-bottom:10px; background-color:rgb(38 39 48); padding:15px;">
                <a href="{search_home}" style="text-decoration:none; color:white;">
                    <img src="{search_poster}" width="300" style=" border-radius:8px" /><br>
                    <strong>{search_title} ({release_date})</strong><br>
                </a>
                </div>
                <div style="text-align: left; margin:20px">
                    IMDb Rating: {search_imdb}
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    recommended_titles, recommended_posters, recommended_movie_release_date, recommended_movie_homepage = recommend(selected_movie)
    st.markdown(
            f'''
            <div style="background-color:rgb(38 39 48); height:auto; padding: 10px; border-radius: 0px; margin-bottom:10px;">
                People also search for:
            </div>
            ''',
            unsafe_allow_html=True
        )
    # First row of recommendations
    cols = st.columns(5)
    for col, title, poster, date, home in zip(cols, recommended_titles[:5], recommended_posters[:5], recommended_movie_release_date[:5], recommended_movie_homepage[:5]):
        with col:

            st.markdown(
                f'''
                <div style="background-color:rgb(38 39 48); height:auto; padding: 10px; border-radius: 0px; text-align: center; margin-bottom:10px;">
                    <a href="{home}" target="_blank" style="text-decoration:none; color:white;">
                        <img src="{poster}" style="width: 100%;  border-radius: 8px;" />
                        <div><strong>{title} ({date})</strong></div>
                    </a>
                </div>
                ''',
                unsafe_allow_html=True
            )

    # Second row of recommendations
    cols2 = st.columns(5)
    for col, title, poster, date, home in zip(cols2, recommended_titles[5:], recommended_posters[5:],recommended_movie_release_date[:5], recommended_movie_homepage[:5]):
        with col:
           
            st.markdown(
                f'''
                <div style="background-color:rgb(38 39 48); height:auto; padding: 10px; border-radius: 0px; text-align: center; margin-bottom:10px;">
                    <a href="{home}" target="_blank" style="text-decoration:none; color:white;">
                        <img src="{poster}" style="width: 100%;  border-radius: 8px;" />
                        <div><strong>{title} ({date})</strong></div>
                    </a>
                </div>
                ''',
                unsafe_allow_html=True
            )

st.write('_______________________________')
