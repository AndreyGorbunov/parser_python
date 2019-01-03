from bs4 import BeautifulSoup
import csv

def get_html(url):
	r = requests.get(url)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]
	return int(total_pages)
	
def write_csv(pages):

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div', class_='catalog-list').find_all('div', class_='item-table')
	for ad in ads:
		try:
			title = ad.find('div', class_='description').find('h3').text.strip()
		except: 
			title = ""
			
		try:
			url = "https://www.avito.ru" + ad.find("div", class_="description").find("h3").find("a").get("href")
		except:
			url = ""
		
	
    