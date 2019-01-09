import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, "lxml")
	pages = soup.find("div", class_="pagination-pages").find_all("a", class_="pagination-page")[-1].get("href")
	total_page_number = pages.split("=")[1].split("&")[0]
	return int(total_page_number)


def write_csv(data):
	with open("avito.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow((data["title"],
						 data["price"],
						 data["address"],
						 data["url"],
						 data["date"]))


def get_page_data(html):
	soup = BeautifulSoup(html, "lxml")
	ads = soup.find("div", class_="catalog-list").find_all("div", class_="item_table")
	for ad in ads:
		name = ad.find("div", class_="description").find("div", class_="item_table-header").find("h3").text.strip().lower()
		if "samsung" or "самсунг" in name:
			try:
				title =  ad.find("div", class_="description").find("div", class_="item_table-header").find("h3").text.strip()
			except:
				title = ""
			try:
				url = "https://www.avito.ru" + ad.find("div", class_="description").find("div", class_="item_table-header").find("h3").find("a").get("href")
			except:
				url = ""
			try:
				price = ad.find("div", class_="about").text.strip()
			except:
				price = ""
			try:
				address = ad.find("div", class_="data").find_all("p")[-1].text.strip()
			except:
				address = ""
			try:
				date = ad.find("div", class_="data").find("div", class_="js-item-date c-2").text.strip()
			except:
				date = ""

			data = {"title": title,
					"price": price,
					"address": address,
					"url": url,
					"date": date}
			write_csv(data)
		else:
			continue


def main():
	url = "https://www.avito.ru/rostov-na-donu/telefony/samsung?p=29&q=samsung"
	base_url = "https://www.avito.ru/rostov-na-donu/telefony/samsung?"
	page_part = "p="
	query_part = "&q=samsung"
	total_pages = get_total_pages(get_html(url))
	for i in range(1, 3):
		url_gen = base_url + page_part + str(i) + query_part
		html = get_html(url_gen)
		get_page_data(html)

if __name__ == '__main__':
	main()