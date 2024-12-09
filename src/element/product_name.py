import time
from typing import Optional
from selenium import webdriver

def get_product_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get product name text for a specific data-index using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div.a-section.a-spacing-base div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small`);

        if (!definiteContainer) return null;

        const selector1= definiteContainer.querySelector('div[data-cy="title-recipe"] h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 span.a-size-base-plus.a-color-base.a-text-normal');
        const selector2= definiteContainer.querySelector('div[data-cy="title-recipe"] h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-3 span.a-size-base-plus.a-color-base.a-text-normal');

        const element= selector1 || selector2

        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting product name for index {index}: {str(e)}")
        return None