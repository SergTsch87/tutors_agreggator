import requests
from bs4 import BeautifulSoup
from tutors_app.utils import parse_price, get_num_of_reviews
from pathlib import Path
# import zlib
# from lorem_text import lorem  #  for insert text 'dolorem ipsum')


def get_html(url: str):
    try:
        response = requests.get(url, allow_redirects=False)
        if 300 <= response.status_code < 400:  #  ! 301 or 302 (redirect)
            # soup = BeautifulSoup(response.text, 'html.parser')
            # body_tag = soup.select_one('body')
            # return body_tag, 1 # 'redirect'
            return response.text, 1 # 'redirect'
        else:
            return response.text, 0 # 'No redirect'
    except requests.exceptions.RequestException as e:
        print(f'An error occured: {e}')


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

def parse_tutor_card_buki(html_card):
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

# ---------------------------------
# def make_multiplier(factor):
#     def multiply(x):
#         return x * factor
#     return multiply
# ---------------------------------

# ========================================
# Створення структури папок для пришвидшення розробки веб-скрапера

def create_dir(dir_path):
    '''
    dir_path == "my_documents/reports"
    Create a directory:
        Create a Path object and then use its mkdir() method.
        Set "parents=True" to create any missing parent directories,
        and "exist_ok=True" to avoid an error if the directory already exists.
    '''
    dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    # print(f"Folder '{dir_path}' created successfully (or already exists).") # for test


# def get_list_ids_tutors_on_page(num_page):
#     pass

def create_empty_txt_file(file_name):
    with open(file_name, 'w'):
        pass
    # print(f"File '{file_name}' created successfully") # for test


def create_file_dir_structure(subject):
    current_directory = Path.cwd()
    dir_path = f"{current_directory}/{subject}/"
    create_dir(dir_path)
    for num_page_dir in range(1, 8):
        dir_path_num_page = f"{dir_path}/{str(num_page_dir)}"
        create_dir(dir_path_num_page)
        create_empty_txt_file(f'{dir_path_num_page}/{num_page_dir}.txt') # html-код за адресою f'/{num_page_dir}/' - для подальшого зберігання списку репетиторів на певній сторінці
        for id_tutor_dir in range( 1 + 20 * ( num_page_dir - 1), 1 + 20 * num_page_dir ):
            path_id_tutor_dir = f'{dir_path_num_page}/{str(id_tutor_dir)}'
            create_dir(f'{path_id_tutor_dir}')
            create_empty_txt_file(f'{path_id_tutor_dir}/{id_tutor_dir}.txt') # html-код за адресою f'/{num_page_dir}/{id_tutor_dir}/'
  
        # list_ids_tutors_on_page = get_list_ids_tutors_on_page(num_page_dir)
        # for id_tutor_dir in list_ids_tutors_on_page:
        #     create_dir(dir_path + '/' + str(num_page_dir) + '/' + str(id_tutor_dir))
        #     # create_empty_txt_file() # html-код за адресою f'/{num_page_dir}/{id_tutor_dir}/'


def create_and_info_dir(category_name): # is_exist_dir()
    subject_dir = Path('bio')
    # return subject_dir.exists()

    if not subject_dir.exists():
        create_file_dir_structure(subject_dir)
        print('Такої папки нема, тому Створено задану структуру папок')
    else:
        print('Така папка вже існує!')

# --------------------------------------------------
def get_count_lines_file(file_path):
    with open(file_path, 'r') as file:
        line_count = 0
        for count, _ in enumerate(file):
            line_count = count + 1
        # line_count = count + 1 if count is not None else 0 # Handle empty files
    return line_count


def writing_html_to_file(num_page, file_name):
    url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    html, _ = get_html(url)
    file_path = f'{Path.cwd()}/bio/{num_page}/{file_name}/{file_name}.txt'

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html)
        print(f"Succesfully wrote large text in chunks to {file_path}")

    except IOError as e:
        print(f'Error writing to file: {e}')


def rename_txt_file(old_file_name, new_file_name):
    old_file_path = Path(f'{Path.cwd()}/bio/{old_file_name}.txt')
    new_file_path = Path(f'{Path.cwd()}/bio/{new_file_name}.txt')
    
    if old_file_path.exists():
        old_file_path.rename(new_file_path)
    else:
        print(f'Не існує файлу {old_file_name}.txt!')

# ========================================

# def get_html_by_page_number(num_page):
#     url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
#     html, is_redirect = get_html(url)
#     return html, is_redirect


def write_list_data_to_file(file_path, list_data, mode='a'):
    '''
        mode == 'a' or 'w'
    '''
    with open(file_path, mode, encoding='utf-8') as file:
        file.write('\n' + '\n'.join(list_data))


def main():


