# Twitter Mass Blocker

⚠️ This script no longer works since twitter hide the likes ⚠️

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).

### Installing

1. Clone the repository
```bash
git clone https://github.com/M-Bahy/twitter-mass-blocker.git
```
2. Install the required packages
```bash
pip install -r requirements.txt
```
## Renaming and Configuring Environment Variables

1. Rename the `.env.example` file to `.env`.
2. Open the `.env` file and fill in your details.

## Running the Script

To run the script, copy the links to the tweets you want to block their author and his followers in targets.txt then simply double click on the `run.bat` file 

## Limitations and Notes ⚠️

- You have  to disable two-factor authentication on your Twitter account to be able to run the script.
- The script is only tested on windows.
- The script will not block private accounts.
- The script will not block accounts that have blocked you.
- Since the script is running on top of the browser version of Twitter, it usually loads 40 followers only.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute to this project by creating a pull request or submitting an issue.
