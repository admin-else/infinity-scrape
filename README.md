# Infinity Scraper

Have you ever wanted to create anime or honey or anything else in [Infinity Craft](https://neal.fun/infinite-craft/), but didn't know how? With this repository, now you can...

## Installation

```bash
$ git clone https://github.com/admin-else/infinity-scrape
$ pip3 install -r requirements.txt
```

## Usage

Once you have installed everything, you can run:

```bash
$ python3 howtoget.py
```

This command will provide you with a list of items you need to craft for your desired item. However, if you encounter a message like:

```bash
$ python3 howtoget.py
what do you want: trolling
didn't find source of Trolling...
```

It means the source for your desired item is not found. In such a case, you need to run the scraper again until you find your desired word. You can do this with:

```bash
$ python3 scrape.py
```

If you do that, it would be appreciated if you could make a pull request so that other people don't have to go through the same process.