from bs4 import BeautifulSoup
import requests, re, csv

main_url = "https://books.toscrape.com/"
response = requests.get(main_url).content
document = BeautifulSoup(response, "html.parser")

books = {}

pages = int(document.find(class_="current").string.strip().split(" ")[-1])
for page in range(1, pages + 1):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url).content
    document = BeautifulSoup(response, "html.parser")
    articles = document.find_all(class_="product_pod")
    for article in articles:
        img = main_url + article.img["src"]
        title = article.h3.string.strip()
        price = article.find(class_="price_color").string.strip()
        instock = article.find(class_="instock availability").text.strip()

        books[title] = {"price": price, "stock": instock, "image": img}



with open("books.csv", "w+") as file:
    dictwriter = csv.DictWriter(file, fieldnames=["title", "price", "stock", "image"])
    dictwriter.writerow({"title": "title", "price": "price", "stock": "stock", "image": "image"})
    for title in books:
        dictwriter.writerow({"title": title, "price": books[title]["price"], "stock": books[title]["stock"], "image": books[title]["image"]})