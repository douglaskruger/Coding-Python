# Import the required libraries
import random

# Define a dictionary with responses
responses = {
    "hello": ["Hi!", "Hello!", "Hey!"],
    "how are you": ["I'm good, thanks for asking!", "I'm doing well, thank you!", "I'm great, thanks!"],
    "what is your name": ["My name is Bot", "I'm Bot", "You can call me Bot"],
    "exit": ["Goodbye!", "See you later!", "Bye!"]
}

# Function to generate a response
def generate_response(user_input):
    # Convert the user input to lowercase
    user_input = user_input.lower()

    # Check if the user input is in the responses dictionary
    if user_input in responses:
        # Return a random response from the list
        return random.choice(responses[user_input])
    else:
        # If the input is not recognized, return a default response
        return "Sorry, I didn't understand that."

# Main function
def main():
    print("Welcome to the chatbot!")

    while True:
        # Get the user input
        user_input = input("User: ")

        # Generate and print the response
        response = generate_response(user_input)
        print("Bot:", response)

        # Exit the loop if the user types 'exit'
        if user_input.lower() == "exit":
            break

# Run the main function
if __name__ == "__main__":
    main()
