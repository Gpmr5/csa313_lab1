from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    driver.get("https://student.must.edu.mn")
    driver.maximize_window()
    time.sleep(2) 

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    username.send_keys("B232270015")  
    password.send_keys("Gteb10140917")  

    # Login товчийг дарах
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-primary.btn-block"))
    )
    login_button.click()
    
    time.sleep(3) 
    try:
        close_popup = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".popup-close, .close, .modal-close"))
        )
        close_popup.click()
    except TimeoutException:
        pass  
    

    try:
        driver.find_element(By.ID, "logout")  
        print("Амжилттай нэвтэрлээ!")
    except NoSuchElementException:
        print("Нэвтрэлт амжилтгүй. Алдаа гарсан байна.")

    actions = ActionChains(driver)
    actions.move_by_offset(200, 300).click().perform()
    
    oyutan_menu = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[span[text()="ОЮУТАН"]]'))
    )
    oyutan_menu.click()
    personal_info_menu = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[span[text()="Хувийн мэдээлэл"]]'))
    )
    personal_info_menu.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.rows > li'))
    )

    list_items = driver.find_elements(By.CSS_SELECTOR, 'ul.rows > li')

    for item in list_items:
        print(item.text)
        
    student_data = {
        "major": "",
        "studentID": ""
    }

    for item in list_items:
        try:
            title_element = item.find_element(By.CSS_SELECTOR, '.title')
            title_text = title_element.text

            text_elements = item.find_elements(By.CSS_SELECTOR, '.text')
            texts = [el.text for el in text_elements]

            if "Мэргэжил" in title_text:
                student_data["major"] = " ".join(texts)
            if "Оюутны код" in title_text:
                student_data["studentID"] = texts[0] if texts else ""
        except Exception:
            pass

    print(student_data)
    
    major_expected = "D071405000000002306 ПРОГРАММ ХАНГАМЖИЙН ИНЖЕНЕРЧЛЭЛ"
    studentID_expected = "B232270015"

    assert student_data["major"] == major_expected, "Мэргэжил таарахгүй байна!"
    print(f"Profession is correct: {student_data['major']}")

    assert student_data["studentID"] == studentID_expected, "Оюутны код таарахгүй байна!"
    print(f"Student ID is correct: {student_data['studentID']}")

    logout_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//a[span[text()="Гарах"]]'))
    )
    logout_button.click()

except Exception as e:
    print("Error:", e)

finally:
    print("Browser is closed.")  