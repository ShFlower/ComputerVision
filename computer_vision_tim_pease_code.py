import cv2
from keras.models import load_model
import numpy as np
import random
import time
​
def get_prediction(prediction):
    predicted_index = np.argmax(prediction)
    choices = ["Rock", "Paper", "Scissors", "Nothing"]
    return choices[predicted_index]
​
class RPS:
​
    def __init__(self):
        self.user_wins = 0
        self.computer_wins = 0
​
    def get_computer_choice(self):
        computer_choice = random.choice(["Rock", "Paper", "Scissors"])
        return computer_choice
​
    def get_user_choice(self):
​
        model = load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
​
        total_duration = 6
        time_passed = 0
        start_time = time.time()
​
        while True: 
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            cv2.imshow('frame', frame)
            # Press p to close the window and input the answer on camera
            if cv2.waitKey(1) & 0xFF == ord('p'):
                break
            if time.time() - start_time >= time_passed:
                time_passed += 1
                print(total_duration - time_passed)
            if time_passed == total_duration:
                break
                    
        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
​
        return get_prediction(prediction)
​
    def get_winner(self,computer_choice, user_choice):
        if computer_choice == user_choice:
            self.winner = "Noone"
        elif [computer_choice, user_choice] in [["Rock", "Paper"], ["Paper", "Scissors"], ["Scissors", "Rock"]]:
            self.winner = "User"
            self.user_wins += 1
        else: 
            self.winner = "Computer"
            self.computer_wins += 1
        return self.winner
​
def play(winning_score = 3):
    game = RPS()
    while True:
        computer_choice = game.get_computer_choice()
        user_choice = game.get_user_choice()
        game.get_winner(computer_choice, user_choice)
        print(f"You chose {user_choice}")
        print(f"The computer chose: {computer_choice}")
        print(f"{game.winner} won this round")
        print(f"The score is {game.user_wins} - {game.computer_wins} to you!")
        if game.user_wins == winning_score:
            print(f"User wins the best of {2 * winning_score - 1} match!")
            break
        elif game.computer_wins == winning_score:
            print(f"Computer wins the best of {2 * winning_score - 1} match!")
            break
        input("Press enter to continue...")
​
if __name__ == '__main__':
    play()