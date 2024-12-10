import time
from typing import Optional
from selenium import webdriver

def get_product_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get product name text for a specific data-index using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div[data-cy="title-recipe"]`);

        if (!definiteContainer) return null;

        const selectors= [
            'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 span.a-size-base-plus.a-color-base.a-text-normal', 
            'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-3 span.a-size-base-plus.a-color-base.a-text-normal', 
            'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 span.a-size-medium.a-color-base.a-text-normal', 
            'h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal span', 
            'h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span'
        ]

        let element= null
        for (const selector of selectors){
            element = definiteContainer.querySelector(selector);

            if (element) break;
        }

        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting product name for index {index}: {str(e)}")
        return None