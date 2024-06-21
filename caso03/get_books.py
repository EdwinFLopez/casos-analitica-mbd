import argparse
import json
import os
import re
import time
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlopen

import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Explicit wait https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.support.wait import WebDriverWait
from unidecode import unidecode


def get_all_lists(soup):
    lists = []
    list_count_dict = {}

    if soup.find('a', text='More lists with this book...'):
        lists_url = soup.find('a', text='More lists with this book...')['href']

        source = urlopen('https://www.goodreads.com' + lists_url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        lists += [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'cell'})]

        i = 0
        while soup.find('a', {'class': 'next_page'}) and i <= 10:
            time.sleep(2)
            next_url = 'https://www.goodreads.com' + soup.find('a', {'class': 'next_page'})['href']
            source = urlopen(next_url)
            soup = bs4.BeautifulSoup(source, 'lxml')

            lists += [node.text for node in soup.find_all('div', {'class': 'cell'})]
            i += 1

        # Format lists text.
        for _list in lists:
            # _list_name = ' '.join(_list.split()[:-8])
            # _list_rank = int(_list.split()[-8][:-2]) 
            # _num_books_on_list = int(_list.split()[-5].replace(',', ''))
            # list_count_dict[_list_name] = _list_rank / float(_num_books_on_list)     # TODO: switch this back to raw counts
            _list_name = _list.split()[:-2][0]
            _list_count = int(_list.split()[-2].replace(',', ''))
            list_count_dict[_list_name] = _list_count

    return list_count_dict


def get_shelves(soup):
    # Find the element containing the number of people currently reading
    currently_reading_element = soup.find("div", class_="SocialSignalsSection__caption")
    print(currently_reading_element)
    if currently_reading_element:
        # Extract the text and clean it
        currently_reading_text = currently_reading_element.text.strip()
        print(currently_reading_text)
        # Extract the number of people currently reading using string manipulation
        currently_reading_count = currently_reading_text.split()[0]
        print("Number of people currently reading:", currently_reading_count)
        return currently_reading_count
    else:
        print("Currently reading signal not found.")
        return ""


def get_want_to(soup):
    # Find the element containing the number of people who want to read
    want_to_read_element = soup.find("div", {"data-testid": "toReadSignal"})
    print("TO READ SIGNAL")
    print(want_to_read_element)
    if want_to_read_element:
        # Extract the text and clean it
        want_to_read_text = want_to_read_element.text.strip()
        # Extract the number of people who want to read using string manipulation
        want_to_read_count = want_to_read_text.split()[0]
        print("Number of people who want to read:", want_to_read_count)
        return want_to_read_count
    else:
        print("Want to read signal not found.")
        return ""


def get_genres(soup):
    # Find the genres list
    genres_list_element = soup.find("div", {"data-testid": "genresList"})
    if genres_list_element:
        # Find all genre button elements
        genre_button_elements = genres_list_element.find_all("span", {"class": "BookPageMetadataSection__genreButton"})

        # Extract genre names
        genres = [genre_button.find("span", {"class": "Button__labelItem"}).text.strip() for genre_button in
                  genre_button_elements]

        # Print the genres
        print("Genres:", genres)
        return genres
    else:
        print("Genres list not found.")
        return ""


def get_series_name(soup):
    # Find the <dt> tag corresponding to the "Series" section
    series_dt = soup.find("dt", string="Series")

    # Check if the <dt> tag is found
    if series_dt:
        # Find the next <dd> tag after the <dt> tag
        series_dd = series_dt.find_next_sibling("dd")

        # Check if the <dd> tag is found and has text
        if series_dd and series_dd.text.strip():
            # Extract the series text from the <dd> tag
            series_text = series_dd.text.strip()

            # Extract the series names from the <a> tags within the <dd> tag
            series_names = [unidecode(a.text.strip()) for a in series_dd.find_all("a")]

            print("Series:", series_text)
            print("Series Names:", series_names)
            return series_names
        else:
            print("No series information found.")
            return ""
    else:
        print("No series section found.")
        return ""


def get_series_uri(soup):
    try:
        series = soup.find(id="bookSeries").find("a")
        series_uri = series.get("href")
        return series_uri
    except:
        return ""


def get_top_5_other_editions(soup):
    other_editions = []
    for div in soup.findAll('div', {'class': 'otherEdition'}):
        other_editions.append(div.find('a')['href'])
    return other_editions


def get_isbn(soup):
    try:
        isbn = re.findall(r'nisbn: [0-9]{10}', str(soup))[0].split()[1]
        return isbn
    except:
        return "isbn not found"


