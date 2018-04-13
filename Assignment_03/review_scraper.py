
from lxml import html
import requests
import json
import json, re
from time import sleep



header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
reviews_df = []

def scrape(url):
    headers = {'User-Agent': header}
    page = requests.get(url, headers = headers)
    parser = html.fromstring(page.content)

    ### this part was in an online tutorial of scraping from python that seemed a bit more intuative than bs4
    ### the format .//identifier[@class_name]//retrieve_text_function does simplify things and lxml does run it faster
    xpath_reviews = '//div[@data-hook="review"]'
    reviews = parser.xpath(xpath_reviews)

    xpath_rating  = './/i[@data-hook="review-star-rating"]//text()'
    xpath_title   = './/a[@data-hook="review-title"]//text()'
    xpath_author  = './/a[@data-hook="review-author"]//text()'
    xpath_date    = './/span[@data-hook="review-date"]//text()'
    xpath_body    = './/span[@data-hook="review-body"]//text()'
    xpath_helpful = './/span[@data-hook="helpful-vote-statement"]//text()'

    print("Start scraping")

    for review in reviews:
        rating = review.xpath(xpath_rating)
        title = review.xpath(xpath_title)
        author = review.xpath(xpath_author)
        date = review.xpath(xpath_date)
        body = review.xpath(xpath_body)
        helpful = review.xpath(xpath_helpful)
        sleep(3)

        review_dict = {'rating': rating,
                    'title': title,
                    'author': author,
                    'date': date,
                    'body': body,
                    'helpful': helpful}
        reviews_df.append(review_dict)
        sleep(5)

def make_json(df):
    f = open('review.json', 'w')
    json.dump(df, f, indent=4)
    print("json is done")

page = []
baselink = 'https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM'

### this creation of a list of page urls was derived from our group project scraping
### link modified to include chronological order, which resulted in an extra page scraped (prior to changes in assignment)
for i in list(range(1, 95)):
    page_link = baselink + '/ref=cm_cr_getr_d_paging_btm_prev_' + str(i) + '?pageNumber=' + str(i) + '&sortBy=recent'
    page.append(page_link)

def scrape():
    for webpage in page:
        scrape(webpage)
    make_json(reviews_df)

def main():
    scrape()
if __name__ == '__main__':
    main()

