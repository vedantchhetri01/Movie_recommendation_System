import streamlit as st
import pandas as pd
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def load_data():
        first_csv = pd.read_csv('E:\\PYTHON PROJECTS\\movie recommendation\\Movies-DataSet.csv')
        second_csv = pd.read_csv('E:\\PYTHON PROJECTS\\movie recommendation\\dataset.csv')
    second_csv['genre'] = second_csv['genre'].str.replace(',', ' ', regex=False)
        second_csv['tags'] = second_csv['genre'] + ' ' + second_csv['overview']
        first_csv = first_csv[['title', 'tags']]
        second_csv = second_csv[['title', 'tags']]
    final_dataset = pd.concat([first_csv[['title', 'tags']], second_csv[['title', 'tags']]], ignore_index=True)
    duplicate_removes = final_dataset.drop_duplicates(subset='title', keep='first')
    return duplicate_removes

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

def fetch_highly_rated_movies():
    API_KEY = '3e45d4908b6845c86fd9de70e43df2f2'
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"


    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        highly_rated_movies = []
        for movie in data['results']:
            title = movie['title']
            rating = movie['vote_average']
            poster_path = movie.get('poster_path', '')
            movie_id = movie['id']
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
            highly_rated_movies.append((title, poster_url, movie_id, rating))
        return highly_rated_movies
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching highly rated movies: {e}")
        return []
def fetch_top_movies_2024():

    
    API_KEY = '3e45d4908b6845c86fd9de70e43df2f2'
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&primary_release_year=2024&language=en-US&page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_movies_2024 = []
        for movie in data['results']:
            title = movie['title']
            rating = movie['vote_average']
            poster_path = movie.get('poster_path', '')
            movie_id = movie['id']
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
            top_movies_2024.append((title, poster_url, movie_id, rating))
        return top_movies_2024
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching top movies of 2024: {e}")
        return []


def surprise_me_option():
    surprise_option = st.selectbox("Surprise Me", ["Select an Option", "Highly Rated Movies", "Top Movies of 2024"])
    return surprise_option

def run_streamlit_app():
    st.set_page_config(page_title="Movie Recommendation System", layout="wide")
    st.markdown("""
    <style>
    .main {background-color: #f0f8ff;}
    h1 {color: #1e90ff;}
    h2 {color: #ff6347;}
    .emoji {font-size: 2rem;}
                .recommendation-box {border: 2px solid #1e90ff; border-radius: 10px; padding: 10px;}

                .movie-poster {
        display: inline-block;
        width: 100%;
        text-align: center;
}
.movie-poster img {
        width: 100%;
        height: auto;
        border-radius: 10px;
        transition: transform 0.3s ease; }

.movie-poster img:hover {
        transform: scale(1.05);  /* Slight zoom effect on hover */
    }

        .movie-info {
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjdjMzl4aGg0bW95Zmg1ZXN4Ymw5bWJidmxvazI1OGZlczR0enJiMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/KxscqRylVTBty6bUIS/giphy.gif" 
    st.markdown(f'''
    <div style="display: flex; align-items: center; justify-content: flex-start; width: 100%;">
        <h1 style="color: #1e90ff; font-weight: bold; margin-right: 10px;">🎬 Movie Recommendation System</h1>
        <img src="{gif_url}" alt="Movie GIF" style="width: 80px; height: 80px;">
    </div>
    ''', unsafe_allow_html=True)

    final_movie_recommendation_ds = load_data()
    cosine_sim = create_cosine_similarity(final_movie_recommendation_ds)
    movie_name = st.selectbox("Select a movie to get recommendations:", final_movie_recommendation_ds['title'].values)

    if st.button("🎯 Recommend Movies"):
        st.write(f"🔍 Recommendations based on: '{movie_name}'")
        recommended_movies = recommend_movie_by_title(movie_name, cosine_sim, final_movie_recommendation_ds)

        if recommended_movies:
            num_cols = 5
            cols = st.columns(num_cols)
            col_idx = 0
            for movie in recommended_movies:
                poster_url, movie_id, title, rating, release_year = fetch_movie_details(movie)

                if poster_url:
                    movie_url = f"https://www.themoviedb.org/movie/{movie_id}" if movie_id else ''
                    cols[col_idx].markdown(f"""
                    <div class="movie-poster">
                        <a href="{movie_url}" target="_blank">
                            <img src="{poster_url}" alt="{movie}">
                        </a>
                        <div class="movie-info">
                            <h3>{title} ({release_year})</h3>
                            <p><strong>Rating:</strong> {rating} / 10</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    cols[col_idx].write(f"Poster not available for {movie}")
                col_idx += 1
                if col_idx >= num_cols:
                    col_idx = 0
    surprise_option = surprise_me_option()
    if surprise_option == "Highly Rated Movies":
        st.write("🔍 Highly Rated Movies")
        highly_rated_movies = fetch_highly_rated_movies()


        
        if highly_rated_movies:
            num_cols = 5
            cols = st.columns(num_cols)
            col_idx = 0
            for movie, poster_url, movie_id, rating in highly_rated_movies:
                movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
                if poster_url: 
                    cols[col_idx].markdown(f"""
                    <div class="movie-poster">
                        <a href="{movie_url}" target="_blank">
                            <img src="{poster_url}" alt="{movie}">
                        </a>
                        <div class="movie-info">
                            <h3>{movie}</h3>
                            <p><strong>Rating:</strong> {rating} / 10</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
                if col_idx >= num_cols:
                    col_idx = 0

    elif surprise_option == "Top Movies of 2024":
        st.write("🔍 Top Movies of 2024")
        top_movies_2024 = fetch_top_movies_2024()

        if top_movies_2024:
            num_cols = 5
            cols = st.columns(num_cols)
            col_idx = 0
            for movie, poster_url, movie_id, rating in top_movies_2024:
                movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
                if poster_url:  
                    cols[col_idx].markdown(f"""
                    <div class="movie-poster">
                        <a href="{movie_url}" target="_blank">
                            <img src="{poster_url}" alt="{movie}">
                        </a>
                        <div class="movie-info">
                            <h3>{movie}</h3>
                            <p><strong>Rating:</strong> {rating} / 10</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
                if col_idx >= num_cols:
                    col_idx = 0

    st.markdown('''<hr style="border: 1px solid #1e90ff; margin-top: 40px;">''', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: space-around; margin-top: 40px;">
        <a href="https://www.netflix.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" alt="Netflix" style="width: 100px; height: auto; margin: 10px;">
        </a>
        <a href="https://www.disneyplus.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/1e/Disney%2B_Hotstar_logo.svg" alt="Disney+" style="width: 100px; height: auto; margin: 10px;">
        </a>
        <a href="https://www.max.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c0/HBO_Max_Logo_Old.svg" alt="HBO Max" style="width: 100px; height: auto; margin: 10px;">
        </a>
        <a href="https://www.primevideo.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Amazon_Prime_Video_logo.svg" alt="Prime Video" style="width: 100px; height: auto; margin: 10px;">
        </a>
    </div>

     <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px; gap: 20px;">
        <a href="https://www.facebook.com/sharer/sharer.php?u=https://github.com/your_github_repository" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 40px; height: 40px;">
        </a>
        <a href="https://api.whatsapp.com/send?text=Check%20out%20this%20amazing%20app:%20https://github.com/your_github_repository" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width: 40px; height: 40px;">
        </a>
        <a href="https://www.instagram.com/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width: 40px; height: 40px;">
        </a>
    </div>
          
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    run_streamlit_app()
