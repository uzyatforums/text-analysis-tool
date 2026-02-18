def welcomeUser():
    print("Welcome to the text analysis tool. I will mine and analyse a body of text from a file you give me")


def getusername():
    username = input("Enter your username: ")
    return username

welcomeUser()
username = getusername()
print(f"Welcome, {username}!")


