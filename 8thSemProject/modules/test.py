from selenium import webdriver 
from selenium.webdriver.common.keys import keys 
from selenium.webdriver import Chrome

driver = Chrome(executable_path='C:\Program Files (x86)\Chrome Driver\chromedriver.exe')

driver.get("http://127.0.0.1:5000/")
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
preview = driver.find_element_by_id('previewframe')
# driver.execute_script('document.getElementById(\'file-btn\').value=\'" + "C:\Users\Prerna\Downloads\img.jpg" + "\';"')
preview.click()

# Store iframe web element
# iframe = driver.find_element_by_tag_name("iframe")

# switch to selected iframe
# driver.switch_to.frame(iframe)
# iframe_elements = driver.find_elements_by_tag_name('button')
  

convert = driver.find_element_by_id('sbt')
convert.click()

download = driver.find_element_by_id('down-btn')
download.click()

delete = driver.find_element_by_id('del-btn')
delete.click()

# buttons = driver.find_element_by_xpath('/html/body/div/div/div[2]/iframe')
# child_elements = buttons.find_elements_by_xpath('.//*')
# for e in child_elements:
#     print(e.tag_name)
#     print(e.text)
#     print(e.location)