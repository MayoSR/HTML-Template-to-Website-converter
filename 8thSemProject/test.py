from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


driver = Chrome(executable_path='C:\Program Files (x86)\Chrome Driver\chromedriver.exe')

# exec(open("server.py").read())

driver.get("localhost:5000")
driver.title

# Get all the elements available with tag name
buttons = driver.find_elements_by_tag_name('button')
# for e in buttons:
#     print(e.text)
#     print(e.size)
#     print(e.location)

inputs = driver.find_elements_by_tag_name('input')
# for e in inputs:
#     print e.text
#     print e.size
#     print e.location

# upload file
upload = driver.find_element_by_id('file-btn')
upload.send_keys("C:\\Users\\Prerna\\Downloads\\Samples\\sample21.jpg")

slide = driver.find_element_by_id('overlay-iframe')
slide.click()

# click each button
convert = driver.find_element_by_id('sbt')
convert.click()

# clicking delete button
# delete = driver.find_element_by_id('del-btn')
# delete.click()
# alert = driver.switch_to.alert
# alert.accept()
# print('deleted')
# driver.switch_to.default_content()
# upload = driver.find_element_by_id('file-btn')
# upload.send_keys("C:\\Users\\Prerna\\Downloads\\Samples\\sample21.jpg")
# driver.implicitly_wait(60) # seconds

# Store iframe web element
iframe = driver.find_element_by_tag_name("iframe")
# switch to selected iframe
driver.switch_to.frame(iframe)

timeout = 10
try:
    element_present = EC.presence_of_element_located((By.ID, 'input3'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")

child_elements = driver.find_elements_by_xpath('.//*')
# for e in child_elements:
#     print(e.tag_name)
example_element = driver.find_element_by_tag_name('input')
example_element.click()

driver.switch_to.default_content()
modify = driver.find_element_by_id('mod-btn')
modify.click()
print('modified')

driver.implicitly_wait(60) # seconds

preview = driver.find_element_by_id('previewframe')
preview.click()
print('previewed')

driver.implicitly_wait(30) # seconds
driver.switch_to.window(driver.window_handles[0])

download = driver.find_element_by_id('down-btn')
download.click()
print('downloading')

# driver.implicitly_wait(60) # seconds

# delete = driver.find_element_by_id('del-btn')
# delete.click()
# print('deleted')

# driver.quit()
