from typing import Optional
from selenium import webdriver

def get_rating(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get rating text for a specific data-index using JavaScript."""
    try:
        # Use a single JavaScript execution to find and extract rating
        script = """
        const selectors = [
            `div[data-index="${arguments[0]}"] span.a-icon-alt`,
            `div[data-index="${arguments[0]}"] i[data-cy="reviews-ratings-slot"] span.a-icon-alt`,
            `div[data-index="${arguments[0]}"] .a-icon.a-icon-star-small span.a-icon-alt`
        ];
        
        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.textContent.trim()) {
                return element.textContent.trim();
            }
        }
        return null;
        """
        
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting rating for index {index}: {str(e)}")
        return None