# ================================
# Тестовий код для обходу усіх сторінок
#   
    # list_num_pages = [1, 10, 30, 50, 60, 90, 98]
    
    # Код для отримання найбільшого номера пагінації
    # ! Якщо такого номера нема, - тоді:
    # - відбувається редірект на 'https://buki.com.ua/tutors/biolohiia/'
    # - виходимо з циклу без збереження даних на поточній ітерації

# ---------------------
# !!!
# get Error
#
# Traceback (most recent call last):
#   File "g:\Windows\Meni\Work\Python\Lessons Python\tutor_dj_scrap\sandbox_parse.py", line 428, in <module>
#     main()
#   File "g:\Windows\Meni\Work\Python\Lessons Python\tutor_dj_scrap\sandbox_parse.py", line 255, in main    
#     max_num_pagination = int( safe_text( soup.select_one("span.styles_separator__aFEYQ.next_sibling") ) ) 
#                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
# ValueError: invalid literal for int() with base 10: 'N/A'
# ---------------------

    # ! Розкоментуй, щойно будеш готовий запустити скрипт для збору УСІХ посилань
    # num_page = 1
    num_page = 97 # ! for test !
    
    url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    html, _ = get_html(url)
    # html, _ = get_html_by_page_number(num_page)
    soup = BeautifulSoup(html, 'html.parser')
    tag_body = soup.select_one('body')

    # А що, якщо перед циклом виставити фіктивне ( >> num_page ) значення, яке точно не буде на цьому сайті, а вже у циклі витягти з сайту його справжнє значення?..
    max_num_pagination = int( safe_text( tag_body.select(".styles_pagination__qGM14 div a")[-1] ) )
    # print(f'max_num_pagination == {max_num_pagination}')
    list_urls_tutors = []
    file_name = 'list_urls_tutors'
    file_path = f'{Path.cwd()}/bio/{file_name}.txt'

    while True:
    # То, може таку умову для циклу зробити?..
    # while num_page <= max_num_pagination:
    # Тоді доведеться залишити ініц-цію max_num_pagination перед циклом...

        # !!!
        # А може, max_num_pagination створити тут?..
        # Тоді не потрібна буде ініціалізація tag_body перед циклом
        # if max_num_pagination is_not_int:
        #     all code follow

        # if ( num_page > max_num_pagination ) or ( link_rel_next is None ):
        # if ( num_page > max_num_pagination ) or ( link_rel_next['rel'] == 'prev' ):
        if ( num_page > max_num_pagination ):
            print(f'num_page > max_num_pagination  =>  {num_page} > {max_num_pagination}  =>  {num_page > max_num_pagination}')
            break

        url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
        html, is_redirect = get_html(url)
        # html, is_redirect = get_html_by_page_number(num_page)

        # ! Якщо це дійсно зайві коди, - тоді доведеться всюди прибрати перевірку на редірект
        # ! Це мабуть вже зайвий код...
        if is_redirect:
            print(f'is_redirect == {is_redirect}')
            break
        # ! ...і це зайвий код
        # # 'no tutor cards are found on the page' - як це перевірити, якщо є редірект?

        # ! Розкоментуй, щойно будеш готовий обробляти код сторінки з усіма її репетиторами
        # # Тут буде збереження файлу: код сторінки з усіма її репетиторами

        # Збереження списку нових 20 URLs репетиторів
        if len(list_urls_tutors) == 20:
            # Зберігаємо кожні 20 нових адрес зі списку репетиторів 
            print(f'list_urls_tutors: {list_urls_tutors}')
            write_list_data_to_file(file_path, list_urls_tutors)
            # with open(file_path, 'a', encoding='utf-8') as file:
            #     file.write('\n' + '\n'.join(list_urls_tutors))
            print(f'Insert list list_urls_tutors to file {file_path}:\n{list_urls_tutors}')
            
            list_urls_tutors = []

        # !!!
        # Якщо tutor_cards порожній — це може означати,
        # що сторінка була редіректнута або порожня.
        # Логуй і пропускай таку сторінку.
        tutor_cards = tag_body.select(".styles_container__4lrBa")
        for card in tutor_cards:
            url_tutor = 'https://buki.com.ua/' + card.select_one(".styles_userName__ltIVo a")["href"]
            list_urls_tutors.append(url_tutor)

            # ! Розкоментуй, щойно будеш готовий обробляти код сторінки певного репетитора
            # html = get_html(url_tutor)
            # # Тут буде збереження файлу: код сторінки певного репетитора

        num_page += 1
        url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
        html, _ = get_html(url)
        # html, _ = get_html_by_page_number(num_page)
        soup = BeautifulSoup(html, 'html.parser')
        tag_body = soup.select_one('body')
        
        # THE END While Loop
    # ----------------------------
    
    # Зберігаємо крайній залишок репетиторів
    # Напр.: є 1012 репетиторів. Тепер збережуться крайні 12 URLs)
    write_list_data_to_file(file_path, list_urls_tutors)
    # with open(file_path, 'a', encoding='utf-8') as file:
    #     file.write('\n' + '\n'.join(list_urls_tutors))
    print(f'Insert list list_urls_tutors to file {file_path}:\n{list_urls_tutors}')

    list_urls_tutors = []

