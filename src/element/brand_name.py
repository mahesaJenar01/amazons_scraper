from typing import Optional
from selenium import webdriver

def get_brand_name(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get brand name text for a specific data-index using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div[data-cy="title-recipe"]`);

        if (!definiteContainer) return null;

        const similarity = 'div.a-row.a-color-secondary h2.a-size-mini.s-line-clamp-1'
        const selectors = [
            'span.a-size-base-plus.a-color-base', 
            'span.a-size-medium.a-color-base'
        ]
        let element = null;

        for (const selector of selectors){
            element = definiteContainer.querySelector(similarity + ' ' + selector)

            if (element) break;
        }

        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting brand name for index {index}: {str(e)}")
        return None