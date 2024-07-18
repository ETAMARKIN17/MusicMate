from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from get_spotify_api_key import *
from songs import *
from user_accounts import *
from match_the_day import *
from decorators import *
from save_songs import *

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Get API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GPT_API_KEY = os.getenv('GPT_API_KEY')


# Route for home page
@app.route('/')
def home():
    session.clear()  # Clear session variables
    return render_template('home.html')


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        if user:
            session['user_id'] = user['user_id']  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password. Please try again.", "danger")
    return render_template('login.html')


# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for('register'))

        user_id, error_message = register_user(username, password)
        if user_id is not None:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash(error_message, "danger")
    return render_template('register.html')


# Route for user dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Clear city, activity, and genre session variables
    session.pop('city', None)
    session.pop('activity', None)
    session.pop('genre', None)

    return render_template('dashboard.html', user=user)


# Route to access the features page
@app.route('/discover')
@login_required
def discover():
    return render_template('discover.html')


# Route for collecting information for the match the day feature
@app.route('/match_the_day_info', methods=['GET', 'POST'])
@login_required
def match_the_day_info():
    if request.method == 'POST':
        city = request.form['city']
        activity = request.form['activity']
        genre = request.form['genre']
        session['city'] = city  # Set city in session
        session['activity'] = activity  # Set activity in session
        session['genre'] = genre  # Set genre in session
        return redirect(url_for('match_the_day'))
    
    # Reset city, activity, and genre if navigating back
    session.pop('city', None)
    session.pop('activity', None)
    session.pop('genre', None)
    genres = get_spotify_genres()
    return render_template('match_the_day_info.html', genres=genres)


# Route for matching the day (finding songs)
@app.route('/match_the_day')
@login_required
def match_the_day():
    if 'city' not in session or 'activity' not in session or 'genre' not in session:
        flash("Please fill in all necessary info first.", "info")
        return redirect(url_for('match_the_day_info'))
    
    city = session['city']
    activity = session['activity']
    genre = session['genre']
    
    # Get weather stats
    weather_stats, city_name = weather_forecast(city, WEATHER_API_KEY)
    
    # Get query words from GPT-3
    query_words = gpt_query_words(weather_stats, activity, GPT_API_KEY)
    
    # Get songs from Spotify API
    songs = recommend_songs(query_words, genre)
    
    if songs:
        return render_template('match_the_day.html', songs=songs, query_words=query_words, activity=activity, city=city_name, weather_stats=weather_stats)
    else:
        flash("No songs found. Please try again.", "info")
        return redirect(url_for('dashboard'))


# Route for saving a song
@app.route('/save_a_song', methods=['POST'])
def save_a_song():
    if request.method == 'POST':
        user_id = session.get('user_id')
        song_name = request.form['song_name']
        artist_name = request.form['artist_name']
        album_name = request.form['album_name']
        song_link = request.form['song_link']
        
        song_id = save_song(user_id, song_name, artist_name, album_name, song_link)
        if song_id:
            flash("Song saved successfully!", "success")
        else:
            flash("Failed to save song. Please try again.", "danger")
        
        return redirect(url_for('match_the_day'))


# Route for viewing saved songs
@app.route('/saved_songs')
def saved_songs():
    user_id = session.get('user_id')
    saved_songs = get_saved_songs(user_id)
    return render_template('saved_songs.html', saved_songs=saved_songs)


# Route for deleting a saved song
@app.route('/delete_saved_song/<int:song_id>', methods=['POST'])
def delete_saved_song(song_id):
    user_id = session.get('user_id')
    if user_id:
        success = delete_saved_song_by_id(user_id, song_id)
        if success:
            flash("Song deleted successfully.", "info")
        else:
            flash("Failed to delete song. Please try again.", "danger")
    else:
        flash("User not found.", "danger")
    return redirect(url_for('saved_songs'))


# Route for logging out
@app.route('/logout')
def logout():
    session.clear()  # Clear all session variables
    return redirect(url_for('home'))


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
