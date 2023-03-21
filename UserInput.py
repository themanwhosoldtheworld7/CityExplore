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
from Secrets import openai_key
from Secrets import maps_key
import re

openai.api_key = openai_key

class WalkingTour:
    interests_options = ["history", "nightlife", "architecture", "famous places"]

    def __init__(self, city, interests, duration=2, user_specifications=None):
        self.city = city
        self.interests = interests
        self._duration = duration
        self._user_specifications = user_specifications or "None"
        self.trip = []

    @classmethod
    def create_walking_tour(cls):
        city = input("Enter the city you would like to take a walking tour in: ")
        interests = input(f"Enter your interests from the following options ({', '.join(cls.interests_options)}): ")
        duration = int(input("Enter the duration of the walking tour in hours (default is 2 hours): ") or "2")
        user_specifications = input("Enter any specific requests or specifications: ")

        return cls(city, interests, duration, user_specifications)

    def generate_trip_prompt(self):
        prompt = f"Generate a walking tour of {self.city} that is {self._duration} hours long and includes the following interests: {self.interests}. {self._user_specifications} Provide a list of locations to visit in the order you would like to visit them, with a brief description of each location.\n\n"
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

class Location:
    def __init__(self, name, city, facts=None, description=None, audio=None):
        self.name = name
        self.city = city
        self.facts = facts or []
        self.description = description or ""
        self.audio = audio or ""

    def __repr__(self):
        return f"Location({self.name}, {self.city})"

    def __str__(self):
        return f"{self.name} in {self.city}"

def main():
    tour = WalkingTour('Munich', 'sports', 2)
    tour.generate_trip_plan()

    
        
if __name__ == "__main__":
    main()
    tour = WalkingTour('Munich', 'sports', 2)
    tour.generate_trip_plan()










