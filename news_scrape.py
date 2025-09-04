import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = Chrome()
driver.get("https://akharinkhabar.ir/")

all_news = []

def scrape_category(href, limit=200):
    news_list = []
    scroll_pause = 2
    max_scroll = 50
    scrolls = 0

    # cllick on category
    cat_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[href="{href}"]'))
    )
    cat_btn.click()
    time.sleep(3)

    while len(news_list) < limit and scrolls < max_scroll:
        news_blocks = driver.find_elements(By.CSS_SELECTOR, '.rectangle_container__rBE5L')

        for block in news_blocks:
            try:
                new = dict()
                new["category"] = href.strip("/")
                new["title"] = block.find_element(By.CSS_SELECTOR, ".rectangle_news_title__VvUoG").text.strip()
                new["time"] = block.find_element(By.CSS_SELECTOR, ".rectangle_timeline__DxX7C time").text.strip()
                try:
                    img_tag = block.find_element(By.CSS_SELECTOR, ".rectangle_news_image__fcCG2 img")
                    new["cover"] = img_tag.get_attribute("src")
                except:
                    new["cover"] = ""
                news_list.append(new)
            except:
                pass

        # scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        scrolls += 1

    return news_list

all_news.extend(scrape_category("/politics", 200))


pd.DataFrame(all_news).to_excel("news_scrape.xlsx", index=False)

driver.close()
