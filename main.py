import tkinter
import customtkinter
import random
from PIL import ImageTk, Image
import string
from playsound import playsound


class Hangman:
    def __init__(self):

        # Defining the Main Window
        self.running = False
        self.img_label = None
        self.window = customtkinter.CTk()
        self.window.geometry("1000x600")
        self.window.configure(fg_color="#F0F0F1")
        self.window.resizable(width=True, height=True)
        self.window.title("Hang Man")

        # Variables
        self.alphabet = list(string.ascii_uppercase)
        self.Button_List_dic = {}
        self.secret_word = None
        self.secret_word_list = None
        self.image_path = ["0.jpg", "1.jpg", "2.jpg",
                           "3.jpg", "4.jpg", "5.jpg", "6.jpg",
                           "7.jpg", "8.jpg", "9.jpg", "10.jpg"]
        self.text = None
        self.used_letters = []
        self.chances = 0

        # Frame for keys
        self.Nframe = customtkinter.CTkFrame(master=self.window)
        # self.Nframe.configure(fg_color="transparent")
        self.Nframe.pack(padx=20, pady=20, side=customtkinter.BOTTOM)
        
        # btn for exit
        self.exit_btn = customtkinter.CTkButton(master=self.window,
                                                fg_color="black",
                                                text="Exit Game",
                                                font=("Product Sans Bold", 30),
                                                command=lambda: self.window.destroy(),
                                                corner_radius=10,
                                                )
        self.exit_btn.place(relx=0.025, rely=0.05)

        # btn for new game
        self.newGame_btn = customtkinter.CTkButton(master=self.window,
                                                   fg_color="black",
                                                   text="New Game",
                                                   font=("Product Sans Bold", 30),
                                                   command=lambda: self.new_game(),
                                                   corner_radius=10)
        self.newGame_btn.place(relx=0.025, rely=0.15)

        # label for chances
        self.chances_label = customtkinter.CTkLabel(master=self.window,
                                                    text_color="black",
                                                    text=f"Chances : {self.chances}",
                                                    font=("RoadRage", 40))
        # winner image
        self.ind = 0
        self.wframeCnt = Image.open('src/images/winner.gif').n_frames
        self.wframes = [tkinter.PhotoImage(file='src/images/winner.gif', format='gif -index %i' % i) for i in
                        range(self.wframeCnt)]

        # loser image
        self.lframeCnt = Image.open('src/images/loser.gif').n_frames
        self.lframes = [tkinter.PhotoImage(file='src/images/loser.gif', format='gif -index %i' % i) for i in
                        range(self.lframeCnt)]

        # secret label
        self.sw_label = customtkinter.CTkLabel(self.window,
                                               text_color="black",
                                               text="",
                                               anchor=tkinter.CENTER,
                                               font=('Product Sans Bold', 50))
        # Add image to main window
        self.update_image()

        # Calling the main function calls
        self.genarate_secret_word()
        self.generate_buttons()
        self.position_buttons()
        self.display_secret_word()

        self.window.mainloop()

    def genarate_secret_word(self):
        self.secret_word = random.choices((open("src/filtered_words.txt", "r")).readlines())[
            0].strip("\n").upper()
        self.secret_word_list = list(self.secret_word[:])
        print(self.secret_word)
        self.text = ["_" for letter in self.secret_word_list]

    def generate_buttons(self):
        for letter in self.alphabet:
            self.Button_List_dic[letter] = customtkinter.CTkButton(master=self.Nframe,
                                                                   width=10,
                                                                   height=40,
                                                                   fg_color="#00BFFF",
                                                                   corner_radius=50,
                                                                   text=letter,
                                                                   hover=True,
                                                                   hover_color="#1E90FF",
                                                                   font=('Product Sans Bold', 30),
                                                                   command=lambda x=letter: self.output(x))

    def position_buttons(self):
        r = 0
        c = 10
        count = 0
        # for letter_index in range(0, len(self.Button_List_dic)):
        for key in self.Button_List_dic.keys():
            if count % 13 == 0:
                r += 1
                c = 10
            self.Button_List_dic[key].grid(row=r, column=c, padx=5, pady=5)
            c += 1
            count += 1

    def clear_buttons(self):
        for widgets in self.Nframe.winfo_children():
            widgets.configure(fg_color="#00BFFF")

    def update_lable(self):
        for letter in self.used_letters:
            for letter_index in range(len(self.secret_word_list)):
                if letter == self.secret_word_list[letter_index]:
                    self.text[letter_index] = letter

    def display_secret_word(self):
        empty_string = ""
        for element in self.text:
            empty_string += f" {element}"
      
        self.sw_label.configure(text=empty_string)
        self.sw_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.7)
        self.chances_label.place(anchor=tkinter.CENTER, relx=0.8, rely=0.1)

    def output(self, y):
        if y not in self.used_letters:
            if y in self.secret_word_list:
                self.Button_List_dic[y].configure(fg_color="#2ECC71", hover=False)
                playsound("src/music/mixkit-correct-answer-tone-2870-[AudioTrimmer.com].wav")
            else:
                self.Button_List_dic[y].configure(fg_color="#F50C0C", hover=False)
                playsound("src/music/mixkit-game-show-wrong-answer-buzz-950-[AudioTrimmer.com].wav")
            self.used_letters.append(y)
            self.chances += 1
            self.chances_label.configure(text=f"Chances : {self.chances}")
        if self.chances < 6:
            self.update_image()
            self.update_lable()
            self.display_secret_word()
        else:
            self.chances_over()
        self.check_winner()

    def check_winner(self):
        if self.text == self.secret_word_list:
            self.sw_label.configure(text=" YOU WON !", font=("RoadRage", 40))
            self.winner_label = tkinter.Label()
            self.winner_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)
            self.running = True
            self.win_window()

    def chances_over(self):
        self.loser_label = tkinter.Label()
        self.loser_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)
        self.running = True
        self.lose_window()

    def new_game(self):
        self.running = False
        self.img_label.place_forget()
        self.clear_buttons()
        self.chances = 0
        self.chances_label.configure(text=f"Chances : {self.chances}")
        self.used_letters = []
        self.update_image()
        self.genarate_secret_word()
        self.display_secret_word()

    def update_image(self):
        path = f"src/images/hangman{self.chances}.png"
        img_ = Image.open(path).resize((251, 260))
        self.img = ImageTk.PhotoImage(img_)

        self.img_label = tkinter.Label(self.window, image=self.img)
        self.img_label.place(anchor=tkinter.CENTER, relx=0.5, rely=0.4)

    def win_window(self):
        if self.running:
            wframe = self.wframes[self.ind]
            self.ind += 1
            if self.ind == self.wframeCnt:
                self.ind = 0
            self.img_label.configure(image=wframe)
            self.window.after(100, self.win_window)

    def lose_window(self):
        if self.running:
            lframe = self.lframes[self.ind]
            self.ind += 1
            if self.ind == self.lframeCnt:
                self.ind = 0
            self.img_label.configure(image=lframe)
            self.window.after(100, self.lose_window)


if __name__ == "__main__":
    App = Hangman()
