from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def verify_org_number(org_number):
    """
    This function checks if a given organization number is valid using the validate_org_number 
    function and then verifies it by accessing a specific website using Selenium.
    """
    
    # Validate the organization number format first
    if not validate_org_number(org_number):
        return False
    
    # Set Chrome browser options
    options = Options()
    options.add_argument("--headless")  # This ensures that the Chrome GUI does not show up
    
    # Initialize the Chrome webdriver with the given options
    driver = webdriver.Chrome(options=options)
    
    # Direct the webdriver to the specific website URL
    driver.get(f"https://anskaffelser.no/verktoy/veiledere/mottakere-i-elma#argument=undefined&query={org_number}&page=1")
    
    try:
        # Explicitly wait up to 10 seconds for a specific element to load on the website
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//*[@id='elma-registry-block']/strong"))
        )
        
        # Get the text content of the element
        text_value = element.text
        max_retries = 10
        retries = 0
        
        # If the text value is not available immediately, retry a few times with short intervals
        while text_value == "" and retries < max_retries:
            sleep(0.1)
            text_value = element.text
            retries += 1
        
        # Close the browser session
        driver.quit()
        
        # Return True if the text value is '1', otherwise return False
        return text_value == '1'
                
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()  # Close the browser session in case of an error
        return False
        

def validate_org_number(org_number):
    """
    Validates the format and structure of an organization number using the modulus 11 algorithm.
    """
    
    # Check the format of the organization number
    if not isinstance(org_number, str) or not org_number.isdigit() or len(org_number) != 9:
        return False
    
    # Convert the organization number string to a list of individual digits
    digits = [int(x) for x in org_number]
    
    # Define the weights for the modulus 11 algorithm
    weights = [3,2,7,6,5,4,3,2]
    
    # Compute the sum of products of the digits and the weights
    product_sum = sum(digit * weight for digit, weight in zip(digits[:-1], weights))
    
    # Calculate the remainder when dividing by 11
    remainder = product_sum % 11
    
    # Determine the control digit based on the remainder
    if remainder == 0:
        control_digit = 0
    elif remainder == 1:
        # The control digit cannot be a minus sign
        return False
    else:
        control_digit = 11 - remainder
    
    # Return True if the calculated control digit matches the last digit of the organization number
    return control_digit == digits[-1]
