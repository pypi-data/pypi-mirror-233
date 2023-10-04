import os
from colorama import Fore, Style
from dev_assistant_client.config import api_client
from dev_assistant_client.utils import save_token, delete_token
import webbrowser

class Auth:
    """
    The Auth class handles authentication operations, including logging in,
    logging out, and establishing a WebSocket connection with Ably.
    """
    
    def login(self):
        """
        Prompts the user for authentication method: email/password or OAuth.
        Iterates 3 times, then exits if all attempts fail.
        """
        print("\nOpening login page in browser...")
        if os.environ.get('ENV') == 'production':
            webbrowser.open('https://devassistant.tonet.dev/login?client_type=cli')
        else:
            url = os.environ.get('APP_URL') or 'https://dev-assistant-server.test'
            webbrowser.open(url + '/login?client_type=cli')
        token = input("Enter the token received after successful login: ")
        if token:
            save_token(token)
            print(Fore.LIGHTGREEN_EX + "Login successful." + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + "Login failed. Please check your credentials and try again." + Style.RESET_ALL)

    def logout(self):
        """
        Logs out the user by deleting the locally stored token.
        """
        try:
            delete_token()
            print("Logged out successfully.")
        except FileNotFoundError:
            print("You aren't logged in.")