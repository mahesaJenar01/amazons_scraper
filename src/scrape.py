import time
from typing import List, Dict
from .prices import get_prices
from .rating import get_rating
from .review import get_review
from .timing_stats import TimingStats
from .brand_name import get_brand_name
from .setup_driver import setup_driver
from .sales_info import get_sales_info
from .product_name import get_product_name
from .max_data_index import get_max_data_index
from selenium.webdriver.support.ui import WebDriverWait

def scrape(urls: List[str]) -> Dict[str, dict]:
    """
    Scrape brand names, product names, and ratings from multiple URLs.
    Returns a dictionary with URLs as keys and dictionaries containing data and timing stats as values.
    """
    results = {}
    driver = None
    
    try:
        driver = setup_driver()
        
        for url in urls:
            url_start_time = time.time()
            try:
                driver.get(url)
                time.sleep(5)
                
                WebDriverWait(driver, 20).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                
                max_index = get_max_data_index(driver)
                print(f"Processing URL with max_index: {max_index}")
                
                item_data = []
                timing_stats = TimingStats()
                
                for i in range(max_index + 1):
                    # Time brand name extraction
                    brand_start = time.time()
                    brand_name = get_brand_name(driver, i)
                    timing_stats.brand_time += time.time() - brand_start
                    
                    # Time product name extraction
                    product_start = time.time()
                    product_name = get_product_name(driver, i)
                    timing_stats.product_time += time.time() - product_start
                    
                    # Time rating extraction
                    rating_start = time.time()
                    rating = get_rating(driver, i)
                    timing_stats.rating_time += time.time() - rating_start
                    
                    # Time review extraction
                    review_start = time.time()
                    review = get_review(driver, i)
                    timing_stats.review_time += time.time() - review_start
                    
                    sales_info_start = time.time()
                    sales_info = get_sales_info(driver, i)
                    timing_stats.sales_info_time += time.time() - sales_info_start
                    
                    price_start = time.time()
                    price = get_prices(driver, i)
                    timing_stats.price_time += time.time() - price_start
                    
                    if brand_name or product_name:
                        timing_stats.total_items += 1
                        item_data.append((
                            brand_name if brand_name else '-',
                            product_name if product_name else '-',
                            rating if rating else '-',
                            review if review else '-',
                            sales_info if sales_info else '-',
                            price if price else '-'
                        ))
                
                url_total_time = time.time() - url_start_time
                
                results[url] = {
                    'data': item_data,
                    'timing': {
                        'total_time': url_total_time,
                        'total_items': timing_stats.total_items,
                        'average_times': timing_stats.get_averages()
                    }
                }
                
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
                results[url] = {'data': [], 'timing': {}}
                continue
                
    finally:
        if driver:
            driver.quit()
            
    return results
