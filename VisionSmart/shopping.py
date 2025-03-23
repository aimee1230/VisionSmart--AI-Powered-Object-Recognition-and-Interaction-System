import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_amazon_best_deal(object_name, object_color):
    """
    Search Amazon for the best deal on a detected object.
    Returns the top-ranked product link based on price, rating, and relevance.
    """

    search_query = f"{object_color} {object_name} best price"
    amazon_url = f"https://www.amazon.com/s?k={'+'.join(search_query.split())}"

    # Set up Selenium WebDriver (Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(amazon_url)
        time.sleep(3)  # Wait for the page to load

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract product listings
        product_list = []
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for result in results:
            title_tag = result.find("span", class_="a-text-normal")
            price_tag = result.find("span", class_="a-offscreen")
            rating_tag = result.find("span", class_="a-icon-alt")
            link_tag = result.find("a", class_="a-link-normal")

            if title_tag and price_tag and link_tag:
                title = title_tag.text.strip()
                price = float(price_tag.text.replace("$", "").replace(",", ""))
                rating = float(rating_tag.text.split()[0]) if rating_tag else 0.0
                link = "https://www.amazon.com" + link_tag["href"]

                product_list.append({"title": title, "price": price, "rating": rating, "link": link})

        driver.quit()

        # Sort by price and rating
        best_deal = sorted(product_list, key=lambda x: (x["price"], -x["rating"]))[0]

        return best_deal["link"]

    except Exception as e:
        driver.quit()
        return f"Error: {str(e)}"
