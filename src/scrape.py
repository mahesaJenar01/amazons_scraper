import time
from typing import List, Dict
from datetime import datetime
from selenium import webdriver
from .prices import get_prices
from .rating import get_rating
from .review import get_review
from .timing_stats import TimingStats
from .brand_name import get_brand_name
from .setup_driver import setup_driver
from .sales_info import get_sales_info
from .retry_manager import RetryManager
from .product_name import get_product_name
from selenium.webdriver.support.ui import WebDriverWait
from .max_data_index import get_max_data_index, check_error_page

def scrape(urls: List[str]) -> Dict[str, dict]:
    """
    Scrape data with retry mechanism for failed URLs.
    """
    results = {}
    driver = None
    retry_manager = RetryManager()
    
    try:
        driver = setup_driver()
        
        # Process initial URLs
        results.update(process_urls(driver, urls, retry_manager))
        
        # Process retry queue
        while retry_item := retry_manager.get_next_retry():
            if retry_item.attempts >= retry_manager.max_attempts:
                print(f"Max retry attempts reached for {retry_item.url}")
                continue
                
            retry_item.attempts += 1
            retry_item.last_attempt = datetime.now()
            
            retry_results = process_urls(driver, [retry_item.url], retry_manager)
            results.update(retry_results)
            
    finally:
        if driver:
            driver.quit()
            
    return results

def process_urls(driver: webdriver.Chrome, urls: List[str], retry_manager: RetryManager) -> Dict[str, dict]:
    """Process a list of URLs and handle retries."""
    results = {}
    
    for url in urls:
        if retry_manager.should_retry(url) and retry_manager.max_attempts <= 1:
            continue
            
        url_start_time = time.time()
        try:
            driver.get(url)
            time.sleep(5)
            
            WebDriverWait(driver, 20).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            if check_error_page(driver):
                print(f"Error page detected for {url}")
                retry_manager.add_retry(url)
                results[url] = {'data': [], 'timing': {}}
                continue
            
            max_index = get_max_data_index(driver)
            print(f"Processing URL with max_index: {max_index}")
            
            item_data = []
            timing_stats = TimingStats()
            
            for i in range(max_index + 1):
                # Extract data with timing
                brand_start = time.time()
                brand_name = get_brand_name(driver, i)
                timing_stats.brand_time += time.time() - brand_start
                
                product_start = time.time()
                product_name = get_product_name(driver, i)
                timing_stats.product_time += time.time() - product_start
                
                rating_start = time.time()
                rating = get_rating(driver, i)
                timing_stats.rating_time += time.time() - rating_start
                
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
            retry_manager.add_retry(url)
            results[url] = {'data': [], 'timing': {}}
            continue
            
    return results