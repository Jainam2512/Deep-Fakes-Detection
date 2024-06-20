import csv
import os
import random
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

def welcome_message():
    print("Welcome to AI Math Practice Tutor!")

def sign_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # Check if username and password match from stored data
    with open("/content/drive/MyDrive/student_data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                print("Sign in successful!")
                return True
    print("Invalid username or password. Please try again.")
    return False

def sign_up():
    fullname = input("Enter your full name: ")
    username = input("Choose a username: ")
    email = input("Enter your email address: ")
    password = input("Choose a password: ")
    # Save the new user data to a CSV file
    with open("/content/drive/MyDrive/student_data.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, fullname, email, password])
    print("Sign up successful! You can now sign in.")

def generate_test(level):
    test_questions = []
    with open(f"/content/drive/MyDrive/algebra_{level}_questions.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            test_questions.append(row)
    random.shuffle(test_questions)
    return test_questions[:10]  # Selecting 10 random questions for the test

def take_test(questions,level):
    score = 0
    times = []
    print("Take the test:")
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question[0]}")
        print("Options:")
        shuf=[]
        for j, option in enumerate(question[2:], 1):
            shuf.append(option)
        random.shuffle(shuf)
        for j, option in enumerate(shuf[:], 1):
            print(f"{j}. {option}")
        start_time = time.time()
        answer = int(input("Enter your answer (1/2/3/4): "))
        end_time = time.time()
        if 0<answer<5:
          times.append((end_time - start_time)/60)
          if shuf[answer-1] == question[1]:
            score += 1
        else:
          print("invalid option")
          i-=1
    print(f"Your score is {score}/10")
    result=pass_fail(times,score,level)
    return result

def create_model():
      model = Sequential()
      model.add(LSTM(64, return_sequences=True, input_shape=(None, 4)))  # Input for (score, time, num_tests, total_questions)
      model.add(LSTM(32))
      model.add(Dense(2, activation='softmax'))  # Softmax for probability distribution (pass/fail)
      model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
      # Replace with your actual training data (scores, times, labels)
      # ... training code here ...
      return model

def predict_next_level(model, student_data_new):
      # Reshape new data for prediction with batch size 1
      data_reshaped = np.array([student_data_new])[:, np.newaxis, :]
      # Predict probabilities for pass/fail classes
      predictions = model.predict(data_reshaped)[0]
      # Return the class with higher probability (pass/fail)
      return "pass" if predictions[1] > predictions[0] else "fail"

def pass_fail(times,score,level):
      scores=[]
      times=[]
      sc = score * 100  # Calculate score for each test
      scores.append(sc)
      t = sum(times)
      times.append(t)
      total_questions = 10
  #     return total_questions, score, scores, times
  # def main():
  #     total_questions, num_correct_answers, scores, times = get_user_input(times,score)
      student_data_new = []
      for score, t in zip(scores, times):
          # Check if score is above 70% and time is between 10 to 20 minutes
          if score >= 70 and 8 <= t <= 20 and level=="beginner":
              student_data_new.append([score, t, len(scores), total_questions])
          elif score >= 70 and 10 <= t <= 30 and level=="intermediate":
              student_data_new.append([score, t, len(scores), total_questions])
          elif score >= 70 and  12 <= t <=45  and level=="advanced":
              student_data_new.append([score, t, len(scores), total_questions])
          else:
              pass

      if not student_data_new:
          x="failed"
          return x

      # Load the pre-trained model (replace with your training logic)
      model = create_model()

      for data in student_data_new:
          prediction = predict_next_level(model, data)
          print(f"Student with {data[0]}% score and {data[1]} minutes is predicted to {'pass' if prediction == 'pass' else 'fail'} next level.")
          x="pass"
          return x

def select_chapter():
    print("Which chapter do you want to practice?")
    print("1. Algebra")
    print("2. Calculus")
    print("3. Geometry")
    choice = input("Enter the number corresponding to your choice: ")
    if choice == "1":
        print("Starting Algebra practice...")
        start_practice("algebra")
    elif choice == "2":
        print("Starting Calculus practice...")
        start_practice("calculas")
    elif choice == "3":
        print("Starting Geometry practice...")
        start_practice("geometry")
    else:
        print("Invalid choice. Please try again.")

def generate_practice(level):
    practice_questions = []
    with open(f"/content/drive/MyDrive/algebra_{level}_questions.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            practice_questions.append(row)
    random.shuffle(practice_questions)
    questions = practice_questions[:15]
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question[0]}")
        print("Options:")
        shuf=[]
        for j, option in enumerate(question[2:], 1):
            shuf.append(option)
        random.shuffle(shuf)
        for j, option in enumerate(shuf[:], 1):
            print(f"{j}. {option}")
        answer = int(input("Enter your answer (1/2/3/4): "))
        if 0<answer<5:
          if shuf[answer-1] == question[1]:
            print("correct!")
          else:
            print("incorrect!")
            print(f"correct answer is {question[1]}.")
        else:
          print("invalid option")
          i-=1
    print("you have completed practicing 15 questions. do you want to take test?")
    x=input("yes/no: ").lower()
    if x=="yes":
      repo=take_test(generate_test(level),level)
      if repo=="pass":
        print("congratulations! you have passed the test.\nyou can now move to next level")
        if level=="beginner":
          print("you are promoted to intermediate level...\nlets practice questions.")
          level=="intermediate"
          generate_practice(level)
        elif level=="intermediate":
          print("you are promoted to advanced level...\nlets practice questions.")
          level=="advanced"
          generate_practice(level)
        elif level=="advanced":
          print("you have mastered the chapter.")
        else:
          pass
      else:
        print("you aren't ready yet, you need to practice more")
        r=input("do you want to practice again? (y/n): ").lower()
        if r=="y":
          generate_practice(level)
        elif r=="n":
          pass
        else:
          print("invalid option.")
    elif x=="no":
      y=input("do you want to practice more? (y/n): ").lower()
      if y=="y":
        generate_practice(level)
    else:
      pass

def start_practice(chapter):
    print(f"You have selected {chapter} practice.")
    level = input("Select the level of difficulty (beginner/intermediate/advanced): ").lower()
    if level == "beginner":
        print(f"Starting {level} {chapter} practice...")
        generate_practice(level)
    elif level == "intermediate":
        print(f"You have selected {level} level. You need to take a test first.")
        test_questions = generate_test("beginner")
        report=take_test(test_questions,level)
        if report=="pass":
          print(f"Now starting {level} {chapter} practice...")
          generate_practice(level)
        else:
          print("you have failed the test, you have to practice the beginner level first")
          level="beginner"
          generate_practice(level)
    elif level == "advanced":
        print(f"You have selected {level} level. You need to take a test first.")
        test_questions = generate_test("intermediate")
        report=take_test(test_questions,level)
        if report=="pass":
          print(f"Now starting {level} {chapter} practice...")
          generate_practice(level)
        else:
          print("you have failed the test, you have to practice the intermediate level first")
          level="intermediate"
          generate_practice(level)
    else:
        print("Invalid level selection. Please try again.")

def main():
    welcome_message()
    while True:
        action = input("Do you want to sign in or sign up? (Enter 'signin' or 'signup'): ").lower()
        if action == "signin":
            if sign_in():
                break
        elif action == "signup":
            sign_up()
        else:
            print("Invalid choice. Please try again.")

    select_chapter()

if __name__ == "__main__":
    main()
