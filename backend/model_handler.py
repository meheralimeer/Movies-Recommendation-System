import pickle
import pandas as pd
import re

# Define the path to your model file (adjust as needed)
MODEL_PATH = 'backend/movie_recommendation_model.pkl'

# Load the model data when the module is imported
try:
    with open(MODEL_PATH, 'rb') as file:
        model_data = pickle.load(file)
    print("Model data loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    model_data = None
except Exception as e:
    print(f"Error loading model data: {e}")
    model_data = None

def get_movie_recommendations(movie_title):
    """
    Get movie recommendations based on the input movie title.

    Args:
        movie_title (str): The title of the movie for which recommendations are needed.

    Returns:
        list: A list of recommended movie titles. Returns an empty list if the movie is not found or if there's an error.
    """
    if model_data is None:
        print("Error: Model data is not loaded.")
        return []

    try:
        # Extract components from the pre-loaded model data
        cosine_sim = model_data.get('cosine_sim')
        movies_list = model_data.get('movies')
        indices_dict = model_data.get('indices')

        # Check if all required components are present
        if cosine_sim is None or movies_list is None or indices_dict is None:
            print("Error: Incomplete model data.")
            return []

        # Convert model data into usable formats
        movies_df = pd.DataFrame(movies_list)
        indices = pd.Series(indices_dict)

        # Process the input movie title (remove spaces and hyphens, convert to lowercase)
        processed_title = re.sub(r'[- ]', '', movie_title).lower()

        # Check if the movie exists in the indices
        if processed_title not in indices:
            print(f"Error: Movie '{movie_title}' not found.")
            return []

        # Get the index of the movie
        idx = indices[processed_title]

        # Compute similarity scores and get top 10 recommendations
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Exclude the movie itself and get top 10
        movie_indices = [i[0] for i in sim_scores]
        recommendations = movies_df['title'].iloc[movie_indices].tolist()

        return recommendations

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []