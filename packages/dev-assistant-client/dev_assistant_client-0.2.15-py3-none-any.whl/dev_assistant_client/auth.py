from colorama import Fore, Style
import getpass
from dev_assistant_client.config import api_client
from dev_assistant_client.utils import delete_token, save_token
import webbrowser

class Auth:
    """
    The Auth class handles authentication operations, including logging in,
    logging out, and establishing a WebSocket connection with Ably.
    """
    
    def login(self):
        """
        Prompts the user for authentication method: email/password or OAuth.
        """
        print("Choose authentication method:")
        print("1. Email and Password")
        print("2. OAuth via GitHub")
        choice = input("Enter your choice (1/2): ")
        if choice == '1':
            self.login_email_password()
        elif choice == '2':
            self.login_oauth()
        else:
            print(Fore.LIGHTRED_EX + "Invalid choice." + Style.RESET_ALL)

    def login_email_password(self):
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        data = {"email": email, "password": password}
     
        response = api_client.post("/api/login", data=data)
        
        if response.status_code in [200, 201, 202, 204]:
            token = response.json()["token"]
            save_token(token)
            return True
        else:
            print(Fore.LIGHTRED_EX + "Login failed. Please check your credentials and try again." + Style.RESET_ALL)
            return False

    def login_oauth(self):
        print("Opening GitHub login page...")
        webbrowser.open('https://devassistant.tonet.dev/github/login')
        token = input("Enter the token received after successful login: ")
        save_token(token)
        print(Fore.LIGHTGREEN_EX + "Login successful." + Style.RESET_ALL)

    def logout(self):
        """
        Logs out the user by deleting the locally stored token.
        """
        try:
            delete_token()
            print("Logged out successfully.")
        except FileNotFoundError:
            print("You aren't logged in.")