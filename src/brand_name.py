from typing import Optional
from selenium import webdriver

def get_brand_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get brand name text for a specific data-index using JavaScript."""
    try:
        script = """
        const selector = `div[data-index="${arguments[0]}"][data-component-type="s-search-result"] span.a-size-base-plus.a-color-base`;
        const element = document.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting brand name for index {index}: {str(e)}")
        return None