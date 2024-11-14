
import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.set_page_config(page_title='Movie Recommendation System', page_icon="🎬", layout='wide')
st.title('🎬 Movie Recommendation System')

st.write("""
    Welcome to the Movie Recommendation System!
    This app helps you find movies similar to the one you love based on our recommendation model. Simply select a movie, and we will suggest others you might enjoy.
    """)

# Load the data
movies = pickle.load(open("C:/Users/rajiv/Downloads/movie_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/rajiv/Downloads/similarity.pkl", 'rb'))

# Dropdown menu to select a movie
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select a Movie from the dropdown list 🎥",
    movie_list
)

# Button to trigger the recommendation
if st.button('Show Similar Movies'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Layout for displaying recommended movies in columns
    st.subheader("Here are some movies you might like based on your selection!")
    
    # Create columns for better layout
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx], use_container_width=True)
            
            # You can add some hover effects using HTML (optional)
            st.markdown(f'<a href="https://www.imdb.com/find?q={recommended_movie_names[idx]}" target="_blank">More Info</a>', unsafe_allow_html=True)





