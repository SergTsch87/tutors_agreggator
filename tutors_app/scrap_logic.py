import requests
from bs4 import BeautifulSoup
from functools import lru_cache
import logging
import time
from random import uniform
from tutors_app.utils import parse_price, is_connected, handle_exception  # get_num_of_reviews
# from file_dir_sys import save_to_file
# sandbox.get_list_ids_tutors_on_page


ABOUT_SEPARATOR = '   >])([<   '


def correct_url(num_page):
    if num_page == 1:
        return "https://buki.com.ua/tutors/biolohiia/"
    else:
        return f"https://buki.com.ua/tutors/biolohiia/{num_page}/"


# Чи знаходимось ми зараз на останній сторінці пагінації?..
# Якщо нема наступного елементу 'a' (посилання на будь-яку наступну сторінку), - тоді повертає False
def is_there_next_page(soup):
    return bool( soup.select("span.styles_button__6Yhoi.styles_active__O51t0 + a") )


def get_html(url: str, timeout=20, return_soup=True):
    try:
        time.sleep( uniform( 0.5, 2.0 ) ) # Павза перед кожним запитом до сайту
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        html = response.text
        # print(f'html: {html}') # for test
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
            # print(f'(Msg from func fetch_url_with_retries) Fetching URL: {url}')  # !!! переконайтеся, що ви дійсно отримуєте нову сторінку
            print(f'Fetching URL: {url}')

            # !!! А що, хіба get_tag_body тут не потрібне?!
            html, redirect = get_html(url, timeout=timeout, return_soup=return_soup)
            
            if html:
                # print(f'\nFROM fetch_url_with_retries:\nhtml: {html}\n')
                # print(f'redirect: {redirect}')
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
    return block_tag.select_one(tag_class).get_text(strip=True) if block_tag else "" # Було: else "N/A"


def safe_text(soup_or_el, selector=None, class_name=None,  tag='span', default=""):  #  Було:  , default="N/A"):
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

def extract_about_myself(soup):
    paragraph = soup.select_one('p.styles_description__EnqoA')
    spans = paragraph.select('span') if paragraph else []
    a_m_1 = spans[0].get_text(strip=True) if len( spans ) > 0 else ''
    a_m_2 = spans[-1].get_text(strip=True) if len( spans ) > 0 else a_m_1  # Чому тут 1 ?

    if not a_m_1 and not a_m_2:
        return ''
    
    if (not a_m_1 or not a_m_2) or (a_m_1 and a_m_2):
        return a_m_1 + a_m_2
    
    about_combined = f"{a_m_1}{ABOUT_SEPARATOR}{a_m_2}"
    
    return '' if len(about_combined) == len(ABOUT_SEPARATOR) else about_combined


def extract_price(soup):
    price_el = soup.select_one("span.topCeil")
    return parse_price( get_element( soup, "span.topCeil" ) ) if price_el else ''
   

def extract_city(soup):
    city_el = soup.select_one("div.styles_userData__xpfLk a")
    return safe_text(city_el) if city_el else ''


def extract_reviews_count(soup):
    reviews_el = soup.select_one("span.styles_reviewsCount__EAIh6")
    return safe_text(reviews_el)[11:-1].strip() if reviews_el else ''


def extract_rating(soup):
    rating_el = soup.select_one('div.styles_reviewsBlock__FNrPL span')
    return safe_text(rating_el)


def extract_education(soup):
    edu_el = soup.select_one('p.styles_education__41VXk')
    return safe_text(edu_el, "span") if edu_el else ''


def extract_experience(soup):
    exp_el = soup.select_one('p.styles_practice__AZyXc')
    return safe_text(exp_el)[14:-5].strip() if exp_el else ''


def extract_subjects(soup):
    return [el.get_text(strip=True) for el in soup.select('span.styles_lessonsItem__v8FAD')]


def extract_name(soup):
    return get_element( soup, ".styles_userName__ltIVo span" )


