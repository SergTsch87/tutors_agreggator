import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_element(block_tag, tag_class):
    return block_tag.select_one(tag_class).get_text(strip=True) if block_tag else "N/A"


def parse_tutor_card(html_card):
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')

    # Extract the tutors name
    name = get_element(soup, ".styles_userName__ltIVo span")
    
    # Extract the price
    price = get_element(soup, ".rate .topCeil")

    object_item = ''
    for item in soup.find_all('span', class_="styles_lessonsItem__v8FAD"):
        object_item += item.get_text(strip=True) + ', '
        print(f'object_item: {object_item}')

    ratg_revs = soup.find('div', class_="styles_reviewsBlock__FNrPL") if soup else "N/A"
    rating = ratg_revs.select_one('span').get_text(strip=True)
    number_of_reviews = ratg_revs.find('span', class_="styles_reviewsCount__EAIh6").get_text(strip=True)

    main_info = soup.find('div', class_="styles_mainInfo__cK8Ru") if soup else "N/A"
    # education = main_info.find('p', class_="styles_education__41VXk").select_one('span').get_text(strip=True)
    education = main_info.find('p', class_="styles_education__41VXk").get_text(strip=True)
    experience = main_info.find('p', class_="styles_practice__AZyXc").get_text(strip=True)
    
    # current_price = extract_element(soup, "div", "ft-whitespace-nowrap ft-text-22 ft-font-bold")

    return {
            "name": name,
            "price": price,
            "objects": object_item,
            "rating": rating,
            "number_of_reviews": number_of_reviews,
            "education": education,
            "experience": experience
        }


def parse_tutors_page(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    # for block in soup.select(".styles_container__4lrBa"):
    tutor_cards = soup.select(".styles_container__4lrBa")
    for card in tutor_cards:
        current_card = parse_tutor_card(str(card))
        tutors.append(current_card)

    return tutors


def main():
    url = "https://buki.com.ua/tutors-online/biolohiia/7/"
    html = get_html(url)
    data = parse_tutors_page(html)

    for tutor in data:
        print(f"Tutor name: {tutor['name']},  Price: {tutor['price']},  Objects: {tutor['objects']}, Rating: {tutor['rating']}, Number of reviews: {tutor['number_of_reviews']}, Education: {tutor['education']}, Experience: {tutor['experience']}")


    # html_str = "<p class='styles_education__41VXk'>Освіта: <span>Запорізький державний медичний університет (ЗДМУ)</span></p>"
    # soup_elem = BeautifulSoup(html_str, "html.parser")
    
    # education = soup_elem.find('p', class_="styles_education__41VXk")
    # print(f"education = {education.get_text(strip=True)}")
    # print(f"education = {education}")


if __name__ == "__main__":
    main()