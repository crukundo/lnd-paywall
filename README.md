# Paywalled
Paywalled is an open blogging platform that enables writers to monetize their content with micropayments enabled by the lightning network. Spend a few sats to publish, view, edit and comment on content. Have fun with lightning. Inspired by Alex Bosworth's [Y'alls](https://yalls.org)

![Paywalled](https://github.com/crukundo/lnd-paywall/blob/main/paywalled.png?raw=true)

## A few things
This application uses ordinary user accounts for anyone who wants to publish their content. User accounts allow the platform keep track of all due earnings and make it easy to claim them when required. It also makes edits to content much easier for the user.

You should have [Lnd](https://github.com/lightningnetwork/lnd/) and [bitcoind](https://github.com/bitcoin/bitcoin) setup already. Plus, for testing, I used regtest. It was quicker to setup and focus on building that way but you can use whatever chain you want. More on this in the Configuration section.

I also wrote a blog about this, you can read [here](https://rukundo.mataroa.blog/blog/i-built-a-blogging-platform-powered-by-the-lightning-network/)

## Setup
Create a virtual environment, clone this repo and install dependencies
```
% virtualenv venv
% source venv/bin/activate
% git clone https://github.com/crukundo/lnd-paywall.git
% cd lnd-paywall
% pip install -r requirements.txt
```

## Database
This project uses sqlite3. Feel free to use whatever engine you want and reference it in your `.env` and settings.py

## Configuration

Once all the dependencies have been installed, you can then create a `.env` file in the root of the project that contains all the configuration parameters for your instance. I added a sample file you can update. Remember to rename as `.env` and add to `.gitignore`

The following are a list of currently available configuration options and a 
short explanation of what each does.

`LND_FOLDER` (required)
This is the path to your lnd folder. There should be read access to this path

`LND_MACAROON_FILE` (required)
This is the path to your admin.macaroon file. This will vary depending on the network chain you decide on. There should be read access to this path

`LND_TLS_CERT_FILE` (required)
This is the path to your tls.cert file. This is usually located inside your $LND_FOLDER. There should be read access to this path

Other configs you can change if you want (but remember to update the values from settings when you call your rpc client):

`LND_NETWORK` (optional; defaults to *regtest*)
This selects the network that your node is configured for. regtest is the default and will have you on your way in no time

`LND_GRPC_HOST` (optional; defaults to *localhost*)
If your node is not on your local machine (say on a different server), you'll 
need to change this value to the appropriate value.

`LND_GRPC_PORT` (optional; defaults to *10009*)
If the GRPC port for your node was changed to anything other than the default 
you'll need to update this as well.

`MIN_VIEW_AMOUNT` = 1500 (number of satoshis to pay to view an article)

`MIN_PUBLISH_AMOUNT` = 2100 (number of satoshis to pay to publish an article)

`PUBLISH_INVOICE_EXPIRY` = 604800 (time until a created lightning invoice to publish an article expires)

`VIEW_INVOICE_EXPIRY` = 10800 (time until a created lightning invoice to view an article expires)


## Initializing the database

To initialize the database which would create the database file and all the 
necessary tables, run the command:

```
% ./manage.py migrate
```

## Running the application server

Start the application backend by running the command:

```
% ./manage.py runserver
```

## Pending matters

- Add comment section
- Make writers pay to edit their posts 😈
- Add a section for writers with content to claim their rewards and facilitating channel opening to their lnd node through their shared public key
- Possibly add [LNURL-auth](https://github.com/fiatjaf/lnurl-rfc/blob/legacy/lnurl-auth.md) and replace the ordinary user accounts authentication system

## Special Credit
- Will Clark's [lnd-grpc](https://github.com/willcl-ark/lnd_grpc) - a python3 gRPC client for LND that did some heavy lifting. 
- The incredible supportive team at [Qala](https://qala.dev)