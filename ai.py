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
        self.chat.send_message("Give an animal/creature from a difficulty level of 1-100 (Difficulty 1 = Ant, Difficulty 100 = Dragon). Output only the name.")

    def generate_creature(self, difficulty = 1):
        # Generate creature
        return self.chat.send_message(f"Create an animal/creature of **Difficulty {difficulty}**. Output only the name.").text[:-1]
    
    def determination_of_prompt(self, creature: str, method: str):
        # Determine if user beats the creature
        determination = self.chat.send_message(f'In a fantasy setting, for the {creature} you just created, Do I defeat the {creature} by: "{method}"? Output **"YES" if I defeat it**, or **"NO" if I do not defeat it**.')

        if ("yes" in determination.text.lower()):
            return True
        else:
            return False

    def get_reasoning_of_failure(self, creature: str, method: str):
        return self.chat.send_message(f'In a fantasy setting, why doesn\'t {method} defeat the {creature}? Explain in 1 sentence, 75 characters maximium.')
        

# api_key = ""
# def set_api_key(k=""):
#     # setup model and api
#     try:
#         # Grab api key in environment (MacOS: env)
#         api_key = os.environ["GEMINI_API_KEY"]
#     except KeyError as _:
#         api_key = k


# model = ""
# def generate_model():
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-flash")

# def generate_chat():
#     # Setup chat bot
#     chat = model.start_chat()
#     chat.send_message("Give an animal/creature from a difficulty level of 1-100 (Difficulty 1 = Ant, Difficulty 100 = Dragon). Output only the name.")

#     # Starting difficulty
#     input_difficulty = input("Input difficulty (1 = Mouse, 100 = Dragon):\n")
#     difficulty = 1
#     if (input_difficulty.isdigit()):
#         difficulty = int(input_difficulty)

#     # Continue until player is defeated
#     defeated = True
#     while (defeated):
#         # Generate creature
#         creature = chat.send_message(f"Create an animal/creature of **Difficulty {difficulty}**. Output only the name.").text[:-2]
#         print(creature)

#         # Ask user for input
#         method = input(f"How do you defeat the {creature}? Your input:\n")

#         # Determine if user beats the creature
#         determination = chat.send_message(f'In a fantasy setting, for the {creature} you just created, Do I defeat the {creature} by: "{method}"? Output **"YES" if I defeat it**, or **"NO" if I do not defeat it**.')
        
#         if ("yes" in determination.text.lower()):
#             defeated = True
#             print(f'You defeated the {creature}! However, there is another creature in your path...')
#             difficulty += 1
#         else:
#             defeated = False
#             reasoning = chat.send_message(f'In a fantasy setting, why doesn\'t {method} defeat the {creature}? Explain in 1 sentence, 75 characters maximium.')
#             print(reasoning.text[:-2])

#     print(f'You died! Score: {difficulty - 1}')