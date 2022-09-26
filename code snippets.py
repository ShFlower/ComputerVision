 ###for countdown seconds delay 
        close_time=time.time() + self.countdown
        #print(f"Close time : {close_time}")
        while time.time() <= close_time:
            if time.time() > close_time:
                break
            else:
                ret, frame = self.cap.read()
                resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
                image_np = np.array(resized_frame)
                normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
                self.data[0] = normalized_image
                prediction = self.model.predict(self.data)
                cv2.imshow('frame', frame)
                print(f"Prediction: {prediction}")
                #user_choice = self.choices.index(max(prediction))
                choice_pos = prediction.argmax(axis=1)
                print(f"choice_pos: {choice_pos}")
                user_choice = self.choices[choice_pos[0]]
                print(f"User choice: {user_choice}")
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break