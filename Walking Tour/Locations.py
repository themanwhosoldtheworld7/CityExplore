#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 06:35:10 2023

@author: Themanwhosoldtheworld
"""

import openai
from Secrets import openai_key
from gtts import gTTS
import requests

class Location:
    def __init__(self, name, city, facts=None, description=None, audio=None):
        self.name = name
        self.city = city
        self.facts = facts or ""
        self.description = description or ""
        self.audio = audio or ""

    def __repr__(self):
        return f"Location({self.name}, {self.city})"

    def __str__(self):
        return f"{self.name} in {self.city}"

    def get_facts(self, language):
        prompt = f"Get 3-5 interesting facts about {self.name} in {self.city} in {language}."
        model_engine = "text-davinci-002"
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=2048, n=1, stop=None, temperature=0.7)

        if response.choices[0].text:
            facts_text = response.choices[0].text.strip()
            # Split the facts text into a list based on the newline character (\n), and remove any empty lines
            facts_list = [fact.strip() for fact in facts_text.split("\n") if fact.strip()]
            # Join the facts into a paragraph
            facts_paragraph = " ".join(facts_list[:min(len(facts_list), 5)])            
            self.facts = facts_paragraph
        else:
            self.facts = "Sorry, I couldn't find any facts about this location."
    
    def get_description(self, language="English"):
        prompt = f"Write a detailed essay on {self.name} in {self.city} in {language}."
        model_engine = "text-davinci-002"
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=3500, n=1, stop=None, temperature=0.7)
    
        if response.choices[0].text:
            self.description = response.choices[0].text.strip()
            # Generate audio file for description
            audio_file = f"{self.city}_{self.name}.mp3"
            tts = gTTS(self.description, lang='en')
            tts.save(audio_file)
            self.audio = audio_file
        else:
            self.description = "Sorry, I couldn't generate a description for this location."
    
    def get_geolocation(self, api_key):
        query = f"{self.name}, {self.city}"
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                self.lat = data["results"][0]["geometry"]["location"]["lat"]
                self.lng = data["results"][0]["geometry"]["location"]["lng"]



