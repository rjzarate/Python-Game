import google.generativeai as genai
import os

class AI():
    def __init__(self, api_key):
        self.api_key = api_key

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_chat(self):
        self.chat = self.model.start_chat()

        # initial prompt
        self.chat.send_message("Create an animal/creature from a difficulty level of 1-100 (Difficulty 1 = Ant, Difficulty 100 = Dragon). Output only the name.")

    def generate_creature(self, difficulty = 1):
        # Generate creature
        return self.chat.send_message(f"Create a new animal/creature of **Difficulty {difficulty}**. Output only the name.").text[:-1]
    
    def determination_of_prompt(self, creature: str, method: str):
        # Determine if user beats the creature
        determination = self.chat.send_message(f'In a fantasy setting, for the {creature} you created, Do I defeat the {creature} by: "{method}"? Output **ONLY a number "0 to 100" of the chances I beat the {creature}**, or **"CHEATING" if I use powers that an average human CANNOT do**.')
        
        print("Determination: " + determination.text[:-1])
        
        if ("cheating" in determination.text.lower()):
            return 0
        
        try:
            return int(determination.text[:-1])
        except:
            return 0
        
    
    def get_nouns(self, text: str):
        nouns = self.model.generate_content('Read this quote: "' + text + '" and get only the nouns. Separate them by spaces.')
        return nouns.text[:-1].split()
    
    def get_creativity(self, text: str):
        creativity = self.model.generate_content('Read this quote: "' + text + '". Rate the quote\'s creativity in from 0 to 100. Only output the number.')
        return int(creativity)

    def get_reasoning_of_failure(self, creature: str, method: str):
        return self.chat.send_message(f'In a fantasy setting, why doesn\'t {method} defeat the {creature}? Explain in 1 sentence, 75 characters maximium.')