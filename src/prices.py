from typing import Optional
from selenium import webdriver

def get_prices(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get price text for a specific data-index using JavaScript."""
    try:
        script = """
        const selector = `div[data-index="${arguments[0]}"] span.a-offscreen`;
        const element = document.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting price for index {index}: {str(e)}")
        return None