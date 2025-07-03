from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

phone_number = os.getenv("PHONE_NUMBER")
password = os.getenv("PASSWORD")
search_query_choices = [
    "whiskey",
    "luxury whiskey",
    "whhiskey in Vietnam",
    "whiskey in VN",
    "delicious whiskey",
]

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/login")
time.sleep(2)


def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.3, 2.0))


def scroll_feed(feed_div, scroll_times):
    for _ in range(scroll_times):
        ActionChains(driver).move_to_element(feed_div).click().perform()
        feed_div.send_keys("\ue00f")  # PAGE_DOWN
        time.sleep(random.uniform(1.5, 2.5))


def click_see_more_buttons(feed_div):
    see_more_buttons = feed_div.find_elements(
        By.XPATH,
        './/div[@role="button" and contains(@class, "x1i10hfl") and text()="Xem thêm"]',
    )
    for btn in see_more_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            btn.click()
            time.sleep(random.uniform(0.5, 1.2))
        except Exception:
            continue


def scroll_and_scrape_one_by_one(driver, max_posts=10):
    feed_div = driver.find_element(By.XPATH, '//div[@role="feed"]')
    seen_posts = set()
    post_index = 0

    while len(seen_posts) < max_posts:
        posts = feed_div.find_elements(By.XPATH, "./div")
        if post_index >= len(posts):
            ActionChains(driver).move_to_element(feed_div).click().perform()
            feed_div.send_keys("\ue00f")
            time.sleep(random.uniform(2.0, 3.0))
            continue

        # skip first item since it is not a post but Nhóm
        if post_index == 0:
            post_index += 1
            continue

        post = posts[post_index]
        post_id = post.get_attribute("data-pagelet") or f"index-{post_index}"
        if post_id in seen_posts:
            post_index += 1
            continue

        seen_posts.add(post_id)

        driver.execute_script("arguments[0].scrollIntoView(true);", post)
        time.sleep(random.uniform(1.0, 2.0))
        try:
            see_more = post.find_element(
                By.XPATH,
                './/div[@role="button" and contains(@class, "x1i10hfl") and text()="Xem thêm"]',
            )
            see_more.click()
            time.sleep(random.uniform(0.5, 1.2))
        except:
            pass

        pageNames = [
            span.text
            for span in post.find_elements(
                By.XPATH,
                './/span[contains(@class, "xdj266r") and contains(@class, "x14z9mp") and contains(@class, "xat24cr") and contains(@class, "x1lziwak") and contains(@class, "xexx8yu") and contains(@class, "xyri2b") and contains(@class, "x18d9i69") and contains(@class, "x1c1uobl") and contains(@class, "x1hl2dhg") and contains(@class, "x16tdsg8") and contains(@class, "x1vvkbs")]',
            )
        ]

        contents = [
            div.text
            for div in post.find_elements(
                By.XPATH, './/div[@dir="auto" and @style="text-align: start;"]'
            )
        ]

        emoji_counts = [
            span.text
            for span in post.find_elements(
                By.XPATH, './/span[contains(@class, "x135b78x")]'
            )
        ]

        comment_counts = [
            span.text
            for span in post.find_elements(
                By.XPATH,
                './/span[contains(@class, "xdj266r") and contains(text(), "bình luận")]',
            )
        ]

        print("Post #", len(seen_posts))
        print("Titles:", pageNames[0])
        print("Contents:", contents)
        print("Comment counts:", comment_counts)
        print("Emoji counts:", emoji_counts)
        print("-" * 50)

        post_index += 1
        time.sleep(random.uniform(10.0, 20.0))


text_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
slow_type(text_input, phone_number)
slow_type(password_input, password)
driver.find_element(By.NAME, "login").click()
time.sleep(random.randrange(5, 10))

searchbarInput = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
time.sleep(random.randrange(3, 7))
slow_type(searchbarInput, random.choice(search_query_choices))
searchbarInput.send_keys("\ue007")  # Enter
time.sleep(random.randrange(3, 7))

feed_div = driver.find_element(By.XPATH, '//div[@role="feed"]')
scroll_times = random.randint(3, 5)

scroll_and_scrape_one_by_one(driver, max_posts=scroll_times)
