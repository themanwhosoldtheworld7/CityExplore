
"""
Created on Mon Mar 20 22:49:00 2023

@author: Themanwhosoldtheworld
"""

import openai
import spacy

openai.api_key = "<your-openai-api-key>"

class PointsOfInterest:
    def __init__(self, city, location, facts=None, description=None, audio=None):
        self.city = city
        self.location = location
        self.facts = facts or []
        self.description = description or ""
        self.audio = audio or ""

    def fetch_facts(self):
        model_engine = "text-davinci-002"
        prompt = f"Generate 3-5 facts about {self.location} in {self.city}."
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        if response.choices[0].text:
            facts_text = response.choices[0].text.strip()
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(facts_text)
            self.facts = [sent.text for sent in doc.sents][:5]
            self.facts = facts_text
        else:
            self.facts = ["Sorry, I couldn't generate any facts for this location."]

    def fetch_description(self):
        model_engine = "text-davinci-002"
        prompt = f"Generate a description for {self.location} in {self.city}."
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        if response.choices[0].text:
            self.description = response.choices[0].text.strip()
        else:
            self.description = "Sorry, I couldn't generate a description for this location."
