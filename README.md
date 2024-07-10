# WeatherTunes 🌤️ 🎶
Welcome to WeatherTunes, where you can discover the perfect soundtrack for your day based on the weather and your activities!

### Table of Contents
- [Setup Instructions](#set-up-instructions)
- [How to Run the Code](#how-to-run-the-code)
- [Overview of the Code](#overview-of-the-code)

### Set Up Instructions
#### Prerequisites:
Before you begin, ensure you have the following installed:
* Python 3.6+
* requests library
* sqlalchemy library
* openai library
* os library
* pandas library
* To install:
    * ```python
      pip install requests sqlalchemy pandas os openai
      ```


#### Setting Up The Repository:
    **Set up environment variables**
        * Obtain an API key from the Google Developer website for the YouTube Data API.
        * Set the API_KEY variable in your code with this obtained key.

### How To Run The Code
1. **Run the script**
    * ```python
      python3 weather_tunes.py
      ```
2. **Follow the prompts**
    * Enter a location when asked
      * Type y(yes) or n(no) if you see the correct city
    * Enter your activity, feel free to be descriptive! 

3. **Check the output**
    * Decide what genre you're feeling!
        * Confused? respond with y to get the list of genres
    * Decide if you want the extended or basic song info
    * Finally, either decide your done or search through all the genres!

### Overview Of The Code
1. #### Imports:
    * **requests:** To make HTTP requests to the all the API's
    * **sqlalchemy:** To interact with the SQLite database.
    * **pandas:** To handle data manipulation and storage.  
     * **openai:** To interact with openai's api and get song keywords  


2. #### Constants:
    * **WEATHER_API_KEY:** Weather API key.
    * **SPOTIFY_API_KEY:** Spotify API key.  
    * **GPT_API_KEY:** Chat GPT API key.  


3. #### Functions:
    * weather_tunes.py:
        * **welcome_user():** Prints out a pretty welcoming message.
        * **weather_forecast():** Until correct location is confirmed, asks user for their desired location,
        returns temp in farenheit, weather description (e.g. Partly Cloudy), and name of location.  
        * **users_activity():** Until the user enters a valid activity (less than 50 characters), prompts user to
        enter in their activity, returns this as string.  
        * **get_query_words():** Asks the Chat GPT API for some keywords based on the weather and user's 
        desired activity, returns these keywords as a string.  
        * **get_songs_from_genre():** After database is created, prompts user for their desired genre, ensuring
        they enter in a valid genre and providing a list of genres to help. Returns a list of song info stored 
        in tuples.
        * **show_genre_list():** Includes logic for asking user if they'd like to see the list of genres,
        a helper called by other functions. 
        * **list_of_genres():** Returns the list of genres stored in spotify_genres.py. 
        * **final_response(activity, city, weather_stats, songs):** Presents the songs from desired genre with 
        some pretty emoji's, and ensures user can ask to investigate songs from another genre if they want. 
    * genre_database.py:
        * **create_db(query_words):** Uses Chat GPT's activity words to send a GET request to Spotify API, adds
        this info to a dictionary where each value represents a song's info. Calls the following function to 
        add this dict to the database as a table 
        * **dict_to_table():** Simply uses pandas to take the provided dictionary and turn it into a table in
        our database. 

  
4. #### Main Logic:
    * Prompts the user for a location
    * Sends a GET request to weather API to find some info about this location's weather
    * Prompts the user for the activity they will be doing
    * Asks openai API for some keywords based on the users activity and weather
    * Sends a GET request to Spotify API to find songs matching these keywords in different genres
    * Creates a database
    * Stores the songs retrieved for every genre in a database (each genre as a table)
    * Continually asks user which genre they'd like to see, returning song info after
    a correct genre name has been answered
    * Does this by querying the database to ask if the user-inputted genre is a table in it
    * Stops returning when user wishes to 


5. #### Error Handling:
    * Ensures correct weather location entered
    * Ensures no bogus genres can be entered
    * Doesn't allow activity description over 50 characters to avoid comprehension errors

