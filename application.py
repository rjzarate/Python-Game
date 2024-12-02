from tkinter import *
import state as State
import director

class Application(Frame):

    def __init__(self):
        # Create main window
        self.root = Tk()
        self.root.wm_title("AI Battles")
        self.root.geometry("500x500")
        Frame.__init__(self, self.root)
        self.pack(fill="both", expand=True)

        self.data = {"A": range(7, 27)}

        # Main Text
        self.main_label = Label(text="Insert Google Gemini API Key", fg="White", font=("Helvetica", 18))
        self.main_label.place(relx=0.5,rely=0.2, anchor=CENTER)

        # Word Count Text
        self.word_count_label = Label(text="Words: NA", fg="White", font=("Helvetica", 15), justify=LEFT)
        self.word_count_label.place(relx=0.2,rely=0.97, anchor=CENTER)

        # Character Count Text
        self.character_count_label = Label(text="Characters: NA", fg="White", font=("Helvetica", 15), justify=LEFT)
        self.character_count_label.place(relx=0.7,rely=0.97, anchor=CENTER)

        # Entry
        self.entry = Entry(font=("Courier New", 15))
        self.entry.place(relx=0.5, rely=0.87, relwidth=0.9, relheight=0.1, anchor=CENTER)
        self.is_entry_focus = True
        self.entry.bind('<FocusIn>', lambda _ : globals().__setitem__('is_entry_focus', True))
        self.entry.bind('<FocusOut>', lambda _ : globals().__setitem__('is_entry_focus', False))

        # Return (Enter key event)
        self.root.bind('<Return>', self.on_return)

        # Any Key pressed
        self.root.bind('<Key>', self.on_key_pressed)

        # Application is resized
        self.root.bind("<Configure>", self.on_configure)

        # Application state
        self.state = State.GET_KEY

        # Create director (LOGIC)
        self.director = director.Director()
        self.director.application = self

        # Run recursive function
        self.update()

    # Start main loop (i.e. application)
    def start(self):
        self.root.mainloop()
    
    def on_return(self, _):
        print('enter key hit')

        if (self.is_entry_focus):
            self.director.submission(self.entry.get())
            self.director.update()
    
    def on_key_pressed(self, _):
        if (self.is_entry_focus):
            self.director.update(self.entry.get())

    def on_configure(self, _):
        # Wrap main label based on width of application
        self.main_label.configure(wraplength=self.root.winfo_width())
            
    
    def set_main_label(self, text):
        self.main_label.configure(text=text)
    
    def set_word_count_label(self, text):
        self.word_count_label.configure(text=text)
    def set_word_count_label_color(self, color):
        self.word_count_label.configure(fg=color)

    def set_character_count_label(self, text):
        self.character_count_label.configure(text=text) 
    def set_character_count_label_color(self, color):
        self.character_count_label.configure(fg=color)

    def clear_entry(self):
        self.entry.delete(0, 'end')
        
    def update(self):

        # Recursive call (1000ms)
        self.after(1000, self.update)