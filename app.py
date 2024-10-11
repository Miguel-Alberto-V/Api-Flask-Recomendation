from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import polars as pl

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Reemplazar '::' por ',' en los archivos
with open('ml-1m/ratings.dat', 'r', encoding='ISO-8859-1') as f:
    ratings_data = f.read().replace('::', ',')

with open('ml-1m/movies.dat', 'r', encoding='ISO-8859-1') as f:
    movies_data = f.read().replace('::', ',')

with open('ml-1m/users.dat', 'r', encoding='ISO-8859-1') as f:
    users_data = f.read().replace('::', ',')

# Guardar los archivos modificados temporalmente
with open('ml-1m/ratings_cleaned.csv', 'w', encoding='ISO-8859-1') as f:
    f.write(ratings_data)

with open('ml-1m/movies_cleaned.csv', 'w', encoding='ISO-8859-1') as f:
    f.write(movies_data)

with open('ml-1m/users_cleaned.csv', 'w', encoding='ISO-8859-1') as f:
    f.write(users_data)

# Cargar los datos con Polars utilizando ',' como separator y codificación ISO-8859-1
ratings = pl.read_csv('ml-1m/ratings_cleaned.csv', separator=',', has_header=False, 
                      new_columns=['UserID', 'MovieID', 'Rating', 'Timestamp'], encoding='ISO-8859-1',
                      truncate_ragged_lines=True, ignore_errors=True)
movies = pl.read_csv('ml-1m/movies_cleaned.csv', separator=',', has_header=False, 
                     new_columns=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1',
                     truncate_ragged_lines=True, ignore_errors=True)
users = pl.read_csv('ml-1m/users_cleaned.csv', separator=',', has_header=False, 
                    new_columns=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], encoding='ISO-8859-1',
                    truncate_ragged_lines=True, ignore_errors=True)

# Implementación de la distancia Manhattan
def manhattan_distance(user1_ratings, user2_ratings):
    common_movies = set(user1_ratings.keys()).intersection(set(user2_ratings.keys()))
    if len(common_movies) == 0:
        return float('inf')  # Si no tienen películas en común, devolver una distancia muy alta
    distance = sum(abs(user1_ratings[movie] - user2_ratings[movie]) for movie in common_movies)
    return distance

# Obtener las calificaciones de un usuario
def get_user_ratings(user_id):
    user_ratings = ratings.filter(pl.col('UserID') == user_id)
    return dict(zip(user_ratings['MovieID'].to_list(), user_ratings['Rating'].to_list()))

# Generar recomendaciones
def recommend_movies(target_user_id, k=5):
    target_user_ratings = get_user_ratings(target_user_id)
    
    distances = []
    for user_id in ratings['UserID'].unique():
        if user_id != target_user_id:
            user_ratings = get_user_ratings(user_id)
            distance = manhattan_distance(target_user_ratings, user_ratings)
            distances.append((user_id, distance))
    
    distances.sort(key=lambda x: x[1])
    closest_user_id = distances[0][0]
    
    closest_user_ratings = get_user_ratings(closest_user_id)
    recommendations = [movie for movie in closest_user_ratings if movie not in target_user_ratings]
    
    recommended_movies = sorted(recommendations, key=lambda movie: closest_user_ratings[movie], reverse=True)[:k]
    
    recommended_movies_info = []
    for movie_id in recommended_movies:
        movie_info = movies.filter(pl.col('MovieID') == movie_id)[['MovieID', 'Title']].row(0)
        rating = closest_user_ratings[movie_id]
        recommended_movies_info.append({
            'MovieID': movie_info[0],
            'Title': movie_info[1],
            'Rating': rating
        })
    
    return recommended_movies_info

# API Endpoint para obtener recomendaciones
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = int(request.args.get('user_id'))  # Obtener el user_id de los parámetros de la URL
    k = int(request.args.get('k', 5))  # Obtener el número de recomendaciones (default: 5)
    
    recommendations = recommend_movies(user_id, k)
    
    return jsonify({
        'user_id': user_id,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
