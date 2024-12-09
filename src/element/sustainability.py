from typing import Optional
from selenium import webdriver

def get_sustainability(driver: webdriver.Chrome, index: int) -> Optional[str]:
    """Get brand name text for a specific data-index using JavaScript."""
    try:
        script = """
        const definiteContainer= document.querySelector(`div[data-index="${arguments[0]}"] div.a-section.a-spacing-base div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small`);

        if (!definiteContainer) return null;

        let totalSustainability = definiteContainer.querySelectorAll('div[data-eometric="provenanceCertifications_desktop_cpf_badge_eo"]')

        if (!totalSustainability) return null

        let content= ''
        for (let i = 0; i < totalSustainability.length; i++){
            const element = totalSustainability[i].querySelector('div.a-expander-content.a-spacing-medium.a-expander-inline-content.a-expander-inner div.a-section.a-spacing-mini.s-pc-expander-inner div.a-section.a-spacing-small span.a-size-base.a-color-base')

            content += `Feature ${i + 1}: ${element ? element.textContent.trim() : null}\n`
        }

        return content
        """
        return driver.execute_script(script, index)
        
    except Exception as e:
        print(f"Error getting brand name for index {index}: {str(e)}")
        return None