def get_isbn13(soup):
    try:
        isbn13 = re.findall(r'nisbn13: [0-9]{13}', str(soup))[0].split()[1]
        return isbn13
    except:
        return "isbn13 not found"


def get_rating_distribution(soup):
    # Encontrar todos los elementos del histograma de calificaciones
    rating_bars = soup.find_all("div", class_="RatingsHistogram__bar")

    # Recorrer los elementos y extraer los valores
    ratings_data = []
    for bar in rating_bars:
        total_ratings = int(
            bar.find("div", class_="RatingsHistogram__labelTotal").text.strip().split()[0].replace(',', ''))
        ratings_data.append((total_ratings))

    distribution_dict = {'5 Stars': ratings_data[0],
                         '4 Stars': ratings_data[1],
                         '3 Stars': ratings_data[2],
                         '2 Stars': ratings_data[3],
                         '1 Star': ratings_data[4]}
    return distribution_dict


def get_num_pages(soup):
    pages_format_element = soup.find("p", {"data-testid": "pagesFormat"})

    if pages_format_element:
        pages_format_text = pages_format_element.text.strip()

        # Split the text based on comma separator
        pages_format_parts = pages_format_text.split(", ")

        # Extract pages and format separately
        if len(pages_format_parts) == 2:
            pages = pages_format_parts[0].split()[0]  # Extract the number of pages
            book_format = pages_format_parts[1]  # Extract the book format
            print("Pages:", pages)
            print("Format:", book_format)
            return pages, book_format
        else:
            return ["", ""]
    else:
        return ["", ""]


def get_year_first_published(soup):
    # Find the publication year
    publication_info_element = soup.find("p", {"data-testid": "publicationInfo"})
    if publication_info_element:
        publication_info = publication_info_element.text.strip()
        # Extract the publication year
        publication_year = publication_info.split()[-1]
        print("Publication Year:", publication_year)
        return publication_year
    else:
        return ""


def get_id(bookid):
    pattern = re.compile("([^.-]+)")
    return pattern.search(bookid).group()


def get_cover_image_uri(soup):
    series = soup.find('img', class_='ResponsiveImage')
    if series:
        series_uri = series.get('src')
        print(series_uri)
        return series_uri
    else:
        return ""


def espera(driver, tag, toPrint, extra_text=""):
    try:
        with WebDriverWait(driver, timeout=30, poll_frequency=3) as wd:
            if tag == 'id':
                wd.until(EC.presence_of_element_located((By.ID, toPrint)))
            elif (tag == 'xpath'):
                wd.until(EC.presence_of_element_located((By.XPATH, toPrint)))
    except:
        # driver.quit()
        print('Driver timeout. Waiting for element >' + toPrint + '<' + extra_text)
        return -1


def espera_texto(driver, tag, toPrint, extra_text=""):
    try:
        with WebDriverWait(driver, timeout=30, poll_frequency=3) as wd:
            if tag == 'id':
                wd.until(EC.text_to_be_present_in_element((By.ID, toPrint), 'people'))
            elif (tag == 'xpath'):
                wd.until(EC.text_to_be_present_in_element((By.XPATH, toPrint), 'people'))
    except:
        # driver.quit()
        print('Driver timeout. Waiting for element >' + toPrint + '<' + extra_text)
        return -1


def get_author_link(soup):
    author_link = soup.find("a", class_="ContributorLink")
    return author_link['href']


def get_author_name(soup):
    author_element = soup.find("span", class_="ContributorLink__name")
    return unidecode(author_element.text.strip())


def get_num_ratings(soup):
    print("Num ratings")
    ratings_element = soup.find("span", {"data-testid": "ratingsCount"})
    ratings_text = ratings_element.text.strip()
    # Extract digits from the ratings text
    num_reviews = ratings_text.split('\xa0')[0].replace(',', '')
    print(num_reviews)
    return num_reviews


def get_num_reviews(soup):
    print("Num reviews")
    reviews_element = soup.find("span", {"data-testid": "reviewsCount"})
    reviews_text = reviews_element.text.strip()
    # Extract digits from the reviews text
    num_reviews = reviews_text.split('\xa0')[0].replace(',', '')
    print(num_reviews)
    return int(num_reviews)


def get_average_rating(soup):
    print("Avg rating")
    avg_rating = soup.find("div", class_="RatingStatistics__rating")
    avg_rating_text = avg_rating.text.strip()
    print(avg_rating_text)
    return avg_rating_text


