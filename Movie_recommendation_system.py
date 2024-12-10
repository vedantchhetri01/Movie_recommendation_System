import streamlit as st
import pandas as pd
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    # GitHub raw file URLs
    url1 = "https://raw.githubusercontent.com/vedantchhetri01/Movie_recommendation_System/main/Movies-DataSet.csv"
    url2 = "https://raw.githubusercontent.com/vedantchhetri01/Movie_recommendation_System/main/dataset.csv"

    try:
        # Load CSV files from GitHub
        first_csv = pd.read_csv(url1)
        second_csv = pd.read_csv(url2)

        # Process the datasets
        second_csv['genre'] = second_csv['genre'].str.replace(',', ' ', regex=False)
        second_csv['tags'] = second_csv['genre'] + ' ' + second_csv['overview']

        first_csv = first_csv[['title', 'tags']]
        second_csv = second_csv[['title', 'tags']]

        # Combine and clean datasets
        final_dataset = pd.concat([first_csv[['title', 'tags']], second_csv[['title', 'tags']]], ignore_index=True)
        duplicate_removes = final_dataset.drop_duplicates(subset='title', keep='first')

        return duplicate_removes
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_cosine_similarity(final_movie_recommendation_ds):
    final_movie_recommendation_ds['tags'] = final_movie_recommendation_ds['tags'].fillna('')
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(final_movie_recommendation_ds['tags'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def recommend_movie_by_title(movie_title, cosine_sim, final_movie_recommendation_ds, num_recommendations=10):
    if movie_title not in final_movie_recommendation_ds['title'].values:
        st.write(f"Movie with title '{movie_title}' not found in the dataset.")
        return []
    movie_idx = final_movie_recommendation_ds[final_movie_recommendation_ds['title'] == movie_title].index[0]
    similarities = cosine_sim[movie_idx]

    recommended_indices = similarities.argsort()[-num_recommendations-1:-1][::-1]
    recommended_movies = []
    for idx in recommended_indices:
        recommended_movies.append(final_movie_recommendation_ds['title'].iloc[idx])
    return recommended_movies

def fetch_movie_details(movie_name):
    API_KEY = '3e45d4908b6845c86fd9de70e43df2f2'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}&language=en-US&page=1&include_adult=false"
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data['results']:
                movie = data['results'][0]
                poster_path = movie.get('poster_path', '')
                movie_id = movie.get('id', '')
                title = movie.get('title', '')
                rating = movie.get('vote_average', 'N/A')
                release_year = movie.get('release_date', '').split('-')[0]

                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    return poster_url, movie_id, title, rating, release_year
            return None, None, None, None, None
        except requests.exceptions.RequestException as e:
            st.warning(f"Attempt {attempt + 1}: Error fetching movie details - {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                st.error("Failed to fetch movie details after multiple attempts.")
                return None, None, None, None, None

def run_streamlit_app():
    st.set_page_config(page_title="Movie Recommendation System", layout="wide")
    st.markdown("""
    <style>
    .main {background-color: #f0f8ff;}
    h1 {color: #1e90ff;}
    h2 {color: #ff6347;}
    .emoji {font-size: 2rem;}
    </style>
    """, unsafe_allow_html=True)
    st.title("🎬 Movie Recommendation System")

    final_movie_recommendation_ds = load_data()
    if final_movie_recommendation_ds is None:
        return

    cosine_sim = create_cosine_similarity(final_movie_recommendation_ds)
    movie_name = st.selectbox("Select a movie to get recommendations:", final_movie_recommendation_ds['title'].values)

    if st.button("🎯 Recommend Movies"):
        st.write(f"🔍 Recommendations based on: '{movie_name}'")
        recommended_movies = recommend_movie_by_title(movie_name, cosine_sim, final_movie_recommendation_ds)

        if recommended_movies:
            for movie in recommended_movies:
                st.write(movie)

if __name__ == "__main__":
    run_streamlit_app()
