# Movie_recommendation_System
This project is a Movie Recommendation System that uses Content-Based Filtering to suggest movies to users. The system leverages TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to analyze and process the movie descriptions or metadata (e.g., genres, tags, or overviews). The aim is to recommend movies that are similar to a user's preference or selected movie.
![pic1](https://github.com/user-attachments/assets/5f123039-5b56-4e45-af9e-3c025d08af31)

![pic2](https://github.com/user-attachments/assets/310180dc-e665-4c10-824f-9814d08af2a0)
![pic3](https://github.com/user-attachments/assets/d16bbb07-2031-47cf-bda0-a16ac87aea58)


Key Features:
Content-Based Filtering:
The system focuses on the content of the movies, such as genres, keywords, or summaries, to compute similarities between movies. It does not rely on user ratings or collaborative data, making it independent of user interactions.

TF-IDF Vectorization:

TF-IDF is used to convert textual metadata into numerical vectors.
It helps identify the most significant words and reduce the impact of frequently occurring but less meaningful terms.
This approach ensures that the system captures the uniqueness of each movie.
Machine Learning Model:

The system uses a similarity measure (like cosine similarity) to find and rank movies based on their closeness in the TF-IDF feature space.
This enables the model to recommend movies most relevant to the user's preferences.
Deployed with Streamlit:

The application has been built and deployed using Streamlit, a Python-based framework for creating interactive web apps.
Streamlit's user-friendly interface allows users to search for a movie and instantly receive recommendations.
The interface is dynamic and responsive, providing an engaging user experience.

TMDb API Integration
The TMDb API provides access to a vast database of movies, TV shows, actors, and associated metadata. By integrating this API, the system can fetch relevant information about movies dynamically and enhance the user experience.
