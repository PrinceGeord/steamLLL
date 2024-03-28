# SteamLLL - Does your game Live, Laugh and Love?
## The Goal - Use Steam Game Reviews to Generate Actionable Feedback
Steam game reviews are notoriously controversial in the video game industry, many developers completely ignore them as they find it impossible to get a concensus that would provide valuable feedback and direct how they develop their game.

This app aims to find if there is a golden nugget of truth in all those Steam reviews, to see if any useful insights can be drawn from the Steam community that could perhaps help game devs improve their game or capture a wider audience

## Project Description

This application uses the Steam Web API to acquire their latest reviews (forming our "corpus") for a video game and then performs keyword extraction on those reviews and then produces the results in the form of a WordCloud.

A key challenge was the limitations imposed by the Steam Web API. 

Steam limits you to 100,000 API calls a day which seems plenty, however there seems to be a less explicit limiter of roughly 200-300 requests every 5 minutes or you will trigger a 429 Error Code.

This is further compounded by the fact you will only be able to acquire info for a specific app one api call at a time and steam posesses roughly 150,000 apps in their database - furthermore I was unable to find a way to get more than 100 reviews per API call. (if someone does find a way, please let me know!)

Due to these limitations, this app tries to focus on building a database in small increments and providing analysis on request while caching the results for future queries a



NOTE: 
- The [TeamFortress2 Wiki](wiki.teamfortress.com/wiki/User:RJackson/StoreFrontAPI#Parameters) provides a really good resource for understanding the SteamWebAPI and comes highly recommended!

- This app is configured for "English" reviews although this app can be repurposed to work with other language


### Technologies Used

#### PostgreSQL

Freely available and good for small time projects like this, plenty of resources are available about this Open-Source Relational Database Management System

#### Yake (Yet Another Keyword Extractor)

YAKE is an automatic keyword extraction method which is light weight and easy to use, good for someone's first venture into the realm of Natural Language Processing (NLP) (as this is my first venture into the realm of NLP).

You can use it without any models to try and obtain some keywords, however as the steam community is a mixed bag and there are various different dialects in play - it becomes necessary to try and apply some sort of cleaning to try and improve the outputs.

#### SparkNLP Library

Is an open-source library that provides language models. In this project we use it for its Stopword Cleaner and Lemmatization libraries

"Stopwords" - are words that do not really add any information to a sentence but simply allow conversation to flow better e.g. 'a', 'an', 'and' etc

In our case we use the Stopword Cleaner to remove these words from the corpus allowing keyword extraction to focus on the other words.

"Lemmatization" - refers to breaking down words to their root meaning 

e.g. "builds", "building" and "built" will be reduced down to "build"

This step was necessary to try and get some commonality between the steam reviews as, even with limiting ourselves to just one language, the range of vocabularies used among the steam community is surprisingly large!

#### Streamlit

The front-end is built with Streamlit and provides quite an easy way to deploy a data app and most importantly - it was free.

This app is built run by running Streamlit locally or to be deployed on the Streamlit Community Cloud

## Installation Instructions

Python 3.10.12

Create a global secrets file at:
 ~/.streamlit/secrets.toml  for macOS/Linux
%userprofile%/.streamlit/secrets.toml   for Windows

Within the secrets.toml type in your database credentials:

host='<*database_URL* or *localhost*>'
database='*name_of_DB*'
user='*your_username*'
password='*your_password*'
options='-c search_path=schema_name' 


*options  is optional, and may not be required depending on your database structure*

### Deploying Locally:

Install streamlit v1.32.2

pip install all the packages listed in the requirements.txt

`streamlit run streamlit_app.py`

### Deploying to Streamlit Community Cloud

The requirements.txt should contain the names of all your packages, if you end up adding additional packages - ensure you list them in the requirements.txt

The packages.txt should also have default-jre listed, which is required for the spark packages to run

Navigate to streamlit.io/cloud and follow instructions for deploying a new app - the project needs to be in an accessible github repo. Ensure you populate the secrets field with your database credentials (as written at the top of this section [Installation Instructions](#installation-instructions))

### Database Setup

#### Create the tables
Run the create_tables() function from the createTables.py

#### Populate your database with steam inventory

Run the insertGames.py script, this should run "insert_games(get_all_games())"

#### Populate your games table with more information for improved performance (optional)

With each query the information for each game is stored in the database for future queries, and so the database will gradually improve in performance over time (e.g. thumbnails for each video game, search queries become more accurate)

You can accelerate this process by running the batchRuns.py script and specify the number of games you wish to update.

This function has an artificial pause in place, this is to avoid incurring a 429 error when querying the SteamAPI

#### Improving the Speed of the Keyword Extraction

The keyword extraction is a very expensive process and can take several minutes to load each result, which is why the database will automatically cache results for that day to improve the speed for future queries.

You can further meddle with the parameters in the keyword_extract.py file and modifying the get_keywords function and changing the following parameters:

.setMinNGrams(1)        this defines the minimum number of words a key phrase should have - lower should result in improved performance (cannot be <1)
.setMaxNGrams(3)  this defines the maximum number of words a key phrase should have - lower should improve performance
.setNKeywords(200)      extracts the top n keywords, smaller number results in improved speed but less quality of result

Note: the range between setMinNGrams and setMaxNGrams will also play a part in the speed of performance, bigger range means more possible phrase combinations to work through.



## How to use the App

When the app is running, you should be greeted by the home page with a search bar

Input the game you would like to query (it is currently case-sensitive, which is to be fixed in the future)

Then click the search button on one of the items in the results. If the query has already been made that day, then the keyword extraction result will already be saved to the database and will be returned to the client immediately. Otherwise it will perform the keyword extraction process which can take 2-3 mins.

By default you will be presented with the Positive feedback first (steam reviews who recommended the game in question) and if you click the "Get Negative Feedback" button, the Negative feedback will be displayed

## Known bugs

If video games don't have enough reviews an error message will display about 'p_keywords' or 'n_keywords' not being found - these games simply need more data. This will be fixed in the future to provide a more intuitive error message



