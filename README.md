# Craigslist Watch / Notifier

This is a simple python program using [import.io](https://import.io/) to scrape
data from craigslist every day and send emails that fit the criteria. You can't
use this right out of the box because of API keys and Gmail passwords. But its
a great place to start for making your own craigslist watcher.

The primary motivation for this program is to notify me of suitable apartments
because the goo ones come and go very quickly. I'm also looking to share a house
with a few friends and Craigslist doesn't allow you to filter based on price per
bedroom and sort them!

This program could easily be repurposed for creating a watch for anything -- like
the two bikes stolen off my porch this past year!

## Getting Started

1. Download and install [import.io](https://import.io/).
2. Create an API selecting various information
3. Fill out `craigslist.py` with your custom API and filters.
4. Create a file called `secrets.py` with the following information:
```
api_key=""
emailAddress = 'username@gmail.com'
emailPassword = ''
```
## CRON Job!

I setup a cron job on my raspberry pi so that it runs every day and emails me
the aggregated results. Here's how you do it:

1. Install Raspian on your raspberry pi.
2. Install `avahi-daemon` so you can ssh without knowing the IP address:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install avahi-daemon
```
Now you can ssh into your pi via `ssh pi@raspberrypi.local`.
3.
