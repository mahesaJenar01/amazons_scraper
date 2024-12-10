from typing import Optional
from selenium import webdriver

def get_prices(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get price text for a specific data-index using JavaScript."""
    try:
        # The definiteContainer is definitely existed at all cost. The rest are possibility. The most commmon is the selector2.
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"]`);

        if (!definiteContainer) return null;

        const selector1= definiteContainer.querySelector('div[data-cy="secondary-offer-recipe"] div.a-row.a-size-base.a-color-secondary span.a-color-base');
        const selector2= definiteContainer.querySelector('div[data-cy="price-recipe"] span.a-price span.a-offscreen');

        let element= selector1 || selector2;
        return element ? element.textContent.trim() : null;
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting price for index {index}: {str(e)}")
        return None