import argparse
import os
from datetime import datetime

import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# Explicit wait https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.support.wait import WebDriverWait


def espera(driver, tag, toPrint):
    try:
        with WebDriverWait(driver=driver, timeout=10, poll_frequency=1) as wd:
            if tag == 'id':
                wd.until(EC.presence_of_element_located(By.ID, toPrint))
            elif tag == 'xpath':
                wd.until(EC.presence_of_element_located((By.XPATH, toPrint)))
    except:
        # driver.quit()
        #print('Driver timeout. Waiting for element >' + toPrint + '<')
        return -1


def get_titles(soup):
    titles = soup.find_all("a", class_="bookTitle", itemprop="url")
    # Recorrer los elementos y extraer los valores
    titles_array = []
    for value in titles:
        link = value["href"]
        titles_array.append(link)
    print(f"{len(titles_array)} books found")
    return titles_array


def main():
    list_titles = []
    start_time = datetime.now()
    script_name = os.path.basename(__file__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str,
                        default="https://www.goodreads.com/list/show/201106.Best_books_of_May_2024"
                        )
    parser.add_argument('--output_directory_path', type=str,
                        default="my_list_of_books.txt"
                        )
    args = parser.parse_args()
    print(args.url_path)
    print(args.output_directory_path)

    chrome_options = Options()
    #chrome_options.add_argument("--headless=new") # Wait does not work when headless :shrug
    #chrome_options.add_argument("--no-first-run")
    #chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-features=Translate")
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-sync")
    driver = webdriver.Chrome(options=chrome_options)

    # driver = webdriver.Chrome()
    url = args.url_path
    driver.get(url)

    while True:
        # primero leemos los datos de una página
        retries = 0
        max_retries = 50
        while (espera(driver, 'xpath', '//*[@id="all_votes"]/table/tbody/tr[1]/td[3]/a') == -1
               and retries < max_retries):
            retries += 1
        if retries == max_retries:
            print(f"{retries} retries  reached!!")
            #exit(1)

        source = driver.page_source
        soup = bs4.BeautifulSoup(source, 'html.parser')
        titles = get_titles(soup)
        for title in titles:
            list_titles.append(title.split('/book/show/')[1])
        print(str(len(list_titles)) + " titles in the list! 🎉")

        try:
            # Wait for the pop-up window to appear
            popup_window = WebDriverWait(driver, 10, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]"))
            )
            # Check if the pop-up window is displayed
            if popup_window.is_displayed():
                # Find the dismiss button inside the pop-up window
                dismiss_button = popup_window.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/button")
                # Click on the dismiss button
                dismiss_button.click()
        except:
            pass

        # Ahora clicamos el botón de next
        next_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next_page"))
        )
        if "disabled" not in next_button.get_attribute("class"):
            # Click on the next button
            next_button.click()
        else:
            # Break out of the loop if the next button is disabled
            break

    # Open the file in write mode
    with open(args.output_directory_path, "w") as file:
        # Write each element of the list to a separate line in the file
        for item in list_titles:
            file.write(item + "\n")

    print("==========================================================================")
    print(f"{str(datetime.now())} {script_name}: ")
    print(f"  🎉 Success! All the books from the list have been scrapped. 🎉")
    print(f"  The list has been stored to {os.path.abspath(args.output_directory_path)}")
    print(f"  Goodreads scraping run time = ⏰ {str(datetime.now() - start_time)} ⏰")
    print("==========================================================================")


if __name__ == '__main__':
    main()
