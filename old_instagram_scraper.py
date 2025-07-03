from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager as CM
import time
import random


def login(bot, username, password):
    bot.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.randrange(2, 5))

    username_input = WebDriverWait(bot, 10).until(
        EC.element_to_be_clickable((By.NAME, "username"))
    )
    password_input = WebDriverWait(bot, 10).until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )

    for char in username:
        username_input.send_keys(char)
        time.sleep(random.randrange(0.1, 0.3))

    for char in password:
        password_input.send_keys(char)
        time.sleep(random.randrange(0.1, 0.3))

    login_button = WebDriverWait(bot, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    time.sleep(10)


def scrape_followers(bot, target_username, num_followers):
    bot.get(f"https://www.instagram.com/{target_username}/")
    time.sleep(3)

    followers_link = WebDriverWait(bot, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
    )
    followers_link.click()
    time.sleep(2)

    try:
        followers_popup = WebDriverWait(bot, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
    except Exception as e:
        print(f"Error: {e}")
        bot.quit()
        return

    users = set()
    with open(f"{target_username}_followers.txt", "w") as file:
        while len(users) < num_followers:
            bot.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup
            )
            time.sleep(
                2
            )  # I have experiment and this is the suitable, enough time to not get suspect

            followers = bot.execute_script(
                """
                let usernames = [];
                document.querySelectorAll('a[href*="/"]').forEach(link => {
                    let href = link.getAttribute('href');
                    if (href && href.startsWith('/')) {
                        let username = href.split('/')[1];
                        if (username && !usernames.includes(username)) {
                            usernames.push(username);
                        }
                    }
                });
                return usernames;
            """
            )

            if not followers:
                print("No more followers found or unable to extract usernames.")
                break

            for username in followers:
                if username and username not in users:
                    users.add(username)
                    file.write(username + "\n")
                if len(users) >= num_followers:
                    break

            # Scroll down further to load more followers
            ActionChains(bot).send_keys(Keys.END).perform()
            time.sleep(2)

    print(f"[Info] - Saved {len(users)} followers to {target_username}_followers.txt")


def scrape():
    # Change this information using your clone Instagram account
    username = "temibij805"
    password = "Aas121574"

    service = Service(CM().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15)

    login(bot, username, password)

    target_username = "ufclassof2yrs"
    num_followers = 3000

    scrape_followers(bot, target_username, num_followers)

    bot.quit()


# if __name__ == "__main__":
#     scrape()
