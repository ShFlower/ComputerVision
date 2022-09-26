from array import array
import cv2
from keras.models import load_model
import numpy as np
import random
import time

class RockPaperScissors:

    def __init__(self, max_score, countdown):
        
        self.choices = ['Nothing' , 'Rock' ,'Paper' , 'Scissors']
        print(f"choices array equals : {self.choices}")

        self.no_of_choices = len(self.choices)
        print(f"no_of_choices = {self.no_of_choices}")

        self.max_score = max_score
        self.countdown = countdown
                      
        self.user_score = 0
        self.computer_score = 0
        self.no_tries = 0

        self.model = load_model('keras_model.h5')
        self.cap = cv2.VideoCapture(0)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
     

    # gets the user input from camera and returns a array showing the likelihood scores
    def get_user_input(self):
        user_choice = self.choices[random.randint(0,self.no_of_choices-1)]
        print(f" User chose: {user_choice}")
        return user_choice
       

    def get_computer_input(self):
        computer_choice = self.choices[random.randint(0,self.no_of_choices-1)]
        print(f" Computer chose: {computer_choice}")
        return computer_choice 

    def cleanup(self):
        # After the loop release the cap object
        self.cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        
def play_game():
    # initialise the game
    game = RockPaperScissors(max_score=3, countdown=3)

    #define all the game messages
    start_message = f"""
                {'*'*50} 
                Let's play Rock Paper Scissors!
                The first player to reach {game.max_score} points wins the game!! 
                {'*'*50}
             """

    countdown_message = f"""
                {'*'*50}  
                The game will read your sign in {game.countdown} seconds
                {'*'*50}
             """

    nodetect_message = f"""
                {'*'*75}  
                  The computer did not detect a clear choice from one/both users. 
                  Please try again.
                {'*'*75}
             """
    def print_won(usr_score,comp_score):
        won_message = f"""
                    {'*'*50}  
                    Congratulations you won !!!
                    You scored : {usr_score}  Computer scored : {comp_score}
                    {'*'*50}
                """
        print(won_message)

    def print_lost(usr_score,comp_score):
        lost_message = f"""
                {'*'*50}  
                    Unfortunately you lost !!!
                    Computer scored : {comp_score}   You scored : {usr_score}
                {'*'*50}
                """
        print(lost_message)

    #start the game
    print(start_message)
  
    while ((game.user_score <= game.max_score) and (game.computer_score <= game.max_score)):
        if((game.user_score == game.max_score) or (game.computer_score == game.max_score)):
            if game.user_score > game.computer_score:
                print_won(game.user_score, game.computer_score)
                game.cleanup()
                exit()
            else:
                print_lost(game.user_score, game.computer_score)
                game.cleanup()
                exit()
        else:
            print(countdown_message)
            game.no_tries += 1
            user_input = game.get_user_input()
            computer_input =game.get_computer_input()
            if ((user_input == 'Rock') and (computer_input == 'Scissors')):
                game.user_score  += 1
            elif ((user_input == 'Paper') and (computer_input == 'Rock')):
                game.user_score  += 1
            elif ((user_input == 'Scissors') and (computer_input == 'Paper')):
                game.user_score  += 1
            elif (user_input == 'Nothing' or computer_input == 'Nothing'):
                print(nodetect_message)
            elif (user_input == computer_input):
                print("We have a draw!! Have another go!")
            else: 
                game.computer_score += 1
               
        print(f" Loop no_tries: {game.no_tries}") 
        print(f" Loop Game user_score: {game.user_score}") 
        print(f" Loop Game computer_score: {game.computer_score}") 
    
    

if __name__ == '__main__':
   play_game()