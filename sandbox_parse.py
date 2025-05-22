import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_tutors_page(html):
    soup = BeautifulSoup(html, "html.parser")
    tutors = []

    for block in soup.select(".thumbnail"):
        name = block.select_one(".title").text.strip()
        price = block.select_one(".price").text.strip()
        tutors.append({"name": name, "price": price})

    return tutors


def main():
    url = "https://buki.com.ua/tutors-online/biolohiia/"
    html = get_html(url)
    data = parse_tutors_page(html)

    for tutor in data:
        print(f"{tutor['name']} - {tutor['price']}")


if __name__ == "__main__":
    main()