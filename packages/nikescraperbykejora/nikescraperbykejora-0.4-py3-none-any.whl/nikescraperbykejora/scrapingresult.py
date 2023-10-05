# scraping_result
import pandas as pd
from nikescraperbykejora.linksscraper import NikeSpider
from nikescraperbykejora.datascraper import NikeProductScraper


class DataHandler:
    @staticmethod
    async def access_and_collect_data(product_scraper: NikeProductScraper):
        # Access all data
        parser = product_scraper.fetch_page()
        url = await product_scraper.get_url()
        image_url = await product_scraper.get_image(parser)
        product_name = await product_scraper.get_product_name(parser)
        product_category = await product_scraper.get_product_category(parser)
        original_price = await product_scraper.get_original_price(parser)
        discount_percentage = await product_scraper.get_discount_percentage(parser)
        discounted_price = await product_scraper.get_discounted_price(parser)
        colour_shown = await product_scraper.get_colour_shown(parser)
        style = await product_scraper.get_style(parser)
        product_description = await product_scraper.get_product_description(parser)
        reviews = await product_scraper.get_reviews(parser)
        rating = await product_scraper.get_rating(parser)
        sizes = await product_scraper.get_product_Sizes()
        images = await product_scraper.get_product_Images()

        # Collect all data
        product_data = {
            "Product URL": url,
            "Hero Image": image_url,
            "Product Name": product_name,
            "Product Category": product_category,
            "Original Price": original_price,
            "Discount Percentage": discount_percentage,
            "Discounted Price": discounted_price,
            "Colour": colour_shown,
            "Style": style,
            "Product Description": product_description,
            "Reviews": reviews,
            "Rating": rating,
            "Sizes": sizes,
            "Detail Images": images
        }
        return product_data


class ProductScraperHandler:
    @staticmethod
    async def one_product(target_url: str, txt_file_name: str):
        product_scraper = NikeProductScraper(target_url)
        product_data = await DataHandler.access_and_collect_data(product_scraper)
        product_data_list = [product_data]

        try:
            with open(txt_file_name, 'w', encoding='utf-8') as txt_file:
                for item in product_data_list:
                    txt_file.write(f"{item}\n")

            print(f"Scraping product completed.")

        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

    @staticmethod
    async def multi_product(target_url: str, csv_file_name: str, product_count: int, timeout_seconds: int):
        if product_count > 24:
            link_scraper = NikeSpider(target_url, timeout_seconds, infinite_scrolling=True)
        else:
            link_scraper = NikeSpider(target_url, timeout_seconds, infinite_scrolling=False)

        product_links = await link_scraper.get_all_product_links()
        product_scraper = NikeProductScraper(target_url)
        total_products = len(product_links)
        product_data_list = []

        for index, product_link in enumerate(product_links, start=1):
            print(f"No. {index} of {total_products}")

            product_scraper.url = product_link

            retries = 0
            while retries < 4:
                try:
                    product_data = await DataHandler.access_and_collect_data(product_scraper)
                    product_data_list.append(product_data)
                    # Save data to CSV after each successful scrape
                    df = pd.DataFrame(product_data_list)

                    try:
                        df.to_csv(csv_file_name, index=False, encoding='utf-8')
                        print(f"Scraping No. {index} completed.")

                    except Exception as e:
                        print(f"An error occurred while saving the data: {e}")
                    break
                except TimeoutError:
                    retries += 1
                    print(f"Timeout error occurred for URL: {product_link}. Retrying... Attempt {retries} of 3")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        # Save the final data to CSV
        df = pd.DataFrame(product_data_list)

        try:
            df.to_csv(csv_file_name, index=False, encoding='utf-8')
            print(f"Scraping all products completed. Results saved in {csv_file_name}")

        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