def get_awards(soup):
    award_spans = soup.find_all("span", {"data-testid": "award"})
    print(award_spans)
    list_awards = []
    if award_spans != None:
        # Iterate over each <span> tag to extract the award information
        for award_span in award_spans:
            # Extract the award text
            award_text = award_span.text.strip()
            #print("Award:", award_text)
            list_awards.append(unidecode(award_text))
        return list_awards
    else:
        return ""


def makeClick(driver, tag, elementToClick):
    success = 0
    attempts = 0
    while success == 0:
        try:
            if espera(driver, tag, elementToClick) != -1:
                driver.find_element(tag, elementToClick).click()
                success = 1
            else:
                return -1
        except:
            success = 0
            attempts = attempts + 1
    return attempts


def get_settings(soup):
    # Find the <dt> tag corresponding to the "Settings" section
    setting_dt = soup.find("dt", string="Setting")

    # Check if the <dt> tag is found
    if setting_dt:
        # Find the next <dd> tag after the <dt> tag
        setting_dd = setting_dt.find_next_sibling("dd")

        # Check if the <dd> tag is found and has text
        if setting_dd and setting_dd.text.strip():
            # Extract the series text from the <dd> tag
            setting_text = setting_dd.text.strip()

            # Extract the series names from the <a> tags within the <dd> tag
            setting_names = [unidecode(a.text.strip()) for a in setting_dd.find_all("a")]

            print("Settings:", setting_text)
            print("Settings names:", setting_names)
            return setting_names
        else:
            print("No setting information found.")
            return ""
    else:
        print("No setting section found.")
        return ""


def get_characters(soup):
    # Find the <dt> tag corresponding to the "Settings" section
    chars_dt = soup.find("dt", string="Characters")

    # Check if the <dt> tag is found
    if chars_dt:
        # Find the next <dd> tag after the <dt> tag
        chars_dd = chars_dt.find_next_sibling("dd")

        # Check if the <dd> tag is found and has text
        if chars_dd and chars_dd.text.strip():
            # Extract the series text from the <dd> tag
            chars_text = chars_dd.text.strip()

            # Extract the series names from the <a> tags within the <dd> tag
            chars_names = [unidecode(a.text.strip()) for a in chars_dd.find_all("a")]

            print("Characters:", chars_text)
            print("Character names:", chars_names)
            return chars_names
        else:
            print("No character information found.")
            return ""
    else:
        print("No character section found.")
        return ""


def get_language(soup):
    # Find the <dt> tag corresponding to the "Settings" section
    language_dt = soup.find("dt", string="Language")

    # Check if the <dt> tag is found
    if language_dt:
        # Find the next <dd> tag after the <dt> tag
        language_dd = language_dt.find_next_sibling("dd")
        # Check if the <dd> tag is found and has text
        if language_dd and language_dd.text.strip():
            # Extract the series text from the <dd> tag
            language_text = language_dd.text.strip()

            print("Language:", language_text)
            return unidecode(language_text)
        else:
            print("No Language information found.")
            return ""
    else:
        print("No language section found.")
        return ""


def get_title(soup):
    title_element = soup.find('h1', {'data-testid': 'bookTitle'})
    if title_element:
        return unidecode(' '.join(title_element.text.split()))
    return ""


def wait_popup(driver):
    # A veces sale un pop-up que hay que cerrar
    try:
        with  WebDriverWait(driver, timeout=30, poll_frequency=3) as wd:
            popup_window = wd.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]")))
            popup_window2 = wd.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[1]/div/div/button")))

            # Check if the pop-up window is displayed
            if popup_window.is_displayed():
                # Find the dismiss button inside the pop-up window
                dismiss_button = popup_window.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/button")
                # Click on the dismiss button
                dismiss_button.click()
            # Check if the pop-up window is displayed
            if popup_window2.is_displayed():
                # Find the dismiss button inside the pop-up window
                dismiss_button2 = popup_window2.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div/button")
                # Click on the dismiss button
                dismiss_button2.click()
    except:
        pass


