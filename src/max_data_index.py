from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def check_error_page(driver: webdriver.Chrome) -> bool:
    """Check if current page is an error page."""
    try:
        title = driver.title
        return "Sorry! Something went wrong!" in title
    except WebDriverException:
        return True

def get_max_data_index(driver: webdriver.Chrome) -> int:
    """Get the highest data-index value using JavaScript with error checking."""
    try:
        if check_error_page(driver):
            raise ValueError("Error page detected")
            
        script = """
        const elements = document.querySelectorAll('div[data-component-type="s-search-result"][data-index]');
        if (elements.length === 0) {
            throw new Error('No search results found');
        }
        const indices = Array.from(elements).map(el => parseInt(el.getAttribute('data-index'), 10));
        return Math.max(...indices);
        """
        max_index = driver.execute_script(script)
        
        if max_index is None or max_index < 0:
            raise ValueError("No valid data-index found")
        
        return max_index
        
    except Exception as e:
        print(f"Error getting max data index: {str(e)}")
        raise