from pathlib import Path
from tutors_app.scrap_logic import fetch_url_with_retries
from tutors_app.utils import get_file_path, timer_elapsed
import json


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


def create_empty_txt_file(file_name):
    with open(file_name, 'w'):
        pass
    # print(f"File '{file_name}' created successfully") # for test


def delete_file(file_path):
    try:
        file_path.unlink()
        print(f'File "{file_path}" deleted successfully')
    except FileNotFoundError:
        print(f'Error: File "{file_path}" not found')
    except OSError as e:
        print(f'Error deleting file "{file_path}": {e}')


def create_file_dir_structure(subject):
    current_directory = Path.cwd()
    dir_path = f"{current_directory}/{subject}/"
    create_dir(dir_path)
    for num_page_dir in range(1, 8):
        dir_path_num_page = f"{dir_path}/{str(num_page_dir)}"
        create_dir(dir_path_num_page)
        create_empty_txt_file(f'{dir_path_num_page}/{num_page_dir}.jsonl') # html-код за адресою f'/{num_page_dir}/' - для подальшого зберігання списку репетиторів на певній сторінці
        for id_tutor_dir in range( 1 + 20 * ( num_page_dir - 1), 1 + 20 * num_page_dir ):
            path_id_tutor_dir = f'{dir_path_num_page}/{str(id_tutor_dir)}'
            create_dir(f'{path_id_tutor_dir}')
            create_empty_txt_file(f'{path_id_tutor_dir}/{id_tutor_dir}.jsonl') # html-код за адресою f'/{num_page_dir}/{id_tutor_dir}/'
  
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


def rename_txt_file(old_file_name, new_file_name):
    old_file_path = Path(f'{Path.cwd()}/bio/{old_file_name}.txt')
    new_file_path = Path(f'{Path.cwd()}/bio/{new_file_name}.txt')
    
    if old_file_path.exists():
        old_file_path.rename(new_file_path)
    else:
        print(f'Не існує файлу {old_file_name}.txt!')


# ====================== ???  ==============
# --------------------------------------------------
def get_count_lines_file(file_path):
    with open(file_path, 'r') as file:
        line_count = 0
        for count, _ in enumerate(file):
            line_count = count + 1
        # line_count = count + 1 if count is not None else 0 # Handle empty files
    return line_count


# def writing_html_to_file(num_page, file_name):
#     # url = f"https://buki.com.ua/tutors/biolohiia/{num_page}/" - це хибна адреса!
#     # html, _ = get_html(url, timeout=10, return_soup=False)
#     html, _ = fetch_url_with_retries(url, retries=3, timeout=10, return_soup=False)

#     # if html is None:
#     #     # handle error
#     if not html or html.startswith('Error'):
#         print(f"Failed to fetch HTML for page {num_page}")
#         return

#     file_path = f'{Path.cwd()}/bio/{num_page}/{file_name}/{file_name}.txt'

#     try:
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(html)
#         print(f"Succesfully wrote large text in chunks to {file_path}")

#     except IOError as e:
#         print(f'Error writing to file: {e}')


def write_list_data_to_file(file_path, list_data, mode='a'):
    '''
        Зберігає список словників до JSONL-файлу
        mode: 'a' or 'w'
    '''
    with open(file_path, mode, encoding='utf-8') as file:
        for item in list_data:
            json_line = json.dumps(item, ensure_ascii=False)
            file.write(json_line + '\n')
                # json.dumps(item) перетворює словник на JSON-рядок
                # ensure_ascii=False дозволяє зберігати кирилицю та інші символи як є
                # '\n' після кожного рядка відповідає формату .jsonl


# !!! Not using
# # @timer_elapsed
# # def save_to_file(data, fname='data.jsonl'):
# #     # Save data to a file after each page to avoid overloading RAM.
# #     # Use JSON Lines for incremental saving
# #     file_path = get_file_path(fname)
# #     with file_path.open(mode='a', encoding='utf-8') as file:
# #         if type(data) is list:
# #             for record in data:
# #                 file.write(json.dumps(record) + '\n')
# #         elif type(data) is dict:
# #             for record in data.items():
#                 file.write(json.dumps(record) + '\n')


def create_dir_bio():
    subject_dir = Path('bio')
    current_directory = Path.cwd()
    dir_path_bio = f"{current_directory}/{subject_dir}/"
    create_dir(dir_path_bio)
    return dir_path_bio


# def main():
#     dir_path_bio = create_dir_bio()
#     print(f'dir_path_bio == {dir_path_bio}')


# if __name__ == "__main__":
#     main()