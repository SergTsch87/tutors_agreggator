#!usr/bin/env python3

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

from tutors_app.utils import is_connected, get_file_path, timer_elapsed
from tutors_app.file_dir_sys import write_list_data_to_file, save_to_file, delete_file, create_dir, create_empty_txt_file
from tutors_app.scrap_logic import get_tag_body, get_max_pagination, get_data_from_one_account, parse_tutor_card_buki #, get_element, get_tutor_urls
from pathlib import Path
import logging
import json


def create_dir_bio():
    subject_dir = Path('bio')
    current_directory = Path.cwd()
    dir_path_bio = f"{current_directory}/{subject_dir}/"
    create_dir(dir_path_bio)
    return dir_path_bio


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
    num_page = 1

    # num_page = 97 # ! for test !
        
    if not is_connected():  # Якщо нема інтернет-зв'язку
        print('Error: No internet connection')
        return 'Error: No internet connection'

# Creating file-dir structure

    # Створюємо папку 'bio'
    dir_path_bio = create_dir_bio()
        # subject_dir = Path('bio')
        # current_directory = Path.cwd()
        # dir_path_bio = f"{current_directory}/{subject_dir}/"
        # create_dir(dir_path_bio)

    tag_body_tmp = get_tag_body(num_page)  # '_tmp' - для того, щоб не заплутатись потім у циклі
    max_num_pagination = get_max_pagination(tag_body_tmp)
    
    # list_urls_tutors = []  # фактично, це - list_ids_tutors
    

    # # Це все можна закоментувати, - якщо я буду инакше обробляти цей список
    # file_name = 'list_urls_tutors'
    # # file_path = f'{Path.cwd()}/bio/{file_name}.txt'
    # file_path = f'{Path.cwd()}/bio/{file_name}.jsonl'


    # file_name_data = 'test'
    # file_path_data = f'{Path.cwd()}/bio/{file_name_data}.jsonl'

    # Tasks:
        # 1) Заміни .txt на .jsonl у всій file-dir структурі
        # 2) Перевір правильність збереження даних 20-ти екаунтів до .jsonl (з однієї сторінки)
        # 3) Перевір правильність збереження даних 20-ти екаунтів до .jsonl (з кількох сторінок)
        # 4) Запусти скрапер на збирання-збереження усіх даних з усіх сторінок

    while num_page <= max_num_pagination:

