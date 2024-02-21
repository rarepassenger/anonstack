# Anon.Stack: A P2P Trade Assistant

Anon.Stack is a peer-to-peer (P2P) trade assistant. It's designed to help with streamlining P2P bitcoin trades by providing:

- Real-time prices and markup rates
- Fee estimates and...
- Transaction deals 

## Features

- Real-time BTC Price: Gets the current bitcoin price from CoinMarketCap API.
- Markup Calculator: Let's users input markup percentages for total cost. 
- Fee Estimator: Estimates transaction fees based on confirmation block time.
- Transaction Receipt: Generates a detailed receipt.
- User-friendly Interface: Simple command-line interface for easy use.

## Usage

Clone the repository to your local drive.
Ensure you have Python 3 installed.
Install the required dependencies using `pip install -r requirements.txt`.
Run the script using `python anonstack.py`.
Follow the on-screen prompts.

## Dependencies

- `requests`: For making HTTP requests to APIs.
- `locale`: For formatting currency values.
- `datetime`: For handling date and time operations.

## Setup

To use the CoinMarketCap API, you need an API Key. Set it as an environment variable named 'COINMARKETCAP_API_KEY'.

## Contributions

Contributions are welcome! If you encounter any bugs or have ideas for improvements, feel free to open an issue or submit a pull request.

# License

This project is licensed under the [MIT License](https://mit-license.org/).

## Author

- rare passenger
- @rarepassenger
- PGP Fingerprint: 07D4 0C14 C00A 61AA A313  50CC 7BB3 E2E1 396D 0C97
