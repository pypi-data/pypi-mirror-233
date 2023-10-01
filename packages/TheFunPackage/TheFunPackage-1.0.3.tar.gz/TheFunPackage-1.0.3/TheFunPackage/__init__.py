# TheFunPackage - Init

''' This is the __init__.py file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import os
import sys
import json
import random
import pyjokes
import requests
import randfacts
import webbrowser
import importlib_metadata
from bs4 import BeautifulSoup
from colorama import Fore, Style

# Variables - Package Information
__name__ = "TheFunPackage"
__version__ = "1.0.3"
__description__ = "This Python package is only meant for fun and to entertain you!"
__license__ = "Apache License 2.0"
__author__ = "Aniketh Chavare"
__author_email__ = "anikethchavare@outlook.com"
__github_url__ = "https://github.com/TheFunPackage/TheFunPackage-Python"
__pypi_url__ = "https://pypi.org/project/TheFunPackage"
__docs_url__ = "https://anikethchavare.gitbook.io/thefunpackage"

# Function 1 - Version Check
def version_check():
    # Variables
    system_version = importlib_metadata.version("TheFunPackage")
    package_version = BeautifulSoup(requests.get(__pypi_url__).text, "html.parser").body.main.find_all("div")[1].h1.text.strip().split()[1]

    # Checking the Version
    if (system_version < package_version):
        # Checking the Environment
        if ("idlelib.run" in sys.modules):
            print("You are using TheFunPackage version " + system_version + ", however version " + package_version + " is available.")
            print("Upgrade to the latest version for new features and improvements using this command: pip install --upgrade TheFunPackage" + "\n")
        else:
            print(Fore.YELLOW + "You are using TheFunPackage version " + system_version + ", however version " + package_version + " is available.")
            print(Fore.YELLOW + "Upgrade to the latest version for new features and improvements using this command: " + Fore.CYAN + "pip install --upgrade TheFunPackage" + Style.RESET_ALL + "\n")

# Function 2 - GitHub
def github():
    # Opening TheFunPackage's GitHub Repository
    try:
        webbrowser.open(__github_url__)
    except:
        raise Exception("An error occurred while opening the GitHub repository. Please try again.")

# Function 3 - PyPI
def pypi():
    # Opening TheFunPackage's PyPI Page
    try:
        webbrowser.open(__pypi_url__)
    except:
        raise Exception("An error occurred while opening the PyPI page. Please try again.")

# Function 4 - Docs
def docs():
    # Opening TheFunPackage's Docs
    try:
        webbrowser.open(__docs_url__)
    except:
        raise Exception("An error occurred while opening the docs. Please try again.")

# Running the "version_check()" Function
version_check()

# Function 5 - Game
def game(name):
    # Variables
    games_list = ["ant", "avoid", "bagels", "bounce", "cannon", "connect", "crypto", "fidget", "flappy", "guess", "illusion", "life", "madlibs", "maze", "memory", "minesweeper", "pacman", "paint", "pong", "rps", "simonsays", "snake", "tictactoe", "tiles", "tron", "typing", "tennis-game", "rock-paper-scissors"]

    # Checking the Data Type of "name"
    if (isinstance(name, str)):
        # Checking if "name" is Valid
        if (name in games_list):
            # Checking the Value of "name"
            if (name == "tennis-game"):
                # Opening the Tennis Game
                webbrowser.open("https://anikethchavare.vercel.app/tennis-game")
            elif (name == "rock-paper-scissors"):
                # Opening the Rock-Paper-Scissors Game
                webbrowser.open("https://anikethchavare.vercel.app/rock-paper-scissors")
            else:
                # Playing the "freegames" Game
                os.system("python -m freegames." + name)
        else:
            raise Exception("The 'name' argument must be a valid game's name. The available games are:\n\n" + str(games_list))
    else:
        raise TypeError("The 'name' argument must be a string.")

# Function 6 - Joke
def joke(topic="random"):
    # Variables
    joke_topics = ["random", "general", "programming", "knock-knock"]
    programming_joke_random = random.choice([1, 2])
    api_endpoint = "https://official-joke-api.appspot.com/jokes/{0}"

    # Checking the Data Type of "topic"
    if (isinstance(topic, str)):
        # Checking the Value of "topic"
        if (topic in joke_topics):
            # Fetching and Returning the Joke
            if (topic == "random"):
                # Fetching the Joke
                try:
                    response = json.loads(requests.get(api_endpoint.format("random")).text)
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("Something went wrong. Please try again.")

                # Returning the Joke
                return response["setup"] + " " + response["punchline"]
            elif (topic in ["general", "knock-knock"]):
                # Fetching the Joke
                try:
                    response = json.loads(requests.get(api_endpoint.format(topic + "/random")).text)[0]
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("Something went wrong. Please try again.")

                # Returning the Joke
                return response["setup"] + " " + response["punchline"]
            elif (topic == "programming"):
                # Checking the Value of "programming_joke_random"
                if (programming_joke_random == 1):
                    # Fetching the Joke
                    try:
                        response = json.loads(requests.get(api_endpoint.format(topic + "/random")).text)[0]
                    except requests.ConnectionError:
                        raise ConnectionError("A connection error occurred. Please try again.")
                    except:
                        raise Exception("Something went wrong. Please try again.")

                    # Returning the Joke
                    return response["setup"] + " " + response["punchline"]
                elif (programming_joke_random == 2):
                    # Returning the Joke
                    return pyjokes.get_joke()
        else:
            raise Exception("The 'topic' argument must be either 'random', 'general', 'programming', or 'knock-knock'.")
    else:
        raise TypeError("The 'topic' argument must be a string.")

# Function 7 - Fact
def fact(topic="general"):
    # Variables
    fact_topics = ["general", "cats"]

    # Checking the Data Type of "topic"
    if (isinstance(topic, str)):
        # Checking the Value of "topic"
        if (topic in fact_topics):
            # Fetching and Returning the Fact
            if (topic == "general"):
                # Returning the Fact
                return randfacts.get_fact(filter_enabled=True, only_unsafe=False)
            elif (topic == "cats"):
                # Fetching the Fact
                try:
                    # Returning the Fact
                    return json.loads(requests.get("https://catfact.ninja/fact").text)["fact"]
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("Something went wrong. Please try again.")
        else:
            raise Exception("The 'topic' argument must be either 'general' or 'cats'.")
    else:
        raise TypeError("The 'topic' argument must be a string.")

# Function 8 - Bored
def bored():
    # Fetching and Returning the Data
    try:
        # Fetching the Activity
        response = json.loads(requests.get("https://boredapi.com/api/activity").text)

        # Deleting Unwanted Keys
        del response["price"]
        del response["key"]

        # Returning the Activity
        return response
    except requests.ConnectionError:
        raise ConnectionError("A connection error occurred. Please try again.")
    except:
        raise Exception("Something went wrong. Please try again.")