# tg-confession-bot


# Telegram Confession Bot

A Python Telegram bot that lets users submit anonymous confessions, which are forwarded to a designated Telegram channel. The bot also includes features like displaying a confession count and handling administrative commands.

## Features

- Allows users to submit confessions anonymously.
- Forwards confessions to a specified Telegram channel.
- Displays a link to the confession for user reference.
- Tracks and numbers each confession automatically.
- Includes admin-only commands for managing users and messages.

## Setup and Installation

### Prerequisites

- Python 3.7 or later
- A Telegram bot token (you can get this from [BotFather](https://core.telegram.org/bots#botfather) on Telegram)
- (Optional) [dotenv](https://pypi.org/project/python-dotenv/) for handling environment variables

### Installation

**Clone the repository**:
   ```bash
   git clone git@github.com:OscillatingBlock/tg-confession-bot.git
   cd tg-confession-bot
   ```
Install dependencies: Ensure you have all necessary libraries installed. You can do this with:

```bash
pip install -r requirements.txt
```
Set up environment variables: Create a .env file in the project root directory and add your bot token and channel ID:

```plaintext
BOT_TOKEN=your_telegram_bot_token
CHANNEL_ID=@your_channel_id
```
Run the bot:

```bash
python py_bot.py
```

## Commands and Usage
| Command              | Description                                      | Notes                       |
|----------------------|--------------------------------------------------|-----------------------------|
| /confess             | Submit a confession to the designated channel    | Sends the confession anonymously |
| /start               | Start interaction with the bot                   | Greets the user             |
| /chat_id             | Provides the current chat ID                     | Useful for admin setup      |
| /ban                 | Bans a user from the chat                        | Admin only                  |
| /unban               | Unbans a previously banned user                  | Admin only                  |
| /kick                | Kicks a user from the chat                       | Admin only                  |
| /timer               | Sets a simple timer                              | Demo feature                |
| /create_invite_link  | Creates a new invite link for the group          | Admin only                  |
| /spurge              | Deletes multiple messages in a chat              | Admin only                  |


## Project Structure
py_bot.py: Main script that starts the bot and loads handlers.
handlers.py: Contains all the command and message handlers for different bot functionalities.
.gitignore: Ignores unnecessary files in Git.
requirements.txt: Lists all dependencies for the project.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you find any bugs or have ideas for improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.






