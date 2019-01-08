import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, "lxml")
	pages = soup.find("div", class_="pagination-pages").find_all("a", class_="pagination-page")[-1].get("href")
	total_pages = pages.split("=")[1].split("&")[0]
	return int(total_pages)


def write_csv(pages):
	with open("avito.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow((data["title"],
						  data["price"],
						  data["address"],
						  data["url"]))


def get_page_data(html):
	soup = BeautifulSoup(html, "lxml")
	ads = soup.find("div", class_="catalog-list").find_all("div", class_="item-table")
	for ad in ads:
		name = ad.find("div", class_="description").find("h3").text.strip()
		if "samsung" in name:
			try:
				title = ad.find("div", class_="description").find("h3").text.strip()
			except:
				title = ""
			try:
				url = "https://www.avito.ru" + ad.find("div", class_="description").find("h3").find("a").get("href")
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

			data = {"title": title,
					"price": price,
					"address": address,
					"url": url}
			write_csv(data)
		else:
			continue

def main():
	url = "https://www.avito.ru/rostov-na-donu/telefony/samsung1&q=samsung"
	base_url = "https://www.avito.ru/rostov-na-donu/telefony/samsung"
	page_part = "s_trg="
	query_part = "&q=samsung"
	total_pages = get_total_pages(get_html(url))
	for i in range(1, total_pages):
		url_gen = base_url + page_part + str(i) + query_part
		html = get_html(url_gen)
		get_page_data(html)

if __name__ == '__main__':
	main()