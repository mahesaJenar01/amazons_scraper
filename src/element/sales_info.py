from typing import Optional
from selenium import webdriver

def get_sales_info(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get sales info using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div.a-section.a-spacing-base div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small`);

        if (!definiteContainer) return null;

        const selector= 'div[data-cy="reviews-block"] div.a-row.a-size-base span.a-size-base.a-color-secondary';

        const element = definiteContainer.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
    except Exception as e:
        print(f"Error getting sales info for index {index}: {str(e)}")
        return None
