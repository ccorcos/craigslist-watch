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

## Setup Raspberry Pi with a Cron job

I setup a cron job on my raspberry pi so that it runs every day and emails me
the aggregated results. Here's how you do it:

### Quick Raspberry Pi Setup
1. Install Raspian on your raspberry pi.
2. Install `avahi-daemon` so you can ssh without knowing the IP address:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install avahi-daemon
```
Now you can ssh into your pi via `ssh pi@raspberrypi.local`.
3. Make sure you install and setup vim:
```
sudo apt-get install vim
echo "set nocompatible" > ~/.vimrc
echo "export VISUAL=vim" > ~/.bashrc
echo "export EDITOR=$VISUAL" > ~/.bashrc
```
4. Dont forget to install the pip python manager!
```
sudo apt-get install python-pip
```

### Cron Jobs Setup
There's very simple [documentation](http://www.raspberrypi.org/documentation/linux/usage/cron.md) for setting up a cron job on your raspberry pi.

First, find the path to `craigslist.py` (for me it is `/home/pi/programs/craigslist-watch/craigslist.py`) and then run `crontab -e` to open up the cron job list. Append the following to the end (in Vim: <ESC>Go to start editing at the end ;):
```
# Craigslist Script
0 16 * * * python /home/pi/programs/craigslist-watch/craigslist.py
```

And that should be it!
