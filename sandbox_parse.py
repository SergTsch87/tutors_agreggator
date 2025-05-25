import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_element(block_tag, tag_class):
    return block_tag.select_one(tag_class).get_text(strip=True) if block_tag else "N/A"


# def safe_text(soup_or_el, selector=None, class_name=None,  tag='span', default="N/A"):
#     if not soup_or_el:
#         return default
#     try:
#         if class_name:
#             el = soup_or_el.find(tag, class_=class_name)
#         elif selector:
#             el = soup_or_el.select_one(selector)
#         else:
#             return default
#         return el.get_text(strip=True) if el else default
#     except Exception:
#         return default

def safe_text(soup_or_el, selector=None, class_name=None,  tag='span', default="N/A"):
    if not soup_or_el:
        return default
    
    try:
        if selector or class_name:
            if class_name:
                el = soup_or_el.find(tag, class_=class_name)
            else:
                el = soup_or_el.select_one(selector)
    
        else:
            el = soup_or_el  # Вважаємо, що передали вже готовий елемент
    
        return el.get_text(strip=True) if el else default
    
    except Exception:
        return default


def parse_tutor_card(html_card):
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')

    # # ratg_revs = soup.find('div', class_="styles_reviewsBlock__FNrPL") if soup else "N/A"
    # # rating = ratg_revs.select_one('span').get_text(strip=True)
    # safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span")

    # # number_of_reviews = ratg_revs.find('span', class_="styles_reviewsCount__EAIh6").get_text(strip=True)
    # safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span", class_name="styles_reviewsCount__EAIh6")
    

    # # main_info = soup.find('div', class_="styles_mainInfo__cK8Ru") if soup else "N/A"
    # # # education = main_info.find('p', class_="styles_education__41VXk").select_one('span').get_text(strip=True)
    # # education = main_info.find('p', class_="styles_education__41VXk").get_text(strip=True)
    # safe_text(soup.select_one('div.styles_mainInfo__cK8Ru'), "p", class_name="styles_education__41VXk")

    # # experience = main_info.find('p', class_="styles_practice__AZyXc").get_text(strip=True)
    # safe_text(soup.select_one('div.styles_mainInfo__cK8Ru'), "p", class_name="styles_practice__AZyXc")
    
    # current_price = extract_element(soup, "div", "ft-whitespace-nowrap ft-text-22 ft-font-bold")

    return {
            "name": get_element(soup, ".styles_userName__ltIVo span"),
            "price": get_element(soup, ".rate .topCeil"),
            "objects": [o.get_text(strip=True) for o in soup.find_all('span', class_="styles_lessonsItem__v8FAD")],
            "rating": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span"), # rating,
            "number_of_reviews": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span", class_name="styles_reviewsCount__EAIh6"), # number_of_reviews,
            "education": safe_text(soup.select_one('p.styles_education__41VXk'), "span"), # education,
            "experience": safe_text(soup.select_one('p.styles_practice__AZyXc')), # experience
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
    url = "https://buki.com.ua/tutors-online/biolohiia/3/"
    # url = "https://profrepetitor.com.ua/repetitors-biologiya"
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