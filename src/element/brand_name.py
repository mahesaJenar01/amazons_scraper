from typing import Optional
from selenium import webdriver

def get_brand_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get brand name text for a specific data-index using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div.a-section.a-spacing-base div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small`);

        if (!definiteContainer) return null;

        const selector= 'div[data-cy="title-recipe"] div.a-row.a-color-secondary h2.a-size-mini.s-line-clamp-1 span.a-size-base-plus.a-color-base';

        const element = definiteContainer.querySelector(selector);
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting brand name for index {index}: {str(e)}")
        return None