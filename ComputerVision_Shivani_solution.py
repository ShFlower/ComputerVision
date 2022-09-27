from array import array
import cv2
from keras.models import load_model
import numpy as np
import random
import time

class RockPaperScissors:

    def __init__(self, max_score, countdown):
        
        self.choices = ['Nothing' , 'Rock' ,'Paper' , 'Scissors']
    
        self.no_of_choices = len(self.choices)
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
                
        ###for countdown seconds delay 
        close_time=time.time() + self.countdown
        
        while close_time > time.time():
            ret, frame = self.cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            self.data[0] = normalized_image
            prediction = self.model.predict(self.data)
            cv2.imshow('frame', frame)
            print(f"Prediction: {prediction}")
            user_choice = self.choices[prediction.argmax(axis=1)[0]]
        
        return user_choice
       

    def get_computer_input(self):
        #computer choice can never be 'Nothing'
        computer_choice = random.choice(self.choices[1:self.no_of_choices-1])
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
                    The camera will read your choice in {game.countdown} seconds
                {'*'*50}
             """

    nodetect_message = f"""
                {'*'*50}  
                    No input detected from one/both users. 
                            Please try again.
                {'*'*50}
             """
    draw_message = f"""
                    {'*'*50} 
                        We have a draw!! Have another go!
                    {'*'*50}
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
         #if either player has scored 3 points
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
            if [user_input, computer_input] in [["Paper","Rock"], ["Scissors","Paper"], ["Rock","Scissors"]]:
                game.user_score  += 1
            elif (user_input == 'Nothing' or computer_input == 'Nothing'):
                print(nodetect_message)
            elif (user_input == computer_input):
                print(draw_message)
            else: 
                game.computer_score += 1
        print(f"User Choice:   {user_input}     Computer Choice:   {computer_input}")       
        print(f"User Score :     {game.user_score}       Computer Score:      {game.computer_score}     of {game.no_tries} tries ") 
   

if __name__ == '__main__':
    play_game()