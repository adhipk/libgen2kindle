# libgen2kindle
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

----
A python flask+HTMX app to search for books on [Libgen](libgen.is) and send them to your Kindle via email.
Demo app at: [libgen2kindle.vercel.app](https://libgen2kindle.vercel.app), (This site is linked to my kindle, feel free to send me good books lol.)

## Requirements

* Python 3

## Installation and Setup

1. Clone this repo
2. Install the requirements.txt file
 ```bash
 pip install -r requirements.txt
 ```
3. Copy `.env.example` into a new `.env` file
4. Replace the following env vars in `.env` file
    1.  `RECIEVER_EMAIL`: This is your send-to-kindle email. [See guide to set this up.](https://www.amazon.com/sendtokindle/email)
    2. `SENDER_EMAIL`: Your personal email which you will use to send books from. You will also need to add this email as an approved sender in your amazon account.(see guide from previous step)
    3. `EMAIL_PASSWORD`: Password to `SENDER_EMAIL` account. If you are using Gmail, you will have to setup an app password. [See guide.](https://support.google.com/mail/answer/185833?hl=en)
    4. `DEFAULT_EXT`: By default I'm searching for only `epub` files for portability reasons. Change this var for other formats.
    
5. Start the web server:
  ```bash
  python run.py
  ```
6. Open app in browser at http://localhost:5000


## Caveats

Sometimes Amazon complains about a problem uploading to kindle even if the file is readable. It doesn't give any details as to why the upload failed. This happens sometimes when you upload the file manually too, so if this happens try another link.


### Credits

 Shoutout to [harrison-broadbent](https://github.com/harrison-broadbent) for their [libgen-api.](https://github.com/harrison-broadbent)