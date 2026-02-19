from random_username.generate import generate_username

def welcomeUser():
    # Print message prompting user  to input their name
    print("Welcome to the text analysis tool. I will mine and analyse a body of text from a file you give me")


def getusername():
    usernameFromInput = input("\nTo begin, please enter your username:\n")

    usernameLessThan5Chars = len(usernameFromInput) < 5

    print("Less than 5 characters: " + str(usernameLessThan5Chars))


    if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
        print("Your username must be at least 5 characters long, alphanumeric only (a-z/A-Z/0-9), have no spaces, and cannot start with a number")
        print("Assigning username instead...")
        usernameFromInput = generate_username()[0]

    return usernameFromInput

def greetUser(username):
    print(f"Welcome, {username}!")

welcomeUser()
username = getusername()
greetUser(username)






