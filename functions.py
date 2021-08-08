from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from database import *
from os import path

cwd = os.getcwd()
chrome_driver_file = (path.join(os.getcwd(), "storage", "chromedriver.exe"))
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2,
                                                    'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                    'media_stream_mic': 2, 'media_stream_camera': 2,
                                                    'protocol_handlers': 2,
                                                    'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                    'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop': 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement': 2,
                                                    'durable_storage': 2}}

options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument(('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'))


def open_driver():
    try:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        driver.maximize_window()

        return driver
    except Exception as e:
        # print("error", e)
        return {"success": False, "error": e}


def close_driver(driver):
    driver.quit()
    return {"success": True}


def search_for_link():
    link_list = []
    all_objects = Links.objects(websiteName="www.extraspace.com")
    for obj in all_objects:
        link_list.append(obj.link)
        # print(obj.Link)
    return {"success": True, "data": link_list}


def multi_list(link_list_number):
    links = search_for_link()["data"]
    links_length = len(links)
    if links_length == 0:
        return False
    else:
        result = links_length / link_list_number
        divideNum = int(result)
        mod = links_length % link_list_number
        a_list = []
        extra = False
        for i in range(link_list_number):
            list_of_list = []
            if i < mod:
                divideNum += 1
                extra = True
            for j in links[:divideNum]:
                list_of_list.append(j)
            del links[:divideNum]
            a_list.append(list_of_list)
            if extra:
                divideNum -= 1
                extra = False
        return {"success": True,"data":a_list}


def check_items(driver, _id):

    try:

        item_size_path = """//div[@style="height: auto; overflow: visible;"]//div//div[@data-qa="unit-class-card"]/div/div/div[normalize-space(.) = "10' x 10'"]"""
        item_size = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, item_size_path))).text
        # print(item_size)
    except:
        print("No item found")
        item_size_path = False
        item_size = False

    if item_size == "10' x 10'":
        print("size: ", item_size)
        try:
            # path = """//div[@style="height: auto; overflow: visible;"]//div//div[@data-qa="unit-class-card"]/div/div/div[normalize-space(.) = "10' x 10'"]//parent::div/following-sibling::div/ul/li/span[contains(text(),"Indoor")]"""
            indoor_access = item_size_path + '//parent::div/following-sibling::div/ul/li/span[contains(text(),"Indoor")]'
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, indoor_access)))
            result = "Indoor"
        except:
            try:
                first_floor_access = item_size_path + '//parent::div/following-sibling::div/ul/li/span[contains(text(),"1st Floor Access")]'
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, first_floor_access)))
                result ="1st Floor Access"

            except:
                result = "outside_access"

        if result == "Indoor":
            # path="""//div[@style="height: auto; overflow: visible;"]//div//div[@data-qa="unit-class-card"]/div/div/div[normalize-space(.) = "5' x 10'"]//parent::div/following-sibling::div/ul/li/span[contains(text(),"Indoor")]//parent::li/preceding-sibling::li//child::span[contains(text(),"Climate Controlled")]"""
            check_climate = f"""({item_size_path}//parent::div/following-sibling::div/ul/li/span[contains(text(),"Indoor")])[1]//parent::li/preceding-sibling::li//child::span[contains(text(),"Climate Controlled")]"""
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, check_climate)))

                climate_control = True
            except:
                climate_control = False

            price_path = f"""({item_size_path}//parent::div/following-sibling::div/ul/li/span[contains(text(),"Indoor")])[1]//parent::li//parent::ul//parent::div/following-sibling::div[@data-qa="web-rate"]/div[1]"""
            item_price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            price = item_price.replace("$", "")
            print("climate_control: ", climate_control)
            print("price: ", price)
            push_records(_id, item_size, climate_control, float(price))

        elif result == "1st Floor Access":
            check_climate = f"""({item_size_path}//parent::div/following-sibling::div/ul/li/span[contains(text(),"1st Floor Access")])[1]//parent::li/preceding-sibling::li//child::span[contains(text(),"Climate Controlled")]"""
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, check_climate)))

                climate_control = True
            except:
                climate_control = False

            price_path = f"""({item_size_path}//parent::div/following-sibling::div/ul/li/span[contains(text(),"1st Floor Access")])[1]//parent::li//parent::ul//parent::div/following-sibling::div[@data-qa="web-rate"]/div[1]"""
            item_price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            price = item_price.replace("$", "")
            print("climate_control: ", climate_control)
            print("price: ", price)
            push_records(_id, item_size, climate_control, float(price))

        else:
            # path="""(//div[@style="height: auto; overflow: visible;"]//div//div[@data-qa="unit-class-card"]/div/div/div[normalize-space(.) = "10' x 10'"])[1]//parent::div/following-sibling::div/ul/li/span[contains(text(),"Climate Controlled")]"""
            check_climate = f"""({item_size_path})[1]//parent::div/following-sibling::div/ul/li/span[contains(text(),"Climate Controlled")]"""
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, check_climate)))

                climate_control = True
            except:
                climate_control = False

            price_path = f"""({item_size_path})[1]//parent::div/following-sibling::div[@data-qa="web-rate"]/div[1]"""
            item_price = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, price_path))).text
            price = item_price.replace("$", "")
            print("climate_control: ", climate_control)
            print("price: ", price)
            push_records(_id, item_size, climate_control, float(price))

    else:
        pass

# check_items()
def runBot(links_list):
    driver = open_driver()
    for link in links_list:
        driver.get(link)
        objcts = Links.objects.get(link=link)
        owner_id = objcts.id
        print("link: ", link)
        check_items(driver, owner_id)
        print("======================data===========================")
    close_driver(driver)