def scrape_book(driver, book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    driver.get(url)
    wait_popup(driver)
    # If the book is not in Goodreads anymore, it will not have a title
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')
    title_element = soup.find('h1', {'data-testid': 'bookTitle'})
    if title_element == None:
        return -1
    wait_popup(driver)
    #Espero a que salga el botón de "Book detals & editions". Veo que a veces cambia de XPath
    espera(driver, 'xpath', '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[6]/div/div/button/span[1]',
           "Books details & editions 1")
    espera(driver, 'xpath', '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[7]/div/div/button/span[1]',
           "Books details & editions 2")
    attempts = makeClick(driver, 'xpath',
                         '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[7]/div/div/button/span[1]')
    attempts = makeClick(driver, 'xpath',
                         '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[6]/div/div/button/span[1]')
    wait_popup(driver)
    #Esperamos a que aparezcan los current_readings
    espera_texto(driver, 'xpath',
                 '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[7]/div/div[1]/span/div[2]/div',
                 "current_readings")
    espera_texto(driver, 'xpath',
                 '//*[@id="__next"]/div[2]/main/div[1]/div[2]/div[2]/div[2]/div[7]/div/div[2]/span/div[2]/div',
                 "current_readings2")
    wait_popup(driver)
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')
    wait_popup(driver)
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')

    return {'book_id_title': book_id,
            'book_id': get_id(book_id),
            'cover_image_uri': get_cover_image_uri(soup),
            'book_title': get_title(soup),
            "book_series": get_series_name(soup),
            "book_settings": get_settings(soup),
            "book_characters": get_characters(soup),
            "book_language": get_language(soup),
            # "book_series_uri":      get_series_uri(soup),
            # 'top_5_other_editions': get_top_5_other_editions(soup),
            # 'isbn':                 get_isbn(soup),
            # 'isbn13':               get_isbn13(soup),
            'year_first_published': get_year_first_published(soup),
            'authorlink': get_author_link(soup),
            'author': get_author_name(soup),
            'num_pages': get_num_pages(soup)[0],
            'format': get_num_pages(soup)[1],
            'genres': get_genres(soup),
            'people_curr_read': get_shelves(soup),
            'peop_want_to_read': get_want_to(soup),
            # 'lists':                get_all_lists(soup),
            'num_ratings': get_num_ratings(soup),
            'num_reviews': get_num_reviews(soup),
            'average_rating': get_average_rating(soup),
            'rating_distribution': get_rating_distribution(soup),
            'awards': get_awards(soup)}


def condense_books(books_directory_path):
    books = []
    # Look for all the files in the directory and if they contain
    # "book-metadata," then load them all and condense them into a single file
    for file_name in os.listdir(books_directory_path):
        if (file_name.endswith('.json') and not file_name.startswith('.')
                and file_name != "all_books.json" and "book-metadata" in file_name):
            _book = json.load(open(books_directory_path + '/' + file_name, 'r'))  #, encoding='utf-8', errors='ignore'))
            books.append(_book)
    return books


def main():
    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--book_ids_path', type=str, default='my_list_of_books.txt')
    parser.add_argument('--output_directory_path', type=str, default='classic_book_metadata')
    parser.add_argument('--format', type=str, action="store", default="csv",
                        dest="format", choices=["json", "csv"],
                        help="set file output format")
    args = parser.parse_args()

    book_ids = [line.strip() for line in open(args.book_ids_path, 'r') if line.strip()]
    books_already_scraped = [file_name.replace('_book-metadata.json', '') for file_name in
                             os.listdir(args.output_directory_path) if
                             file_name.endswith('.json') and not file_name.startswith('all_books')]
    books_to_scrape = [book_id for book_id in book_ids if book_id not in books_already_scraped]
    condensed_books_path = args.output_directory_path + '/all_books'

    chrome_options = Options()
    # Agregar opciones para automatización:
    # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md#catch-all-automation
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-features=Translate")
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--no-first-run")
    driver = webdriver.Chrome(options=chrome_options)

    no_encontrados = 0
    for i, book_id in enumerate(books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' + script_name + ': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' + script_name + ': #' + str(
                i + 1 + len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            book = scrape_book(driver, book_id)
            # If it returns -1, it means that the book was not found
            if book != -1:
                # Add book metadata to file name to be more specific
                json.dump(book, open(args.output_directory_path + '/' + book_id + '_book-metadata.json', 'w'))
            else:
                print("Libro no encontrado!")
                no_encontrados += 1

            print('=============================')

        except HTTPError as e:
            print(e)
            exit(0)

    books = condense_books(args.output_directory_path)
    if args.format == 'json':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
    elif args.format == 'csv':
        json.dump(books, open(f"{condensed_books_path}.json", 'w'))
        book_df = pd.read_json(f"{condensed_books_path}.json")
        book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding='utf-8')

    print(f"{str(datetime.now())} {script_name}: ============================================")
    print(f"🎉 Success! All book metadata scraped. 🎉\n\n")
    print(f"Metadata files have been output to {os.path.abspath(args.output_directory_path)}")
    print(f"Goodreads scraping run time = ⏰ {str(datetime.now() - start_time)} ⏰")
    print(str(no_encontrados) + "Books were not found")
    print(f"============================================")


if __name__ == '__main__':
    main()
