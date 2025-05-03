import streamlit as st
from backend.model_handler import get_movie_recommendations

# Page settings
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# App title
st.markdown(
    """
    <h1 style='text-align: center; color: #ff4b4b;'>🎬 Movie Recommender System</h1>
    <p style='text-align: center;'>Find your next favorite movie!</p>
    """,
    unsafe_allow_html=True
)


# --- SEARCH BAR ---
movie_name = st.text_input("🔎 Search for a movie:", "")

# --- Decide What to Show ---
if movie_name:
    st.markdown("---")
    st.subheader(f"🎯 Recommendations based on: **{movie_name}**")
    movies_to_show = get_movie_recommendations(movie_name)
else:
    st.markdown("---")
    st.subheader("🔥 Popular Movies Right Now:")
    movies_to_show = get_movie_recommendations("Popular")  # Show default movies

# --- Show Movies ---
cols = st.columns(5)
for idx, movie in enumerate(movies_to_show):
    with cols[idx]:
        #st.image(movie["poster_url"], width=180)
        st.markdown(f"<h5 style='text-align: center; color: #00adb5;'>{movie['title']}</h5>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>⭐ {movie['rating']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>🎬 {movie['genres']}</p>", unsafe_allow_html=True)
        if st.button("❤️ Add to Favorites", key=idx):
            st.success(f"Added {movie['title']} to favorites!")
