# MusicMate ♫
Welcome to MusicMate, your go-to app for discovering the perfect soundtrack based on your day, mood, or even a specific song! MusicMate offers three main features:
1. Match the Day: Discover songs that fit the weather and activity of your day.
2. Match the Mood: Find songs that align with your current mood.
3. Match the Song: Get recommendations based on a song you input.
* You can also save your favorite songs and manage your Spotify playlists directly through MusicMate.

### Table of Contents
- [Setup Instructions](#set-up-instructions)
- [How to Run the Code](#how-to-run-the-code)
- [Code Overview](#code-overview)
- [Testing Information](#testing-information)
- [Acknowledgments](#Acknowledgments)

### Set Up Instructions
#### Prerequisites:
Before you begin, ensure you have the following installed:
* Python 3.6+
* requests library
* sqlalchemy library
* openai library
* os library
* dotenv library
* To install these dependencies, run:
    * ```python
      pip install requests sqlalchemy openai dotenv
      ```

#### Setting Up Environment Variables:
##### You need the following API keys:
* GPT_API_KEY=your_openai_api_key
* SPOTIFY_CLIENT_ID=your_spotify_client_id
* SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

Set these variables in your environment. The code will automatically create an SQL database to store all necessary information once it is run.


### How To Run The Code
1. **Run the script**
    * ```python
      python3 app.py
      ```
2. **Enjoy and interact with the website**
    - Follow the prompts to explore MusicMate's features and enjoy the personalized music experience.

### Code Overview
1. #### Imports:
    * **requests:** To make HTTP requests to the all the API's
    * **sqlalchemy:** To interact with the SQLite database.
    * **openai:** To interact with openai's api and get song keywords  


2. #### Constants:
    * **WEATHER_API_KEY:** Weather API key.
    * **SPOTIFY_API_KEY:** Spotify API key.  
    * **GPT_API_KEY:** Chat GPT API key.  


3. #### File Rundown:
    * app.py
        * Handles all flask logic and routing for the web app 
    * decorators.py
        * Decorators for ensuring the user is logged into the site and to Spotify before accessing different functionalities
    * get_spotify_api_key.py
        * Holds all functions to handle Spotify integration and getting the proper access
    * match_the_day.py
        * Holds all functionality for the match the day feature
    * match_the_mood.py
        * Holds all functionality for the match the mood feature
    * match_the_song.py
        * Holds all functionality for the match the song feature
    * playlist_feature.py
        * Handles logic with integrating the users Spotify playlist for in-site adding and modifying the playlists
    * save_songs.py
        * All logic for saving songs by using a SQL database to store users and their songs
    * songs.py
        * Handles the logic for retrieving, storing, and displaying the current song data form either a Spotify playlist or track
    * unit_tests.py
        * Integrated with YAML auto check to automatically run the unit tests on every push.
    * user_accounts.py
        * All logic to handle the creation and storing of user accounts using a SQL database

### Testing Information
- **To test the application, use the following Spotify account:**
    - Email: testmusicmateapp@gmail.com
    - Password: 1234567abc

### Acknowledgments
This project was developed as part of the SEO Tech Developer Program as the final project in the summer of 2024. The development team includes Elliott Tamarkin, Doug Bogle, and Charlize Aponte. We hope you enjoy using MusicMate!