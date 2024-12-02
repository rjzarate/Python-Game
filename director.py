import ai
import random
import string
import state as State
import application

class Director():    
    def __init__(self):
        self.state = State.GET_KEY

        # game stuff
        self.restart()

    # Run to rest all vars into its __init__ vals
    def restart(self):
        self.difficulty = 1
        self.max_words = 10
        self.max_characters = 30
        self.score = 0
        self.words_used = {}

    
    def update(self):
        # Make success label spin
        if (self.state == State.CREATURE):
            get_used_words_count = self.get_used_words(self.application.get_entry())
            if (get_used_words_count):
                self.application.set_success_rate_label_color("Red")
                self.application.set_success_rate_label("Success Rate: " + str(random.randint(0, 99)).zfill(2) + "% -" + str(get_used_words_count) + "%")
            else:
                self.application.set_success_rate_label_color("White")
                self.application.set_success_rate_label("Success Rate: " + str(random.randint(0, 99)).zfill(2) + "%")
    

    # Entry submission
    def submission(self, text: str):
        self.application.set_success_rate_label_color("White")

        match (self.state):
            case State.LOSE:
                self.restart()
                self.generate_creature()

                self.state = State.CREATURE
                return

            case State.WIN:
                self.application.set_main_label("You encounter a(n) " + self.creature + "!")
            
                self.state = State.CREATURE
                return


        ## Edge case: text is empty
        if (not text or text.isspace()):
            return

        # Edge case: max words/characters reached
        if (self.state != State.GET_KEY and (len(text.split()) > self.max_words or len(text) > self.max_characters)):
            return

        match self.state:
            case State.GET_KEY:
                # Generate ai
                if (self.create_ai(text)):
                    self.application.show_entry()
                    # Switch states and create creature
                    self.generate_creature()
                    self.state = State.CREATURE
                else:
                    pass

            case State.CREATURE:
                # Get outcome
                outcome = self.determination(text)

                if (outcome):
                    self.score += 100 * (self.difficulty / 2.0)
                    self.state = State.WIN


                if (not outcome):
                    self.state = State.LOSE
            
        # Clear entry
        self.application.clear_entry()


    # Updates everytime a key is pressed inside the application.entry
    def on_key_pressed(self, text = ""):
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

    def get_used_words(self, entry: str):
        count = 0
        
        # Go through each word, store in the table, or reduce outcome score
        for s in entry.translate(str.maketrans('', '', string.punctuation)).lower().split():
            if (s in self.words_used):
                count += self.words_used[s]
        
        return count

    
    def determination(self, entry: str):
        # Gives a values from 0% to 100% of the success rate
        outcome = self.ai.determination_of_prompt(self.creature, entry)

        # Go through each word, store in the table, or reduce outcome score
        for s in entry.translate(str.maketrans('', '', string.punctuation)).lower().split():
            if (s in self.words_used):
                outcome -= self.words_used[s]
                self.words_used[s] += 1
            else:
                self.words_used[s] = 1
        
        requiredOutcome = random.randint(0, 20) * 5
        self.application.set_success_rate_label("Success Rate: " + str(outcome).zfill(2) + "% | " + str(requiredOutcome).zfill(2) + "% Needed")


        # Success: display next creature
        if (outcome >= requiredOutcome):
            self.application.set_main_label(f"You defeated the {self.creature}!\nHit <Return> to continue")

            # Pre generate the next creature
            self.difficulty += 1
            self.creature = self.ai.generate_creature(self.difficulty)
            self.application.set_success_rate_label_color("Lime")

            
        # Failure: display reason of failure
        else:
            reasoning = self.ai.get_reasoning_of_failure(self.creature, entry).text[:-2]
            self.application.set_main_label("You died!\n" + reasoning + "\nHit <Return> to restart\n\nScore: " + str(self.score))
            self.application.set_success_rate_label_color("Red")
        
        return outcome >= requiredOutcome
