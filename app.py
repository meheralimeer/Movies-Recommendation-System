# frontend.py
import streamlit as st
from backend import (
    create_tables, get_all_movies, get_genres_for_movie,
    add_favorite, remove_favorite, get_favorites, 
    get_movie_recommendations, get_all_genres, get_all_movie_titles
)

# Initialize database tables
create_tables()

# Configure page
st.set_page_config(page_title="Movie Database", layout="wide")

# Cache expensive database queries
@st.cache_data(ttl=300)
def cached_movies():
    return get_all_movies()

@st.cache_data(ttl=300)
def cached_genres():
    return get_all_genres()

@st.cache_data(ttl=300)
def cached_titles():
    return get_all_movie_titles()

# Utility functions
def get_movie_id(title: str) -> int:
    """Helper to get movie ID from title"""
    movies = cached_movies()
    for movie in movies:
        if movie['title'] == title:
            return movie['movie_id']
    return -1

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
    ["Recommendations", "Browse Movies", "Favorites"])

# Recommendations Page (Default Tab)
if page == "Recommendations":
    st.title("Movie Recommendations")
    
    # Search input with suggestions
    movie_query = st.text_input("Search for a movie to get recommendations:")
    suggestions = [title for title in cached_titles() if movie_query.lower() in title.lower()]
    
    if suggestions:
        selected_movie = st.selectbox("Select a movie:", suggestions)

        if selected_movie:
            recommendations = get_movie_recommendations(selected_movie)
            if recommendations:
                st.subheader(f"Recommendations based on {selected_movie}:")
                favorites = [m['movie_id'] for m in get_favorites()]
                
                for i, title in enumerate(recommendations, 1):
                    col1, col2 = st.columns([4, 1])
                    movie_id = get_movie_id(title)
                    
                    with col1:
                        st.write(f"{i}. {title}")
                    
                    with col2:
                        if movie_id != -1:
                            if movie_id in favorites:
                                if st.button("❤️ Remove", key=f"rec_fav_{movie_id}"):
                                    remove_favorite(movie_id)
                                    st.rerun()
                            else:
                                if st.button("🤍 Add", key=f"rec_fav_{movie_id}"):
                                    add_favorite(movie_id)
                                    st.rerun()
            else:
                st.warning("No recommendations found for this movie.")

# Browse Movies Page
elif page == "Browse Movies":
    st.title("Movie Database Browser")
    
    # Search and filters
    col1, col2 = st.columns([3, 1])
    search_query = col1.text_input("Search movies by title:")
    selected_genres = col2.multiselect("Filter by genre:", options=cached_genres())
    
    # Pagination
    movies_per_page = 20
    page_number = st.number_input("Page number", min_value=1, value=1)
    offset = (page_number - 1) * movies_per_page

    # Filter movies
    filtered_movies = []
    for movie in cached_movies():
        if search_query.lower() in movie['title'].lower():
            if selected_genres:
                movie_genres = get_genres_for_movie(movie['movie_id'])
                if not any(genre in movie_genres for genre in selected_genres):
                    continue
            filtered_movies.append(movie)

    # Display results
    total_pages = (len(filtered_movies) // movies_per_page) + 1
    st.write(f"Showing {len(filtered_movies)} results (Page {page_number} of {total_pages})")
    
    for movie in filtered_movies[offset:offset+movies_per_page]:
        with st.expander(f"{movie['title']} ({movie['release_year']})"):
            col1, col2 = st.columns([3, 1])
            col1.write(movie['description'])
            genres = get_genres_for_movie(movie['movie_id'])
            col2.write(f"**Genres:** {', '.join(genres)}")
            
            # Favorite button
            favorites = [m['movie_id'] for m in get_favorites()]
            if movie['movie_id'] in favorites:
                if col2.button("❤️ Remove from Favorites", key=f"fav_{movie['movie_id']}"):
                    remove_favorite(movie['movie_id'])
                    st.rerun()
            else:
                if col2.button("🤍 Add to Favorites", key=f"fav_{movie['movie_id']}"):
                    add_favorite(movie['movie_id'])
                    st.rerun()

# Favorites Page
elif page == "Favorites":
    st.title("Your Favorite Movies")
    
    favorites = get_favorites()
    if not favorites:
        st.info("No favorites yet! Browse movies or get recommendations to add some.")
    else:
        movies_per_page = 20
        page_number = st.number_input("Page number", min_value=1, value=1, key="fav_page")
        offset = (page_number - 1) * movies_per_page
        
        for movie in favorites[offset:offset+movies_per_page]:
            with st.expander(f"{movie['title']} ({movie['release_year']})"):
                col1, col2 = st.columns([3, 1])
                col1.write(movie['description'])
                genres = get_genres_for_movie(movie['movie_id'])
                col1.write(f"**Genres:** {', '.join(genres)}")
                
                if col2.button("❌ Remove", key=f"remove_{movie['movie_id']}"):
                    remove_favorite(movie['movie_id'])
                    st.rerun()