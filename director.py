import ai
import state as State
import application

class Director():
    def __init__(self):
        self.difficulty = 1
        self.state = State.GET_KEY


        # game stuff
        self.max_words = 15
        self.max_characters = 50
    

    # Entry submission
    def submission(self, text: str):
        # Edge case: defeat, restart game
        if (self.state == State.DEFEAT):
            self.restart()
            self.generate_creature()
            self.state = State.CREATURE
            return

        ## Edge case: text is empty
        if (not text or text.isspace()):
            return

        # Edge case: max words/characters reached
        if (len(text.split()) > self.max_words or len(text) > self.max_characters):
            return

        match self.state:
            case State.GET_KEY:
                # Generate ai
                if (self.create_ai(text)):
                    # Switch states and create creature
                    self.generate_creature()
                    self.state = State.CREATURE
                else:
                    pass

            case State.CREATURE:
                # Get outcome
                outcome = self.determination(text)

                if (not outcome):
                    self.state = State.DEFEAT
            
        # Clear entry
        self.application.clear_entry()

    # Run to rest all vars into its __init__ vals
    def restart(self):
        self.difficulty = 1
        self.max_words = 15
        self.max_characters = 50


    # Updates everytime a key is pressed inside the application.entry
    def update(self, text = ""):
        # Edge case: wrong state
        if (self.state == State.GET_KEY):
            return

        # Update word count label and color
        self.application.set_word_count_label("Words: " + str(len(text.split())) + "/" + str(self.max_words))
        if (len(text.split()) > self.max_words):
            self.application.set_word_count_label_color("Red")
        else:
            self.application.set_word_count_label_color("White")

        # Update character count label
        self.application.set_character_count_label("Characters: " + str(len(text)) + "/" + str(self.max_characters))
        if (len(text) > self.max_characters):
            self.application.set_character_count_label_color("Red")
        else:
            self.application.set_character_count_label_color("White")

    def create_ai(self, api_key: str):
        try:
            self.ai = ai.AI(api_key)
            self.ai.generate_chat()
        except:
            self.application.set_main_label("Invalid Google Gemini Key. Please try again.")
            return False
        return True

    def generate_creature(self):
        self.creature = self.ai.generate_creature(self.difficulty)

        # Display to application
        self.application.set_main_label("You encounter a(n) " + self.creature + "!")
    
    def determination(self, entry: str):
        outcome = self.ai.determination_of_prompt(self.creature, entry)

        # Success: display next creature
        if (outcome):
            self.difficulty += 1
            self.creature = self.ai.generate_creature(self.difficulty)
            self.application.set_main_label("You encounter a(n) " + self.creature + "!")
        # Failure: display reason of failure
        else:
            reasoning = self.ai.get_reasoning_of_failure(self.creature, entry).text[:-2]
            self.application.set_main_label(reasoning + "\nHit <Return> to restart")
        
        return outcome
