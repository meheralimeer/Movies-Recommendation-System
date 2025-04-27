from backend.database import (
    create_tables, add_movie, get_all_movies,
    add_genre, assign_genre, get_genres_for_movie,
    add_favorite, get_favorites
)

# ensure tables exist at startup
# create_tables()

# example usage
# movie_id = add_movie("Inception", 2010, "A thief who steals corporate secrets…")
# genre_id = add_genre("Sci-Fi")
# assign_genre(movie_id, genre_id)
print(get_all_movies())
