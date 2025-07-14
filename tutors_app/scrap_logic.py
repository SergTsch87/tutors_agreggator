import requests
from bs4 import BeautifulSoup
from functools import lru_cache
import logging
import time
from tutors_app.utils import parse_price, get_num_of_reviews, is_connected, handle_exception
# from tutors_app.file_dir_sys import save_to_file
# sandbox.get_list_ids_tutors_on_page


def get_html(url: str, timeout=20, return_soup=True):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        html = response.text
        soup_or_html = BeautifulSoup(html, 'html.parser') if return_soup else html
        is_redirect = 1 if 300 <= response.status_code < 400 else 0
        return soup_or_html, is_redirect        # 0 == 'No redirect'   # 1 == 'redirect'
    except requests.exceptions.RequestException as e:
        print(f'An error occured: {e}')
        return None, -1  # Уніфікований фолбек на помилку  # always return a tuple


@lru_cache(maxsize = 3000)  # Для кешування повторних URL адрес
def fetch_url_with_retries(url, retries=3, timeout=10, return_soup=False):
    """
    Фактично, ця ф-ція є обгорткою для get_html(), запускаючи останню до 3-х разів, з перервою у 10 сек між повторами
    
    Fetches a URL with a specified number of retries on network-related errors.
    #  Fetches the HTML content of a webpage with error handling for network issues.

    Args:
        url (str): The URL of the webpage to fetch.
        retries (int): Number of retry attempts.
        timeout (int): Timeout in seconds for the request.

    Returns:
        str: The HTML content of the page, or an error message if an exception occurs.

    Example of use:
        html = fetch_url_with_retries(url, retries=3, timeout=10)

        if not html:
            print("Empty HTML or failed to fetch page.")
            break
    """
    
    if not is_connected():  # Якщо нема інтернет-зв'язку
        print('Error: No internet connection')
        return None, -1
        # return 'Error: No internet connection'

    # Повтори при таймаутах
    for attempt in range(retries):
        try:
            print(f'Fetching URL: {url}')  # !!! переконайтеся, що ви дійсно отримуєте нову сторінку
            html, redirect = get_html(url, timeout=timeout, return_soup=return_soup)
            
            if html:
                return html, redirect  # Успішний запит, - Повертаємо контент

            # # if html is None or len(html.strip()) == 0:
            # #     return []
            # if html is None or ( not return_soup and len(html.strip()) == 0 ): # ???
            #     return 'Error: Empty HTML content'
            
            # return html, redirect  # Успішний запит, - Повертаємо контент
        
        except requests.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed for {url}.")
            if attempt == retries - 1:  # Last attempt
                return handle_exception(e, context=f"Fetching URL {url}")
            time.sleep(2 ** attempt)  #  Покрокове збільшення затримки, - задля уникнення блокування сервером

    return 'Error: Failed to fetch the URL after multiple retries.'  # Якщо усі спроби були невдалі:...


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


# ------------------------------------------------
# Site BUKI com

# Це скрапінг картки репетитора на Загальній(!) сторінці.
def parse_tutor_card_buki(html_card: str) -> dict:
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')
    about_myself = soup.select_one('p.styles_description__EnqoA')
    return {
            "id_tutor": int(soup.select_one(".styles_userName__ltIVo a")["href"][6:-1]),
            "name": get_element(soup, ".styles_userName__ltIVo span"),
            "price": parse_price(get_element(soup, ".rate .topCeil")),
            # "price": get_element(soup, ".rate .topCeil"),
            "objects": [o.get_text(strip=True) for o in soup.find_all('span', class_="styles_lessonsItem__v8FAD")],
            "rating": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span"),
            # "number_of_reviews": safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span", class_name="styles_reviewsCount__EAIh6"),
            "number_of_reviews": get_num_of_reviews(safe_text(soup.select_one('div.styles_reviewsBlock__FNrPL'), "span", class_name="styles_reviewsCount__EAIh6")),
            "education": safe_text(soup.select_one('p.styles_education__41VXk'), "span"),
            
            "experience": safe_text(soup.select_one('p.styles_practice__AZyXc'))[15:-6].strip() + '+',
            
            # "about_myself": safe_text(soup.select_one('p.styles_description__EnqoA')),
            "about_myself": about_myself.select_one('span').get_text(strip=True) + about_myself.select_one('span.next_sibling').get_text(strip=True),
            
            "city_or_online": safe_text(soup.select_one('div.styles_userData__xpfLk a')),
        }


# !!!
        # Це скрапінг картки репетитора на сторінці самого екаунту
# !!!
    # Вдоскональ цю ф-цію!
def get_data_from_one_account(id_rep):
    # Extract Data from a Single Account
    tag_body = get_tag_body(id_rep)
    url = f"https://buki.com.ua/user-{id_rep}/"
    fetch_url_with_retries(url, retries=3, timeout=10, return_soup=False)
    return {
            # "id_tutor": id_rep,
            # "name": <list>['name'], # get_element(tag_body, ".styles_userName__ltIVo span"),
            # "price": <list>['price'], # parse_price(get_element(tag_body, ".rate .topCeil")),
            # "objects": ['bio'],
            # "rating": <list>['rating'],
            # "number_of_reviews": <list>['rating'],
            # "education": <list>['education'],
            # "experience": <list>['experience'],
            "about_myself_1": get_element(tag_body, "p.styles_mobileDescription__LxjZs"),
            "about_myself_2": get_element(tag_body, "p.styles_aboutMe__4uKLA"),
            # "city_or_online": <list>['city_or_online'],
        }


def parse_tutors_page_buki(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    tutor_cards = soup.select(".styles_container__4lrBa")
    for card in tutor_cards:
        current_card = parse_tutor_card_buki(str(card))
        tutors.append(current_card)

    return tutors


# ---------------------------------
# Site PROFREP
def parse_tutor_card_profrep(html_card):
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')
    return {
            "name": safe_text(soup.select_one('div.card-courses-title'), "span"),            
            "price": None,
            "objects": None,
            "rating": None,
            "number_of_reviews": None,
            "education": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(2)')),
            "experience": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(1)')),
            "about_myself": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(3)')),
            "city_or_online": safe_text(soup.select_one('i.fa fa-map-marker-alt')),
        }


def parse_tutors_page_profrep(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    # tutor_cards = soup.select(".row > .col-lg-12.m-b30 > .widget-inner")
    tutor_cards = soup.select(".widget-inner")
    for card in tutor_cards:
        current_card = parse_tutor_card_profrep(str(card))
        tutors.append(current_card)

    return tutors


# def get_list_ids_tutors_on_page(num_page):
#     pass


def get_tag_body(num_page):
    url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    soup, _ = fetch_url_with_retries(url, retries=3, timeout=10, return_soup=True)
    if soup is None:
        return None
    # if not soup:
    #     return None
    tag_body = soup.select_one('body')
    return tag_body
    

def get_max_pagination(soup_element):
    return int( safe_text( soup_element.select(".styles_pagination__qGM14 div a")[-1] ) )


def get_tutor_urls(soup_elem):
    return soup_elem.select_one(".styles_userName__ltIVo a")["href"][6:-1]