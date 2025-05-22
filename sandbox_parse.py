import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_tutors_page(html):
    soup = BeautifulSoup(html, "html.parser")
    tutors = []

    for block in soup.select(".styles_container__4lrBa"):
        # Extract the tutos name
        name_tag = block.select_one(".styles_userName__ltIVo span")
        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        #__next > div > section > div.styles_tutorsContainer__y5yzC > div.styles_catalogWrapper__zRZcm > div.styles_mainContent__fp_h3 > div.styles_tutorsList__80R_9 > div:nth-child(1) > div > div.styles_userPreviewWrapper__HBWPS > div.styles_userPreview__dSzlG > p > span
        #__next > div > section > div.styles_tutorsContainer__y5yzC > div.styles_catalogWrapper__zRZcm > div.styles_mainContent__fp_h3 > div.styles_tutorsList__80R_9
        # price_tag = block.select_one(".rate.schoolRate .topCeil")
        price_tag = block.select_one(".rate .topCeil")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
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