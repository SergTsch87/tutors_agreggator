import requests
from bs4 import BeautifulSoup
# from decors import parse_example
from decors import log_parse


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_element(block_tag, tag_class):
    return block_tag.select_one(tag_class).get_text(strip=True) if block_tag else "N/A"


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


def parse_tutor_card_buki(html_card):
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')
    return {
            "name": get_element(soup, ".styles_userName__ltIVo span"),
            "price": get_element(soup, ".rate .topCeil"),
            "objects": [o.get_text(strip=True) for o in soup.find_all('span', class_="styles_lessonsItem__v8FAD")],
            "rating": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span"),
            "number_of_reviews": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span", class_name="styles_reviewsCount__EAIh6"),
            "education": safe_text(soup.select_one('p.styles_education__41VXk'), "span"),
            "experience": safe_text(soup.select_one('p.styles_practice__AZyXc')),
            "about_myself": None,
            "city_or_online": None,
        }


def parse_tutor_card_profrep(html_card):
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')
    return {
            # "name": get_element(soup, ".card-courses-title h4 span"),
            # "name": get_element(soup, ".card-courses-title span"),
            "name": safe_text(soup.select_one('div.card-courses-title'), "span"),
            
            "price": None,
            "objects": None,
            
            "rating": None,
            "number_of_reviews": None,
            "education": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(2)')),
            # col-md-12 catalog-item-desc mt-1
            # div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(2) > b
            "experience": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(1)')),
            # div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(1) > b

            "about_myself": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(3)')),
            # div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(3)

            "city_or_online": safe_text(soup.select_one('i.fa fa-map-marker-alt')),
        }


def parse_tutors_page_buki(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    tutor_cards = soup.select(".styles_container__4lrBa")
    for card in tutor_cards:
        current_card = parse_tutor_card_buki(str(card))
        tutors.append(current_card)

    return tutors


def parse_tutors_page_profrep(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    # tutor_cards = soup.select(".row > .col-lg-12.m-b30 > .widget-inner")
    tutor_cards = soup.select(".widget-inner")
    # print(f'\ntutor_cards: {tutor_cards}\n')
    # print(f'\nsize(data): {len(tutor_cards)}\n')
    # print(f'tutor_cards: {tutor_cards}')
    for card in tutor_cards:
        current_card = parse_tutor_card_profrep(str(card))
        tutors.append(current_card)

    return tutors


# def log_parse(func):
#     def wrapper(*args, **kwargs):
#         print('Starting parsing...')
#         result = func(*args, **kwargs)
#         print('Parsing done.')
#         return result
    
#     return wrapper


@log_parse
def parse_example():
    print('Parsing something...')


def main():
    # # url = "https://buki.com.ua/tutors-online/biolohiia/3/"
    # # html = get_html(url)
    # # data = parse_tutors_page_buki(html)

    # url = "https://profrepetitor.com.ua/repetitors-biologiya"
    # html = get_html(url)
    # # print(f'\nsize(html): {len(html)}\n')
    # data = parse_tutors_page_profrep(html)
    # # print(f'\nCount elements of data: {len(data)}\n')

    # for tutor in data:
    #     print(f"Tutor name: {tutor['name']},  Price: {tutor['price']},  Objects: {tutor['objects']}, Rating: {tutor['rating']}, Number of reviews: {tutor['number_of_reviews']}, Education: {tutor['education']}, Experience: {tutor['experience']}, about_myself: {tutor['about_myself']}, city_or_online: {tutor['city_or_online']}")


    parse_example()


    # html_str = "<p class='styles_education__41VXk'>Освіта: <span>Запорізький державний медичний університет (ЗДМУ)</span></p>"
    # soup_elem = BeautifulSoup(html_str, "html.parser")
    
    # education = soup_elem.find('p', class_="styles_education__41VXk")
    # print(f"education = {education.get_text(strip=True)}")
    # print(f"education = {education}")


if __name__ == "__main__":
    main()