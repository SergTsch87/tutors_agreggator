#!usr/bin/env python3

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

from tutors_app.utils import is_connected, get_file_path, timer_elapsed
from tutors_app.file_dir_sys import write_list_data_to_file, create_dir, create_empty_txt_file, create_dir_bio # create_file_dir_structure, save_to_file, delete_file
from tutors_app.scrap_logic import correct_url, is_there_next_page, get_tag_body, get_max_pagination, get_data_from_one_account, parse_tutor_card_buki #, get_element, get_tutor_urls
from pathlib import Path
import logging
import json
from collections import Counter
import os
import math


def get_freq_dict(my_list):
    return Counter(my_list)


def get_hist_prices(data_prices: list, freq_dict) -> dict:
    min_price = min(data_prices) # 150
    max_price = max(data_prices) # 1000
    width_bin = 50
    count_bins = math.ceil( ( max_price - min_price ) / width_bin ) + 1

    # Initial...
    hist_dict = {}

    # Range of each bins:
    min_bin = min_price

    # ... and create hist_dict
    for _ in range( count_bins ):
        hist_dict[min_bin] = 0  # [ min_bin..max_bin ]
        min_bin += width_bin
    print(f'Empty hist_dict: {hist_dict}')

    # # Reading freq dict of prices ( freq_dict ) from freq_dict_prices.json
    # file_path_data = f'{dir_path_bio}/freq_dict_prices.json'
    # file_path_data = Path(file_path_data)
    # with open(file_path_data, "r") as json_file:
    #     freq_dict = json.loads(json_file.read())

    # Заповнення hist_dict
    for price_str, count in freq_dict.items():
        price = int(price_str)
        bin_key = price - ( price % width_bin )
        if bin_key in hist_dict:
            hist_dict[bin_key] += count

    print(f'Follow hist_dict: {hist_dict}')

    return hist_dict



        # # Writing freq_dict_prices to file
        # current_directory = Path.cwd()
        # subject_dir = Path('bio')
        # dir_path_bio = f"{current_directory}/{subject_dir}/"
        # # freq_dict_prices = get_freq_dict(data_prices)
        # # print(f'freq_dict_prices == {freq_dict_prices}')
        # # # print(f'freq_dict_prices == {list(freq_dict_prices)}')
        # file_path_data = f'{dir_path_bio}/hist_dict_prices.json'
        # file_path_data = Path(file_path_data)
        # # write_list_data_to_file(file_path_data, list(freq_dict_prices), 'w')
        # with open(file_path_data, "w") as json_file:
        #     json.dump(hist_dict, json_file, indent=4, sort_keys=True)



    # while ...:
    #     if freq_dict[key] < hist_dict[f'{min_bin}']:
    #         hist_dict[f'{min_bin}'] += freq_dict[key]

    # for key, val in hist_dict:
    #     if int(key) < max_bin:
    #         hist_dict[f'{min_bin}'] += val

    # # freq_dict.sort()

    


# how to round to nearest 50 in python
# 50 * round(number / 50)
# 50 * math.ceil(number / 50)
    
    # for num in data_prices:
    #     if num in hist_dict:
    #         hist_dict[f'{min_bin}'] += 1
    #     else:
    #         hist_dict[f'{min_bin}'] = 1

    #     min_bin = min_price + width_bin
    #     max_bin = min_bin + width_bin

# ---------------------



# def find_folder_in_current_dir(target_name):
#     """
#     Знаходить папку з певною назвою в поточному каталозі.

#     Args:
#         target_name: Назва папки, яку потрібно знайти.

#     Returns:
#         Повний шлях до папки, якщо знайдено, інакше None.
#     """
#     for item in os.listdir("."):
#         item_path = os.path.join(".", item)
#         if os.path.isdir(item_path) and item == target_name:
#             return item_path
#     return None


