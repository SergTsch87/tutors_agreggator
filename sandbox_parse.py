#!usr/bin/env python3

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

from tutors_app.utils import is_connected, get_file_path, timer_elapsed
from tutors_app.file_dir_sys import write_list_data_to_file
from tutors_app.scrap_logic import get_tag_body, get_max_pagination, get_tutor_urls, get_data_from_one_account #, get_element
from pathlib import Path
import logging


@timer_elapsed
def main():
    logging.basicConfig(
        filename=get_file_path('parser_errors.log'),
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode = 'a'   # Дозаписування нових записів до файлу
    )
# ================================
# Тестовий код для обходу усіх сторінок
#   
    # list_num_pages = [1, 10, 30, 50, 60, 90, 98]
    
    # Код для отримання найбільшого номера пагінації
    # ! Якщо такого номера нема, - тоді:
    # - відбувається редірект на 'https://buki.com.ua/tutors/biolohiia/'
    # - виходимо з циклу без збереження даних на поточній ітерації

# ---------------------

# 09.07.25
#     Task 1:
#         Взяти 20 ідентифікаторів → Зберегти їх у файл → Зібрати дані з відповідних URL-адрес → Повторити.
#         Зберіг - Обробив - Повторив

    # ! Розкоментуй, щойно будеш готовий запустити скрипт для збору УСІХ посилань
    # num_page = 1

    num_page = 97 # ! for test !

    if not is_connected():  # Якщо нема інтернет-зв'язку
        print('Error: No internet connection')
        return 'Error: No internet connection'

    tag_body = get_tag_body(num_page)
    max_num_pagination = get_max_pagination(tag_body)
    list_urls_tutors = []
    file_name = 'list_urls_tutors'
    file_path = f'{Path.cwd()}/bio/{file_name}.txt'

    while num_page <= max_num_pagination:

#         # ! Розкоментуй, щойно будеш готовий обробляти код сторінки з усіма її репетиторами
#         # # Тут буде збереження файлу: код сторінки з усіма її репетиторами

        # Якщо tutor_cards порожній — це може означати, що сторінка була редіректнута або порожня.
        # Логуй і пропускай таку сторінку.
        tag_body = get_tag_body(num_page)

        tutor_cards = tag_body.select(".styles_container__4lrBa")
        for card in tutor_cards:
            # # # Цей рядок потрібен під час витягання коду репетитора з БД чи файлу. А не навпаки(!)
            # # url_tutor = 'https://buki.com.ua' + card.select_one(".styles_userName__ltIVo a")["href"]
            # url_tutor = card.select_one(".styles_userName__ltIVo a")["href"][6:-1]
            url_tutor = get_tutor_urls(card)
            list_urls_tutors.append(url_tutor)

            # ! Розкоментуй, щойно будеш готовий обробляти код сторінки певного репетитора
            # html = get_html(url_tutor)
            # # Тут буде збереження файлу: код сторінки певного репетитора

        write_list_data_to_file(file_path, list_urls_tutors) # Зберіг
        # Можна й так ф-цію назвати:
        # save_ids_to_file(ids: list[int], filename: str)

        #  # Обробив:
            # Використовуючи ці 20 IDs, - витяг дані з сайту за 20-ю URL'ами
        # fetch_data_from_urls(ids: list[int]) -> list[dict]
        # process_batches(all_ids: list[int], batch_size: int = 20)

        for id_rep in list_urls_tutors:
            # Якщо екаунт не містить важливих даних, - тоді оминаємо його
            data_one_account = get_data_from_one_account(id_rep, list_urls_tutors)
            save_to_db(data_one_account)
        
        list_urls_tutors = []

        num_page += 1
        
        # THE END While Loop
    # ----------------------------
    
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