import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_element(block_tag, tag_class):
    return block_tag.select_one(tag_class).get_text(strip=True) if block_tag else "N/A"


def parse_tutors_page(html):
    soup = BeautifulSoup(html, "html.parser")
    tutors = []

    for block in soup.select(".styles_container__4lrBa"):
        # Extract the tutors name
        # name_tag = block.select_one(".styles_userName__ltIVo span")
        # name = name_tag.get_text(strip=True) if name_tag else "N/A"
        name = get_element(block, ".styles_userName__ltIVo span")
        
        # Extract the price
        # price_tag = block.select_one(".rate.schoolRate .topCeil")
        # price_tag = block.select_one(".rate .topCeil")
        # price = price_tag.get_text(strip=True) if price_tag else "N/A"
        price = get_element(block, ".rate .topCeil")

        object_item = ''
        for item in block.find_all('span', class_="styles_lessonsItem__v8FAD"):
            object_item += item.get_text(strip=True) + ', '
            print(f'object_item: {object_item}')
            
        tutors.append({"name": name, "price": price, "objects": object_item})

    return tutors


def main():
    url = "https://buki.com.ua/tutors-online/biolohiia/5/"
    html = get_html(url)
    data = parse_tutors_page(html)

    for tutor in data:
        print(f"Tutor name: {tutor['name']},  Price: {tutor['price']},  Objects: {tutor['objects']}")


if __name__ == "__main__":
    main()