def count_subdirectories(directory_path):
    """
    Counts the number of subdirectories directly within a given directory.

    Args:
        directory_path (str): The path to the directory to examine.

    Returns:
        int: The number of subdirectories found.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        return 0

    # os.walk yields a 3-tuple: (dirpath, dirnames, filenames)
    # The first element returned by next(os.walk(...)) will contain the
    # dirnames (subdirectories) of the top-level directory.
    try:
        _, dirnames, _ = next(os.walk(directory_path))
        return len(dirnames)
    except StopIteration:
        # This can happen if the directory_path itself is empty or not accessible
        return 0


@timer_elapsed
def main():
    logging.basicConfig(
        filename=get_file_path('parser_errors.log'),
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode = 'a'   # Дозаписування нових записів до файлу
    )
# ================================
    
    # Код для отримання найбільшого номера пагінації
    # ! Якщо такого номера нема, - тоді:
    # - відбувається редірект на 'https://buki.com.ua/tutors/biolohiia/'
    # - виходимо з циклу без збереження даних на поточній ітерації

# ---------------------

    # num_page = 1
    num_page = 10
        
    if not is_connected():  # Якщо нема інтернет-зв'язку
        print('Error: No internet connection')
        return 'Error: No internet connection'
    
# -------------------
    subject_dir = Path('bio')
    
    if subject_dir.exists():
        print('Така папка вже існує!')



    #     # if found_path:
    #     #     print(f"Папку знайдено за шляхом: {found_path}")
    #     # else:
    #     #     print(f"Папку з назвою '{folder_name}' не знайдено.")

    #     # max_num = find_folder_in_current_dir(subject_dir) + 1

        current_directory = Path.cwd()
        dir_path_bio = f"{current_directory}/{subject_dir}/"

        file_path_data = f'{dir_path_bio}/bio_data.jsonl'
        file_path_data = Path(file_path_data)

        if file_path_data.is_file():
    # # ============= Витягаю дані для створення freq_dict_prices =======
    #     #     # file_path_data = f'{dir_path_bio}/bio_data.jsonl'
    #     #     data_prices = []
            
    #     #     # Reading bio_data.jsonl for extract data_prices list with all data
    #     #     with open(file_path_data, "r", encoding='utf-8') as jsonFile:
    #     #         for line in jsonFile:
    #     #             try:
    #     #                 json_object = json.loads(line)
    #     #                 data_prices.append(json_object['price'])
    #     #             except json.JSONDecodeError as e:
            
    #     #                 print(f'Error decoding JSON on line: {line.strip()} - {e}')
    #     #                 continue # skip invalid lines and continue processing

    #     # # Writing prices to prices.json
    #         file_path_data = f'{dir_path_bio}/prices.json'
    #         file_path_data = Path(file_path_data)
    #     #     # write_list_data_to_file(file_path_data, data_prices, 'w')
    #     #     with open(file_path_data, "w") as json_file:
    #     #         json.dump(data_prices, json_file)

    #     # Reading list of prices ( data_prices ) from prices.json
    #         try:
    #             data_prices = []
    #             with open(file_path_data, "r", encoding='utf-8') as jsonFile:
    #                 try:
    #                     # data_prices = json.loads(jsonFile.read()) # Це дозволить правильно прочитати ціле вміст файлу як рядок, а потім розпарсити його як JSON.
    #                     data_prices = json.load(jsonFile) # Це дозволить правильно прочитати ціле вміст файлу як рядок, а потім розпарсити його як JSON.
    #                     # print(f'data_prices == {data_prices}')
    #                 except json.JSONDecodeError as e:                
    #                     print(f'Error decoding JSON: {e}')
    #         except FileNotFoundError:
    #             print("Error: 'prices.json' not found")
    #         except json.JSONDecodeError:
    #             print("Error: Could not decode JSON from 'prices.json'")

        # Reading freq dict of prices ( freq_dict ) from freq_dict_prices.json
            file_path_data = f'{dir_path_bio}/freq_dict_prices.json'
            file_path_data = Path(file_path_data)
            print('Reading freq dict of prices ( freq_dict ) from freq_dict_prices.json')
            # write_list_data_to_file(file_path_data, list(hist_prices), 'w')
            with open(file_path_data, "r") as json_file:
                freq_dict = json.loads(json_file.read())
                # json.load(freq_dict, json_file, indent=4, sort_keys=True)

                avg_sum = 0
                numerator = 0
                denominator = 0
                for price_str, count in freq_dict.items():
                    numerator += int(price_str) * count
                    denominator += count
                    
                avg_sum = numerator / denominator
                print(f'avg_sum == {avg_sum}')
    #         print(f'freq_dict == {freq_dict}')

    #         file_path_data = f'{dir_path_bio}/hist_prices.json'
    #         file_path_data = Path(file_path_data)            


# ============= Витягаю дані для створення dict_expieriens_by_prices_category: dict_exprs_by_prices_cat =======
            file_path_data = f'{dir_path_bio}/bio_data.jsonl'
            dict_exprs_by_prices_cat = {}
                # int( id_tutor )
                # price
                # int( experience )
            list_dicts_exprs_by_prices_cat = []
            
            # Reading bio_data.jsonl for extract dict_exprs_by_prices_cat list with all data
            with open(file_path_data, "r", encoding='utf-8') as jsonFile:
                for line in jsonFile:
                    try:
                        json_object = json.loads(line.strip())
                        # Нас не цікавлять дані без ціни або без років досвіду
                        if json_object['price'] and json_object['experience']:
                            dict_exprs_by_prices_cat = {
                                'id_tutor': int( json_object['id_tutor'] ),
                                'price': json_object['price'],
                                'experience': int( json_object['experience'] )
                            }
                            list_dicts_exprs_by_prices_cat.append(dict_exprs_by_prices_cat)
                    except json.JSONDecodeError as e:
            
                        print(f'Error decoding JSON on line: {line.strip()} - {e}')
                        continue # skip invalid lines and continue processing

    # Дописав список даних до файлу exprs_by_prices_cat.jsonl
                file_path_data = f'{dir_path_bio}/exprs_by_prices_cat.jsonl'
                # write_list_data_to_file(file_path_data, list_dicts_exprs_by_prices_cat, 'a')
                with open(file_path_data, "w") as json_file:
                    # json.dump(list_dicts_exprs_by_prices_cat, json_file, indent=4, sort_keys=True)
                    json.dump(list_dicts_exprs_by_prices_cat, json_file, indent=4)
                print(f'Writing data from {file_path_data}')




    #     # Forming hist_prices of dict
    #         # print(f'data_prices == {data_prices}')
    #         hist_prices = get_hist_prices(data_prices, freq_dict)
    #         # print(f'hist_prices == {hist_prices}')
    #         # print(f'hist_prices == {list(hist_prices)}')

    #     # Writing hist_prices to hist_prices.json
    #         # write_list_data_to_file(file_path_data, list(hist_prices), 'w')
    #         with open(file_path_data, "w") as json_file:
    #             json.dump(hist_prices, json_file, indent=4, sort_keys=True)

    #     # # Writing freq_dict_prices to file
    #     #     freq_dict_prices = get_freq_dict(data_prices)
    #     #     print(f'freq_dict_prices == {freq_dict_prices}')
    #     #     # print(f'freq_dict_prices == {list(freq_dict_prices)}')
    #     #     file_path_data = f'{dir_path_bio}/freq_dict_prices.json'
    #     #     file_path_data = Path(file_path_data)
    #     #     # write_list_data_to_file(file_path_data, list(freq_dict_prices), 'w')
    #     #     with open(file_path_data, "w") as json_file:
    #     #         json.dump(freq_dict_prices, json_file, indent=4, sort_keys=True)
        
        else:
    # ============= Transferred all data from a hundred files to a single file, in two cycles =======
    # === BEGIN ===

            # Example usage:
            target_directory = dir_path_bio
            num_folders = count_subdirectories(target_directory)
            print(f"Number of folders in '{target_directory}': {num_folders}")

            # list_tutors_data = [] # список словників з даними усіх репетиторів (макс. = 20) на сторінці
            
            # Отримати список усіх файлів
            num_page = 1
            dir_path_bio_num_page = f"{dir_path_bio}/{str(num_page)}"
            dir_path_bio_num_page = Path(dir_path_bio_num_page)
            list_file_pathes = []

            print('Begin WHILE loop...')
            # while dir_path_bio_num_page.exists():
            while dir_path_bio_num_page.is_dir():
                file_path_data = f'{dir_path_bio_num_page}/{num_page}.jsonl'
                list_file_pathes.append(file_path_data)
                print(num_page)
                
                num_page += 1
                dir_path_bio_num_page = f"{dir_path_bio}/{str(num_page)}"
                dir_path_bio_num_page = Path(dir_path_bio_num_page)

            print('THE END while loop...')
            print('Begin FOR loop...')

            # Тут буде цикл обходу усіх папок
            for file_path in list_file_pathes:

            # ! Дістаємо дані 20-ти репетиторів із загальної сторінки
                data_tutors = []
                with open(file_path, "r", encoding='utf-8') as jsonFile:
                    for line in jsonFile:
                        try:
                            json_object = json.loads(line)
                            data_tutors.append(json_object)
                        except json.JSONDecodeError as e:
                            print(f'Error decoding JSON on line: {line.strip()} - {e}')
                            continue # skip invalid lines and continue processing

            # Дописав список даних до файлу bio_data.jsonl
                file_path_data = f'{dir_path_bio}/bio_data.jsonl'
                write_list_data_to_file(file_path_data, data_tutors, 'a')
                print(f'Writing data from {file_path}')

            print('THE END for loop...')
    # === THE END ===

    else:
        print('Такої папки нема, тому Створено задану структуру папок')
# -------------------
    # === BEGIN else ===

    # Creating file-dir structure
        # Створюємо папку 'bio'
        dir_path_bio = create_dir_bio()
        # tag_body_tmp = get_tag_body(num_page)  # '_tmp' - для того, щоб не заплутатись потім у циклі
        url_upd = correct_url(num_page)
        tag_body_tmp = get_tag_body(url_upd)
        # print(f'\ntag_body_tmp: {tag_body_tmp}\n')
        max_num_pagination = get_max_pagination(tag_body_tmp)
        
        print(f'\nmax_num_pagination: {max_num_pagination}\n')

        num_page = max_num_pagination # - 10 # ! for test !
        # num_page = 2
        
        # Tasks:
            # 2) Перевір правильність збереження даних 20-ти екаунтів до .jsonl (з однієї сторінки)
            # 3) Перевір правильність збереження даних 20-ти екаунтів до .jsonl (з кількох сторінок)
            # 4) Запусти скрапер на збирання-збереження усіх даних з усіх сторінок

        # while num_page <= 3: # for test  # max_num_pagination:
        while num_page <= max_num_pagination:

    # ========= Ініціалізація пар-рів + створення '/bio/1.jsonl' =============
        # === BEGIN ===
            min_num_pagination = int( max_num_pagination * 0.7 )
            # # ! Тут відбувається звернення до сайту
            # tag_body = get_tag_body(num_page)
            url_upd = correct_url(num_page)
            tag_body = get_tag_body(url_upd)

            if ( num_page >= min_num_pagination and num_page < max_num_pagination ) and not is_there_next_page(tag_body):
                break

            dir_path_bio_num_page = f"{dir_path_bio}/{str(num_page)}"
            create_dir(dir_path_bio_num_page)
            file_path_data = f'{dir_path_bio_num_page}/{num_page}.jsonl'
            create_empty_txt_file(file_path_data)  # створює порожній jsonl-файл
            # json даних з усіх анкет репетиторів за адресою f'/{num_page}/'

            # # Перевірку на відсутність мережі краще зробити декоратором
            # if not is_connected():  # Якщо нема інтернет-зв'язку
            #     print('Error: No internet connection')
            #     return 'Error: No internet connection'
            
            # # # ! Тут відбувається звернення до сайту
            # # tag_body = get_tag_body(num_page)
            # url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/"
            # tag_body = get_tag_body(url)

            list_tutors_data = [] # список словників з даними усіх репетиторів (макс. = 20) на сторінці
        # === THE END ===

    # ========= Збирання та зберігання даних 20-ти репетиторів із загальної сторінки, до файлу =============
        # === BEGIN ===
            tutor_cards = tag_body.select(".styles_container__4lrBa")  # list of card elements
            
            # if tutor_cards == []: # ми дійшли до останньої сторінки пагінації
            #     logging()
            #     break
            
            for card in tutor_cards:
            # for card in tutor_cards[1:3]: # for test
                # Дістали дані репетитора із загальної сторінки
                dict_current_card = parse_tutor_card_buki(str(card))
                
                # !!!
                # Коли опрацюєш усі збереження даних, - тоді розкоментуй ці рядки!
                # # оминаємо порожні анкети
                # if ( dict_current_card['price'] is None ) and ( dict_current_card['about_myself'] is None ):
                # # is none or is null ?..
                #     continue
                
                list_tutors_data.append(dict_current_card)  #  list of dicts - список усіх даних про репетиторів
            
            # Зберіг дані 20-ти репетиторів із загальної сторінки
            write_list_data_to_file(file_path_data, list_tutors_data)
            # Можна й так ф-цію назвати:
            # save_ids_to_file(ids: list[int], filename: str)
        # === THE END ===
        
    # ========= Збираємо дані ("about_myself_1" та "about_myself_2") зі сторінок кожного з 20-ти репетиторів =============
        # === BEGIN ===

            # !!! Зі списку list_tutors_data витягаємо "id_tutor" кожного репетитора
            list_urls_tutors = [dict_tutor_data['id_tutor'] for dict_tutor_data in list_tutors_data]
            
            # ! list_data_one_account - це буде список словників з двома ключами: "about_myself_1" та "about_myself_2"
            list_data_one_account = []
            
            for id_rep in list_urls_tutors:
                # Якщо екаунт не містить важливих даних, - тоді оминаємо його
                
                # ! Тут відбувається звернення до сайту
                list_data_one_account.append( get_data_from_one_account(id_rep) )

                # save_to_file(data_one_account) # creating and saving to jsonl-files
        # === THE END ===

    # ========= Збираємо дані ("about_myself_1" та "about_myself_2") зі сторінок кожного з 20-ти репетиторів =============
        # === BEGIN ===
        #     Дістаємо дані 20-ти репетиторів із загальної сторінки    
        #     Додаємо текст з анкети репетитора до списку даних
        #     Зберігаємо до файлу з оновленими даними
        # # === ... ===

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

            # # Додаємо текст з анкети репетитора до списку даних
            # Саме тут відбувається перезапис даних кожного словника репетитора!
            for index, one_tutor in enumerate(data_tutors):
                one_tutor['about_myself_1'] = list_data_one_account[index]['about_myself_1']
                one_tutor['about_myself_2'] = list_data_one_account[index]['about_myself_2']
            
            # Зберігаємо файл з оновленими даними
            write_list_data_to_file(file_path_data, data_tutors, 'w')
            # with open(file_path_data, "w") as jsonFile:
            #     for item in data_tutors:
            #         json.dump(item, jsonFile)
            #         jsonFile.write('\n')


            num_page += 1
    
    # === THE END else ===
        
        # THE END While Loop
    # ----------------------------
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