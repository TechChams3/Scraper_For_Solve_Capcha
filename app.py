from selenium import webdriver
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service



service = Service('/home/karol/Job_Codes/For_Main_app/chromedriver')

driver = webdriver.Chrome(service=service)


driver.get('https://www.amazon.com/errors/validateCaptcha')

link = driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')

captcha = AmazonCaptcha.fromlink(link)

captcha_value = AmazonCaptcha.solve(captcha)

input_field = driver.find_element(By.ID,"captchacharacters").send_keys(captcha_value)

button = driver.find_element(By.CLASS_NAME,"a-button-text")

button.click()







# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from amazoncaptcha import AmazonCaptcha

# def solve_captcha(captcha_image_url):
#     """Solves a captcha using the AmazonCaptcha library."""
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     service = Service('/home/karol/Job_Codes/For_Main_app/chromedriver')
#     driver = webdriver.Chrome(service=service, options=options)
    
#     try:
#         # Download the captcha image
#         driver.get(captcha_image_url)
#         captcha_image_path = "captcha_image.png"
        
#         # Save the captcha image
#         with open(captcha_image_path, "wb") as file:
#             file.write(driver.find_element(By.TAG_NAME, "img").screenshot_as_png)
        
#         # Use AmazonCaptcha to solve the captcha
#         captcha = AmazonCaptcha(captcha_image_path)
#         captcha_text = captcha.solve()

#         return captcha_text, driver  # Return the driver for further use

#     except Exception as e:
#         print(f"Error occurred while solving captcha: {str(e)}")
#         return None, driver

#     finally:
#         if os.path.exists(captcha_image_path):
#             os.remove(captcha_image_path)
    
# def interact_with_amazon(driver, captcha_solution):
#     """Interacts with Amazon after solving the CAPTCHA."""
#     # Example: enter the CAPTCHA solution and submit the form
#     try:
#         captcha_input = driver.find_element(By.ID, "captcha-input-id")  # Replace with actual ID
#         captcha_input.send_keys(captcha_solution)
#         submit_button = driver.find_element(By.ID, "submit-button-id")  # Replace with actual ID
#         submit_button.click()

#         # Continue with further interactions (e.g., searching for products)
#         # driver.get("https://www.amazon.com/s?k=your_search_term")
#         # Add more actions as needed...

#     except Exception as e:
#         print(f"Error during interaction: {str(e)}")

# # Example usage
# if __name__ == "__main__":
#     captcha_image_url = "https://images-na.ssl-images-amazon.com/captcha/yniigayf/Captcha_qrztemjyxp.jpg"  # Replace with actual URL
#     captcha_solution, driver = solve_captcha(captcha_image_url)
    
#     if captcha_solution:
#         print(f"Solved Captcha: {captcha_solution}")
#         interact_with_amazon(driver, captcha_solution)
#     else:
#         print("Failed to solve captcha.")




