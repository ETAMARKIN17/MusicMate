from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from api_key import *
from songs import *
from user_accounts import *
from info_for_songs import *
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

# Admin credentials
ADMIN_USERNAME = 'Admin'
ADMIN_PASSWORD = 'MainAdmin'


# Route for home page
@app.route('/')
def home():
    session.clear()  # Clear session variables
    return render_template('home.html')


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_id = request.form['username_or_id']
        password = request.form['password']
        user = login_user(username_or_id, password)
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
    is_admin_user = is_admin(user_id)  # Check if the current user is an admin

    # Clear city, activity, and genre session variables
    session.pop('city', None)
    session.pop('activity', None)
    session.pop('genre', None)

    return render_template('dashboard.html', user=user, is_admin_user=is_admin_user)


# Route for admin dashboard
@app.route('/admin')
@login_required
def admin():
    user_id = session['user_id']
    if not is_admin(user_id):
        flash("Unauthorized access. Only admin can access the admin dashboard.", "danger")
        return redirect(url_for('dashboard'))

    user = get_user_by_id(user_id)  # Fetch the user details
    return render_template('admin.html', user=user)


# Route for viewing all users (admin only)
@app.route('/view_users')
@login_required
def view_users():
    if not is_admin(session.get('user_id')):
        flash("Unauthorized access. Only admin can view users.", "danger")
        return redirect(url_for('dashboard'))

    users = get_all_users()
    return render_template('view_users.html', users=users)


# Route for clearing users table (admin only)
@app.route('/clear_users', methods=['GET', 'POST'])
@login_required
def clear_users():
    if not is_admin(session.get('user_id')):
        flash("Unauthorized access. Only admin can clear users table.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        check_confirmation = request.form.get('confirmation', '')
        if check_confirmation == 'yes':
            clear_users_table()
            flash("Users table cleared successfully.", "info")
        else:
            flash("Operation aborted. Users table not cleared.", "info")
        return redirect(url_for('dashboard'))
    return render_template('clear_users.html')


# Route to start the WeatherTunes process
@app.route('/start')
@login_required
def start():
    return render_template('start.html')


# Route for collecting information for songs
@app.route('/info_for_activity', methods=['GET', 'POST'])
@login_required
def info_for_activity():
    if request.method == 'POST':
        city = request.form['city']
        activity = request.form['activity']
        genre = request.form['genre']
        session['city'] = city  # Set city in session
        session['activity'] = activity  # Set activity in session
        session['genre'] = genre  # Set genre in session

        #return redirect(url_for('song_matches'))
        songs, weather_stats = get_songs_from_activity(city, activity, genre)

        return render_template('song_matches.html', songs=songs, city=city, activity=activity, weather_stats=weather_stats)

    # Reset city, activity, and genre if navigating back
    session.pop('city', None)
    session.pop('activity', None)
    session.pop('genre', None)
    genres = get_spotify_genres()
    return render_template('info_for_activity.html', genres=genres)


# Route for collecting information for songs
@app.route('/info_for_mood', methods=['GET', 'POST'])
@login_required
def info_for_mood():
    if request.method == 'POST':
        mood = request.form['mood']
        genre = request.form['genre']
        session['mood'] = mood  # Set mood in session
        session['genre'] = genre  # Set genre in session

        songs, mood = get_songs_from_mood(mood, genre)

        #print(songs)
        return render_template('song_matches.html', songs=songs, mood=mood)

    # Reset if navigating back
    session.pop('mood', None)
    session.pop('genre', None)
    genres = get_spotify_genres()
    return render_template('info_for_mood.html', genres=genres)


# Route for collecting information for songs
@app.route('/info_for_similar', methods=['GET', 'POST'])
@login_required
def info_for_similar():
    if request.method == 'POST':
        original_song = request.form['song']
        session['original_song'] = original_song

        songs = get_similar_songs(original_song)
        
        return render_template('song_matches.html', songs=songs, original_song=original_song)

    # Reset if navigating back
    session.pop('original_song', None)
    genres = get_spotify_genres()
    return render_template('info_for_similar.html', genres=genres)


@app.route('/song_matches', methods=['GET','POST'])  # redirect to dashboard
@login_required
def song_matches():  # make this reusable to display similar songs and mood songs and activity songs
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
    
    previous_page = session.get('previous_page')
    if previous_page == 'info_for_activity':
        city = session.get('city')
        activity = session.get('activity')
        weather_stats = session.get('weather_stats')
        songs = get_songs_from_activity(city, activity, genre)
        return render_template('song_matches.html', songs=songs, city=city, activity=activity, weather_stats=weather_stats)
    elif previous_page == 'info_for_mood':
        mood = session.get('mood')
        genre = session.get('genre')
        songs = get_songs_from_mood(mood, genre)
        return render_template('song_matches.html', songs=songs, mood=mood)
    elif previous_page == 'info_for_similar':
        original_song = session.get('original_song')
        songs = get_similar_songs(original_song)
        return render_template('song_matches.html', songs=songs, original_song=original_song)
    else:
        flash("No songs found. Please try again.", "danger")
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
        
        return redirect(url_for('song_matches'))


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


# Route for discovering new music (not implemented here, just for structure)
@app.route('/discover')
@login_required
def discover():
    return render_template('discover.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.clear()  # Clear all session variables
    return redirect(url_for('home'))


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
