import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

class MovieRecommender:
    def __init__(self, movies_path, credits_path):
        self.movies_path = movies_path
        self.credits_path = credits_path
        self.movies = None
        self.cosine_sim = None
        self._prepare()

    def _prepare(self):
        # Load datasets
        movies = pd.read_csv(self.movies_path)
        credits = pd.read_csv(self.credits_path)
        movies = movies.merge(credits, on='title')

        # Keep relevant columns
        movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        
        # Process features
        def extract_names(obj, key='name', limit=None):
            try:
                items = ast.literal_eval(obj)
                if key == 'name':
                    names = [item[key] for item in items]
                    if limit:
                        names = names[:limit]
                    return names
                elif key == 'job':
                    return [item['name'] for item in items if item.get('job') == 'Director']
                return []
            except:
                return []
        
        movies['genres'] = movies['genres'].apply(lambda x: extract_names(x))
        movies['keywords'] = movies['keywords'].apply(lambda x: extract_names(x))
        movies['cast'] = movies['cast'].apply(lambda x: extract_names(x, limit=3))
        movies['crew'] = movies['crew'].apply(lambda x: extract_names(x, key='job'))
        movies['overview'] = movies['overview'].fillna('')
        
        movies['tags'] = movies['overview'] + ' ' + \
                         movies['genres'].apply(lambda x: ' '.join(x)) + ' ' + \
                         movies['keywords'].apply(lambda x: ' '.join(x)) + ' ' + \
                         movies['cast'].apply(lambda x: ' '.join(x)) + ' ' + \
                         movies['crew'].apply(lambda x: ' '.join(x))
        
        self.movies = movies[['movie_id', 'title', 'tags']]

        # Vectorization and similarity matrix
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.movies['tags'])
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def recommend(self, title, top_n=10):
        if title not in self.movies['title'].values:
            return f"Movie '{title}' not found in database."
        
        idx = self.movies[self.movies['title'] == title].index[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]

        recommended_titles = [self.movies.iloc[i[0]]['title'] for i in sim_scores]
        return recommended_titles
