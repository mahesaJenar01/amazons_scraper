import time
from typing import Optional
from selenium import webdriver

def get_product_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get product name text for a specific data-index using JavaScript."""
    try:
        script = """
        const selector = `div[data-index="${arguments[0]}"][data-component-type="s-search-result"] span.a-size-base-plus.a-color-base.a-text-normal`;
        const element = document.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting product name for index {index}: {str(e)}")
        return None