# ================================================

    # !!! Already work!
    # category_name = 'bio'
    # create_and_info_dir(category_name)

    # num_page = 5
    # file_name = '84'
    # writing_html_to_file(num_page, file_name)

    # old_file_name = 'file1'
    # new_file_name = 'file2'
    # rename_txt_file(old_file_name, new_file_name)

    # large_str = lorem.paragraph() * 10
    # print(f'large_str: {large_str}\n')
    # print(f'Compress large_str: {zlib.compress(large_str.encode('utf-8'))}')


    # line_count = get_count_lines_file(file_name)
    # print(f'line_count == {line_count}')
    # print(f'len(html) == {len(html)}')
    
    # num_chunks = get_count_lines(html) # 10000

    # try:
    #     with open(file_name, 'w', encoding='utf-8') as f:
    #         # f.write(html)
    #         for chunk in generate_large_text_chunks(num_chunks, html):
    #             f.write(chunk)
    #     print(f"Succesfully wrote large text in chunks to {file_name}")

    # except IOError as e:
    #     print(f'Error writing to file: {e}')

    # with open(file_name, 'w', encoding='utf-8') as f:
    #     f.write(html)

# ================================
# Тестовий код для обмеженої к-сти сторінок та фалів
#     
    # num_page = 5
    # url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    # html = get_html(url)
    # # tutors_data = parse_tutors_page_buki(html)


    # list_num_pages = [1, 10, 30, 50, 60, 90, 98]
    # for num_page in list_num_pages:
    #     url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    #     html = get_html(url)
    #     soup = BeautifulSoup(html, "html.parser")

    #     # Тут буде збереження файлу: код сторінки з усіма її репетиторами

    #     tutor_cards = soup.select(".styles_container__4lrBa")
    #     for card in tutor_cards:
    #         soup = BeautifulSoup(card, 'html.parser') # А точно цей рядок коду тут потрібен? Хіба не достатньо замість 'soup' просто залишити 'card'?..
    #         url_tutor = 'https://buki.com.ua/' + soup.select_one(".styles_userName__ltIVo a")["href"],

    #         html = get_html(url_tutor)
        
    #         # Тут буде збереження файлу: код сторінки певного репетитора

# ================================================

    # url = "https://buki.com.ua/tutors-online/biolohiia/3/"
    # html = get_html(url)
    # soup = BeautifulSoup(html, 'html.parser')
    # # print( get_element(soup, ".styles_userName__ltIVo a")["href"] )
    # print( get_element(soup, ".styles_userName__ltIVo a[href]") )
    # print( soup.select_one(".styles_userName__ltIVo a")["href"] )


    # num_page = 5
    # url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
    # html = get_html(url)
    # data = parse_tutors_page_buki(html)

    # # url = "https://profrepetitor.com.ua/repetitors-biologiya"
    # # html = get_html(url)
    # # # print(f'\nsize(html): {len(html)}\n')
    # # data = parse_tutors_page_profrep(html)
    # # # print(f'\nCount elements of data: {len(data)}\n')

    # for tutor in data:
    #     # print(f"ID Tutor: {tutor['id_tutor']}, Tutor name: {tutor['name']},  Price: {tutor['price']},  Objects: {tutor['objects']}, Rating: {tutor['rating']}, Number of reviews: {tutor['number_of_reviews']}, Education: {tutor['education']}, Experience: {tutor['experience']}, about_myself: {tutor['about_myself']}, city_or_online: {tutor['city_or_online']}")
    #     print(f"ID Tutor: {tutor['id_tutor']}")

    #     # print(f"Tutor name: {tutor['name']},  Price: {parse_price(tutor['price'])},  Objects: {tutor['objects']}, Rating: {tutor['rating']}, Number of reviews: {tutor['number_of_reviews']}, Education: {tutor['education']}, Experience: {tutor['experience']}, about_myself: {tutor['about_myself']}, city_or_online: {tutor['city_or_online']}")


    # parse_example()
    # pass


    # html_str = "<p class='styles_education__41VXk'>Освіта: <span>Запорізький державний медичний університет (ЗДМУ)</span></p>"
    # soup_elem = BeautifulSoup(html_str, "html.parser")
    
    # education = soup_elem.find('p', class_="styles_education__41VXk")
    # print(f"education = {education.get_text(strip=True)}")
    # print(f"education = {education}")


if __name__ == "__main__":
    main()