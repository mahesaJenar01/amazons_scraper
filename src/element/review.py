from typing import Optional
from selenium import webdriver

def get_review(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get review count using JavaScript."""
    try:
        script = """
        const selector = `div[data-index="${arguments[0]}"] span[data-component-type="s-client-side-analytics"] span.a-size-base.s-underline-text`;
        const element = document.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
    except Exception as e:
        print(f"Error getting review for index {index}: {str(e)}")
        return None