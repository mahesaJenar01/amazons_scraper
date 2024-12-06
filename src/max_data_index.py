from selenium import webdriver

def get_max_data_index(driver: webdriver.Chrome) -> int:
    """Get the highest data-index value using JavaScript."""
    try:
        script = """
        const elements = document.querySelectorAll('div[data-component-type="s-search-result"][data-index]');
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