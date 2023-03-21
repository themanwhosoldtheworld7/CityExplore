#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:04:21 2023

@author: Themanwhosoldtheworld
"""

""" Get user Input 
I am trying to create an application using chat gpt code, with minimal human additions.
I am exploring the ways in which chat gtp can be used to help create propotypes, even amongst
non technically inclined users, and create product velocity
"""
import openai
import json
import Locations as loc
from Secrets import openai_key
from Secrets import maps_key
import re
import folium
import os
import datetime

openai.api_key = openai_key



class WalkingTour:
    interests_options = ["history", "nightlife", "architecture", "famous places"]

    def __init__(self, city, interests, duration=2, language = 'en' ,user_specifications=None):
        self.city = city
        self.interests = interests
        self._duration = duration
        self._user_specifications = user_specifications or "None"
        self.language = language or "english"
        self.trip = []
        
        now = datetime.datetime.now()
        dir_name = now.strftime("%Y%m%d_%H%M")
        os.mkdir(dir_name)
        # Set the new directory as the working directory
        os.chdir(dir_name)


    @classmethod
    def create_walking_tour(cls):
        city = input("Enter the city you would like to take a walking tour in: ")
        interests = input(f"Enter your interests from the following options ({', '.join(cls.interests_options)}): ")
        duration = int(input("Enter the duration of the walking tour in hours (default is 2 hours): ") or "2")
        language = input("Enter language code en, de, es, fr")
        user_specifications = input("Enter any specific requests or specifications: ")
        

        return cls(city, interests, duration, language, user_specifications)

    def generate_trip_prompt(self):
        prompt = f"Generate a walking tour of {self.city} that is {self._duration} hours long and includes the following interests: {self.interests}. {self._user_specifications} Provide only list of locations to visit"
        return prompt

    def generate_trip_plan(self):
        prompt = self.generate_trip_prompt()
        model_engine = "text-davinci-002"
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.7)
        if response.choices[0].text:
            trip_text = response.choices[0].text.strip()
            # Split the trip text into a list based on the newline character (\n)
            self.trip = re.split(r"\n\d+\.\s", trip_text)
            # Remove leading serial numbers from each item in the list
            self.trip = [re.sub(r"^\d+\.\s", "", item).strip() for item in self.trip]
        else:
            self.trip = ["Sorry, I couldn't generate a trip plan for you."]
    
    def generate_locations(self):
        self.trip_locations = []
        for item in self.trip:
            location = loc.Location(item, self.city)
            location.get_facts(self.language)
            location.get_description(self.language)
            location.get_geolocation(maps_key)
            self.trip_locations.append(location)


    def plot_on_map(self):
        # Create a map centered on the city
        city = loc.Location(self.city, self.city)
        city.get_geolocation(maps_key)        
        map_center = (city.lat, city.lng)
        map_zoom = 14
        tour_map = folium.Map(location=map_center, zoom_start=map_zoom)

        # Plot each location on the map
        for location in self.trip_locations:
            marker_text = f"{location.name}: {location.facts}"            
            marker_location = (location.lat, location.lng)
            popup = folium.Popup(marker_text, max_width=300)
            folium.Marker(location=marker_location, popup=popup).add_to(tour_map)

        # Save the map as a file and set it as a self variable
        filename = f"{self.city}.html"
        tour_map.save(filename)        
        return



    def __repr__(self):
        return f"Location({self.name}, {self.city})"

    def __str__(self):
        return f"{self.name} in {self.city}"


tour = WalkingTour('Munich', 'architecture', 2)
tour.generate_trip_plan()
tour.generate_locations()
tour.plot_on_map()    










