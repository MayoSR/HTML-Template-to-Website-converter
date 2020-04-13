from selenium import webdriver 
from selenium.webdriver.common.keys import keys 
from selenium.webdriver import Chrome

driver = Chrome(executable_path='C:\Program Files (x86)\Chrome Driver\chromedriver.exe')

driver.get("localhost:5000")
driver.title

# Get all the elements available with tag name
buttons = driver.find_elements_by_tag_name('button')
for e in buttons:
    print(e.text)
    print(e.size)
    print(e.location)

inputs = driver.find_elements_by_tag_name('input')
for e in inputs:
    print e.text
    print e.size
    print e.location

# manually upload file
# click each button
convert = driver.find_element_by_id('sbt')
convert.click()

# buttons = driver.find_element_by_xpath('/html/body/div/div[2]/input')
# child_elements = buttons.find_elements_by_xpath('./html/body/div')
# for e in child_elements:
#     print(e.tag_name)
#     print(e.text)
#     print(e.location)



# Store iframe web element
# iframe = driver.find_element_by_tag_name("iframe")

# switch to selected iframe
# driver.switch_to.frame(iframe)
# child_elements = driver.find_elements_by_xpath('.//*')
# iframe_elements = driver.find_elements_by_tag_name('button')

# driver.switch_to.default_content

preview = driver.find_element_by_id('previewframe')
# driver.execute_script('document.getElementById(\'file-btn\').value=\'" + "C:\Users\Prerna\Downloads\img.jpg" + "\';"')
preview.click()

download = driver.find_element_by_id('down-btn')
download.click()

delete = driver.find_element_by_id('del-btn')
delete.click()
