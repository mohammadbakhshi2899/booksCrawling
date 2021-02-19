import requests
from bs4 import BeautifulSoup
import base64
import json

books = {}

def getPagesInfo():
    req = requests.get(f'http://books.toscrape.com/catalogue/page-1.html')
    count = 1
    print(req)
    while req.ok :
        soup = BeautifulSoup(req.content, 'html.parser')
        base_url = 'http://books.toscrape.com/catalogue/'
        for url in getBookpage(soup):
            book = getBookInfo(base_url+url)
            books[book[0]] = book[1]
            print(len(books))
        count += 1
        req = requests.get(f'http://books.toscrape.com/catalogue/page-{count}.html')
        print(f'http://books.toscrape.com/catalogue/page-{count}.html')
    return count

def getBookpage(req:BeautifulSoup):
    booksUrl = []
    for i in req.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        booksUrl.append(i.find('a').attrs['href'])
    return booksUrl

def getBookInfo(url):
    soup      = BeautifulSoup(requests.get(url).content, 'html.parser')
    bookName  = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
    bookPrice = soup.find('p', {'class':"price_color"}).get_text()
    bookDescription = soup.find_all('p')[3].get_text()
    bookImg = getImageInBase64(soup)
    bookInfo = {
        'book_price':bookPrice,
        'book_description':bookDescription,
        'book_image':bookImg
    }
    return (bookName, bookInfo)

def getImageInBase64(soup:BeautifulSoup):
    domain = 'http://books.toscrape.com'
    bookImg = requests.get(domain + soup.find('img').attrs['src'][5:]).content
    inBase64 = base64.b64decode(bookImg)
    return inBase64

if __name__ == '__main__':
    getPagesInfo()
    with open('books.json', 'w') as f :
        json.dump(books, f)
        f.close()