#         # ! Розкоментуй, щойно будеш готовий обробляти код сторінки з усіма її репетиторами
#         # # Тут буде збереження файлу: код сторінки з усіма її репетиторами

        dir_path_bio_num_page = f"{dir_path_bio}/{str(num_page)}"
        create_dir(dir_path_bio_num_page)
        file_path_data = f'{dir_path_bio_num_page}/{num_page}.jsonl'
        create_empty_txt_file(file_path_data)  # json даних з усіх анкет репетиторів за адресою f'/{num_page}/'
        
        # # !!!
        # # А це для чого?!
        # file_name_data = f'{num_page}.jsonl'
        # # file_path_20_repetitors = f'{Path.cwd()}/bio/{file_name_data}.jsonl'
        # file_path_20_repetitors = f'{dir_path_bio_num_page}/{file_name_data}.jsonl'

        # Якщо tutor_cards порожній — це може означати, що сторінка була редіректнута або порожня.
        # Логуй і пропускай таку сторінку.
        tag_body = get_tag_body(num_page)

        list_tutors_data = [] # список словників з даними усіх репетиторів (макс. = 20) на сторінці

        tutor_cards = tag_body.select(".styles_container__4lrBa")  # list of card elements
        for card in tutor_cards:
            # # # Цей рядок потрібен під час витягання коду репетитора з БД чи файлу. А не навпаки(!)
            # # url_tutor = 'https://buki.com.ua' + card.select_one(".styles_userName__ltIVo a")["href"]
            # url_tutor = card.select_one(".styles_userName__ltIVo a")["href"][6:-1]
            
            # Дістали дані репетитора із загальної сторінки
            dict_current_card = parse_tutor_card_buki(str(card))
            
            
            # !!!
            # Коли опрацюєш усі збереження даних, - тоді розкоментуй ці рядки!
            # # оминаємо порожні анкети
            # if ( dict_current_card['price'] is None ) and ( dict_current_card['about_myself'] is None ):
            # # is none or is null ?..
            #     continue
            
            
            list_tutors_data.append(dict_current_card)  #  list of dicts - список усіх даних про репетиторів

            # url_tutor = dict_current_card['id_tutor']

            # ! Нащо на ходу збирати списки chunks_urls | ids  репетиторів, коли вони вже є у списку list_tutors_data ?!..
            # url_tutor = get_tutor_urls(card)  !!! А це ж тоді зайва ф-ція
            # list_urls_tutors.append(url_tutor)  # список chunks_urls | ids  репетиторів

            # ! Розкоментуй, щойно будеш готовий обробляти код сторінки певного репетитора
            # html = get_html(url_tutor)
            # # Тут буде збереження файлу: код сторінки певного репетитора

        # Зберіг дані 20-ти репетиторів із загальної сторінки
        write_list_data_to_file(file_path_data, list_tutors_data)

        # write_list_data_to_file(file_path_data, list_tutors_data)

        # # !!! Це, мабуть, зайвий рядок коду
        # write_list_data_to_file(file_path, list_urls_tutors)
        
        # Можна й так ф-цію назвати:
        # save_ids_to_file(ids: list[int], filename: str)

        #  # Обробив:
            # Використовуючи ці 20 IDs, - витяг дані з сайту за 20-ю URL'ами
        # fetch_data_from_urls(ids: list[int]) -> list[dict]
        # process_batches(all_ids: list[int], batch_size: int = 20)

        # !!!
        # Зі списку list_tutors_data витягаємо "id_tutor" кожного репетитора
        list_urls_tutors = [dict_tutor_data['id_tutor'] for dict_tutor_data in list_tutors_data]
        
        # # Далі заходимо на сторінки анкет репетиторів, та витягаємо з кожної розділи "about_myself_1" та "about_myself_2"
        # ??? list_urls_tutors = [dict_tutor_data['about_myself_1'] + '>]\/[<' + dict_tutor_data['about_myself_2'] for dict_tutor_data in list_tutors_data]
        # За цим рядком '>]\/[<' потім будемо ділити ці два about's
        
        # ! list_data_one_account - це буде список словників з двома ключами: "about_myself_1" та "about_myself_2"
        list_data_one_account = []
        
        for about_data_rep in list_urls_tutors:
            # Якщо екаунт не містить важливих даних, - тоді оминаємо його
            
            # Тут відбувається звернення до сайту
            list_data_one_account.append( get_data_from_one_account(about_data_rep) )

            # Слід дописати дані 'about' до вже існуючого jsonl-файлу
            # Напиши таку ф-цію

            # save_to_file(data_one_account) # creating and saving to jsonl-files
            
            # Це вже зайве, бо структури з txt-файлами вже не буде
            # # delete_file(file_path) # del all txt-files
            
        # list_urls_tutors = []

        # ! Дістаємо дані 20-ти репетиторів із загальної сторінки
        data_tutors = []
        with open(file_path_data, "r", encoding='utf-8') as jsonFile:
            for line in jsonFile:
                try:
                    json_object = json.loads(line)
                    data_tutors.append(json_object)
                except json.JSONDecodeError as e:
                    print(f'Error decoding JSON on line: {line.strip()} - {e}')
                    continue # skip invalid lines and continue processing

        # # ! for test
        # for item in data_tutors:
        #     print(item)

        # Додаємо текст з анкети репетитора до списку даних
        for index, one_tutor in enumerate(data_tutors):
            one_tutor['about_myself_1'] = list_data_one_account[index]['about_myself_1']
            one_tutor['about_myself_2'] = list_data_one_account[index]['about_myself_2']
        
        # Зберігаємо файл з оновленими даними
        with open(file_path_data, "w") as jsonFile:
            for item in data_tutors:
                json.dump(item, jsonFile)
                jsonFile.write('\n')


        num_page += 1
        
        # THE END While Loop
    # ----------------------------
    
    # list_urls_tutors = []

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
    # # list_tutors_data = parse_tutors_page_buki(html)


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