def extract_id(soup):
    # print(f'ID rep: {soup.select_one("p.styles_userName__ltIVo a")}')
    tag_a = soup.select_one("p.styles_userName__ltIVo a")
    if not tag_a:
        img_with_id = soup.select_one("div.styles_imageWrapper__GmpHF div img")
        img_title = img_with_id['title']
        if img_title:
            beg_index_id_rep = img_title.find('id:')
            id_rep = img_title[beg_index_id_rep + 3:]
            return int(id_rep)
        #  div.styles_imageWrapper__GmpHF div img[title] "Репетитор - Софія Китчак id:195421"
    href = soup.select_one(".styles_userName__ltIVo a")["href"]
    return int(href[6:-1])


def extract_is_online(soup):
    # is_online = soup.select_one('p.styles_workOnline__p4t8f')
    # return True if is_online else False
    return soup.select_one('p.styles_workOnline__p4t8f') is not None


# Це скрапінг картки репетитора на Загальній(!) сторінці.
def parse_tutor_card_buki(html_card: str) -> dict:
    # Extract Data from a Single Tutor Card
    # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
    soup = BeautifulSoup(html_card, 'html.parser')

    # id_tutor = extract_id(soup)

    # about_myself = soup.select_one('p.styles_description__EnqoA')
    # if about_myself.select_one('span') is not None:
    #     a_m_1 = about_myself.select_one('span').get_text(strip=True)
    # elif ( len( about_myself.select_one('span').get_text(strip=True) ) == 0)  or ( about_myself.select_one('span') is None ):
    #     a_m_1 = ''

    # if about_myself.select('span')[-1] is not None:
    #     a_m_2 = about_myself.select('span')[-1].get_text(strip=True)
    # elif ( len( about_myself.select('span')[-1].get_text(strip=True) ) == 0)  or ( about_myself.select('span')[-1] is None ):
    #     a_m_2 = ''

    # about_myself = a_m_1 + '   >])([<   ' + a_m_2
    # if len(about_myself) == 12:
    #     about_myself = ''
    # elif ( len(a_m_1) == 0 ) or ( len(a_m_2) == 0 ):
    #     about_myself = a_m_1 + a_m_2
    about_myself = extract_about_myself(soup)

    # price = soup.select_one("span.topCeil")
    # if price is not None:
    #     price = parse_price( get_element( soup, "span.topCeil" ) )
    # else:
    #     price = ''
    price = extract_price(soup)

    # if soup.select_one('p.styles_workOnline__p4t8f') is not None:
    #     is_online = True
    # else:
    #     is_online = False

    # if soup.select_one('div.styles_userData__xpfLk a') is not None:
    #     city = safe_text(soup.select_one('div.styles_userData__xpfLk a'))
    # else:
    #     city = ''

    # if soup.select_one('span.styles_reviewsCount__EAIh6') is not None:
    #     number_of_reviews = safe_text(soup.select_one('span.styles_reviewsCount__EAIh6'))[11:-1].strip()
    # else:
    #     number_of_reviews = ''
    
    # Оминаємо певного репетитора з порожніми водночас ціною та about
    if not about_myself and not price:
        return {
            "id_tutor": extract_id(soup),
            "empty": "empty",
            "name": '',
            "price": '',
            "objects": '',
            "rating": '',
            "number_of_reviews": '',
            "education": '',
            "experience": '',
            "about_myself": '',
            "about_myself_1": '',
            "about_myself_2": '',
            "city": '',
            "is_online": '',
            }


    return {
            "id_tutor": extract_id(soup),
            "name": extract_name(soup),
            "price": price,
            "objects": extract_subjects(soup),
            "rating": extract_rating(soup),
            "number_of_reviews": extract_reviews_count(soup),
            "education": extract_education(soup),
            "experience": extract_experience(soup),
            "about_myself": about_myself,
            "about_myself_1": '',
            "about_myself_2": '',
            "city": extract_city(soup),
            "is_online": extract_is_online(soup),
        }


