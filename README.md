# Vanguard Scraper

Mint and Personal Capital are cool, but they can be unreliable. Account history can be lost, duplicated, or obscured. For a more reliable and accurate financial history I like to use them as a reference but aggregate it elsewhere. This is a tool that will help reduce the manual burden of getting data from Vanguard and automate it instead.

I hope.

## Process

Following [this](https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72) tutorial.

Except that I created the virtual environment with:

```
python3 -m venv env
```

## TODOs
- [] You are getting an extraneous result per row. Make sure that isn't getting in there (I think it's a bug with last_row_index)
- [] Allow inputting the date for which you want to get the account balances