# !!!
        # Це скрапінг картки репетитора на сторінці самого екаунту
# !!!
    # Вдоскональ цю ф-цію!
def get_data_from_one_account(id_rep):
    # # Extract Data from a Single Account
    # tag_body = get_tag_body(id_rep)
    url = f"https://buki.com.ua/user-{id_rep}/"
    tag_body = get_tag_body(url)
    
    # # !!! Та це ж повторний зайвий виклик!
    # # У tag_body вже відбувся такий же виклик
    # fetch_url_with_retries(url, retries=3, timeout=10, return_soup=False)
    
    return {
            "about_myself_1": get_element(tag_body, "p.styles_mobileDescription__LxjZs"),
            "about_myself_2": get_element(tag_body, "p.styles_aboutMe__4uKLA"),
        }


def parse_tutors_page_buki(html):
    soup = BeautifulSoup(html, "html.parser")

    tutors = []
    
    tutor_cards = soup.select(".styles_container__4lrBa")
    for card in tutor_cards:
        current_card = parse_tutor_card_buki(str(card))
        tutors.append(current_card)

    return tutors


# # ---------------------------------
# # Site PROFREP
# def parse_tutor_card_profrep(html_card):
#     # Extract Data from a Single Tutor Card
#     # Саме в цій функції ми визначаємо усі ті дані, які хочемо дістати з кожної картки репетитора
#     soup = BeautifulSoup(html_card, 'html.parser')
#     return {
#             "name": safe_text(soup.select_one('div.card-courses-title'), "span"),            
#             "price": None,
#             "objects": None,
#             "rating": None,
#             "number_of_reviews": None,
#             "education": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(2)')),
#             "experience": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(1)')),
#             "about_myself": safe_text(soup.select_one('div.col-md-12.catalog-item-desc.mt-1 > p:nth-child(3)')),
#             "city_or_online": safe_text(soup.select_one('i.fa fa-map-marker-alt')),
#         }


# def parse_tutors_page_profrep(html):
#     soup = BeautifulSoup(html, "html.parser")

#     tutors = []
    
#     # tutor_cards = soup.select(".row > .col-lg-12.m-b30 > .widget-inner")
#     tutor_cards = soup.select(".widget-inner")
#     for card in tutor_cards:
#         current_card = parse_tutor_card_profrep(str(card))
#         tutors.append(current_card)

#     return tutors

# # Site PROFREP
# # THE END
# # =====================================


# def get_list_ids_tutors_on_page(num_page):
#     pass


# # !!!
# # Додай другий параметр: id_rep.
# # А потім, через if..else повертай відповідний tag_body
# def get_tag_body(num_page):
#     if num_page == 1:
#         url = "https://buki.com.ua/tutors/biolohiia"
#     else:
#         url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
#     soup, _ = fetch_url_with_retries(url, retries=3, timeout=10, return_soup=True)
#     # print(f'soup FROM get_tag_body: {soup}')
#     if soup is None:
#         print('Func get_tag_body returning None')
#         return None
#     tag_body = soup.select_one('body')
#     # print(f'tag_body FROM get_tag_body: {tag_body}')
#     return tag_body

def get_tag_body(url):
    # if num_page == 1:
    #     url = "https://buki.com.ua/tutors/biolohiia"
    # else:
    #     url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    soup, _ = fetch_url_with_retries(url, retries=3, timeout=10, return_soup=True)
    # print(f'soup FROM get_tag_body: {soup}')
    if soup is None:
        print('Func get_tag_body returning None')
        return None
    tag_body = soup.select_one('body')
    # print(f'tag_body FROM get_tag_body: {tag_body}')
    return tag_body
    

def get_max_pagination(soup_element):
    # print(f'soup_element == {soup_element}')
    return int( safe_text( soup_element.select(".styles_pagination__qGM14 div a")[-1] ) )


def get_tutor_urls(soup_elem):
    return soup_elem.select_one(".styles_userName__ltIVo a")["href"][6:-1]