import streamlit as st
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font
import time
import json
from stqdm import stqdm
import pandas as pd 

st.title("Chewy scraper")

cookies = {
    'ajs_anonymous_id': '47dd1547-3473-403a-9b46-f53f1e5c8516',
    'device-id': 'e75aec2b-9f6a-45bd-8585-325684e1ccae',
    'experiment_': '',
    'pid': 'zAdfeO0gQteR3EwdvManIw',
    'rxVisitor': '172614886550717S0UUK9BMOTP7EGAPL4A5G9REERETCE',
    'abTestingAnonymousPID': 'zAdfeO0gQteR3EwdvManIw',
    '_gcl_au': '1.1.1261460882.1726148875',
    '_ga': 'GA1.1.1996544349.1726148875',
    '_mibhv': 'anon-1726148876453-4913162035_6593',
    '_fbp': 'fb.1.1726148877979.83309416726697474',
    '_tt_enable_cookie': '1',
    '_ttp': 'qRgXiEjWS4DFlo_-NnL2tBZn4cQ',
    'addshoppers.com': '2%7C1%3A0%7C10%3A1726148801%7C15%3Aaddshoppers.com%7C44%3AOWU2YTY0NjhmYjQ4NGFlZGE0ZmMxZmNiZjgzMjhiN2I%3D%7C0590968691d8fb528fbbb09d12aa8c13d660abfa8cbb39463eb00328f6712991',
    '_iidt': 'BonYizeKv/gjvDwQzJQo9W/tZLy5bBPdswJpAyXAQoBf04FrgFFjFb4JvtlSFVGG38fkH+3XesfsXGDGE7DRGSh6YQFevJXL0gI8KDM=',
    'fpPostInitStatus': 'SuccessfulResponse',
    '_vid_t': '32Wrtu0MjaVThYGsNZU3AmadDFyTkWynThKdZAQb2bLJhVL/fXhUg3HWFXifDTQYXOAE5+oTNf1tRwJ4xjL9f9Ra2JshGnxw63YExVE=',
    'fppro_id': '{"rid":"1726148801954.6LwjS4","vid":"QY9VQsvezRldiCIrr5FY","exp":1726753680213}',
    '_RCRTX03': 'd3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8',
    '_RCRTX03-samesite': 'd3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8',
    '_ga_18116CKN3R': 'GS1.1.1726153332.1.1.1726157023.0.0.0',
    'sid': '8f545594-8556-4c17-b1c6-c828b261e93b',
    'x-feature-preview': 'false',
    'ajs_anonymous_id': '47dd1547-3473-403a-9b46-f53f1e5c8516',
    'KP_UIDz-ssn': '0a4RJMw9qeIxlLDhFFEhJrh17mLS9onFYtcfXPRPruzOSof8KNgUJ3mTxEPo7RU9BZBr0JX3NwTJQ9GSlApIXiISzxHTEvV34DOG2cWdrZvVGisdFpYcZPivYPuTlvRQ9iZdwCsVVtES3mhKPHA1gKUOqrPcyb10hbf2CbGruDZ',
    'KP_UIDz': '0a4RJMw9qeIxlLDhFFEhJrh17mLS9onFYtcfXPRPruzOSof8KNgUJ3mTxEPo7RU9BZBr0JX3NwTJQ9GSlApIXiISzxHTEvV34DOG2cWdrZvVGisdFpYcZPivYPuTlvRQ9iZdwCsVVtES3mhKPHA1gKUOqrPcyb10hbf2CbGruDZ',
    'pageviewCount': '130',
    '_abck': '5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaMty2/ORAQAAsbB9/AzCHqIOSpNJeWTDPF2DqEtnwkK86z4G28LzgY/a8kRM63vccXLzhqwhwFAilpIbJhrTiHsxdQyfRN+0CMqBh3SPhl/nA4RRFa30qr0PBvnwCiT+jAvdatsKfBoxSESWK3j8/0pWKW6StiS7fepfAfwjx/V3W+W0jn/fwUTgEl0O/krh2UxqH5z4dBn/FewMWsrYBcJk/Xry2sAGt/P2Pj9TkJ5HWbjxYFbQwvStjQ5stS3Hxk3/RMvLjqpCEpWm4OLhTgShKZbZetNI1C/uRidIvxcJatBdH2An34LbazDH+movQtH6FZPUSEohN8fHv9YLneiE1wNah1P+FdDGe6w5p6Gjl7iGddV3Pf2737jyNHzZGhyiTkHTyQA8zdBZL/Vca/S8oWAnPKW2Np0LNItrLNzOna3xE0n6BwMaYIQNreerRV0syJqqSEOZYt38p33hJ6QmXDAgZ8ZxtG0L2Q3/mN002l7fCv92aAwzs857TGF+FrcwExf93EziA6ZZUaM1obry1Q==~-1~||0||~-1',
    '_uetsid': '9e4ceb80710d11ef96a5e78feb9245ee',
    '_uetvid': '9e4d37e0710d11efae7c991463647fcd',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Sep+16+2024+22%3A19%3A43+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    'akavpau_defaultvp': '1726518458~id=5fb879d3657c8bc46f45b8dae944a67d',
    'dtCookie': 'v_4_srv_-2D79_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    '_clck': '1vwylvv%7C2%7Cfp9%7C0%7C1716',
    '_clsk': 'c8wiz7%7C1726560717261%7C1%7C0%7Cu.clarity.ms%2Fcollect',
    '_ga_GM4GWYGVKP': 'GS1.1.1726560722.21.0.1726560722.60.0.0',
    'rxvt': '1726562522056|1726560412217',
    'dtPC': '-79$317979330_358h25vHDEWSRNROKQSORRJCJLUPTRGRMDFKCPV-0e0',
    'RT': '"z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m15g7ygy&sl=1&tt=cop&nu=12cc2c38&cl=pgcro&ld=pgcwp&ul=pgcwq"',
    'dtSa': 'false%7CC%7C25%7CCat%7Cfetch%7C1726560721919%7C317979330_358%7Chttps%3A%2F%2Fwww.chewy.com%2Fpedigree-complete-nutrition-grilled%2Fdp%2F141433%7C%7C%7C%7C',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    # 'cookie': 'ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; device-id=e75aec2b-9f6a-45bd-8585-325684e1ccae; experiment_=; pid=zAdfeO0gQteR3EwdvManIw; rxVisitor=172614886550717S0UUK9BMOTP7EGAPL4A5G9REERETCE; abTestingAnonymousPID=zAdfeO0gQteR3EwdvManIw; _gcl_au=1.1.1261460882.1726148875; _ga=GA1.1.1996544349.1726148875; _mibhv=anon-1726148876453-4913162035_6593; _fbp=fb.1.1726148877979.83309416726697474; _tt_enable_cookie=1; _ttp=qRgXiEjWS4DFlo_-NnL2tBZn4cQ; addshoppers.com=2%7C1%3A0%7C10%3A1726148801%7C15%3Aaddshoppers.com%7C44%3AOWU2YTY0NjhmYjQ4NGFlZGE0ZmMxZmNiZjgzMjhiN2I%3D%7C0590968691d8fb528fbbb09d12aa8c13d660abfa8cbb39463eb00328f6712991; _iidt=BonYizeKv/gjvDwQzJQo9W/tZLy5bBPdswJpAyXAQoBf04FrgFFjFb4JvtlSFVGG38fkH+3XesfsXGDGE7DRGSh6YQFevJXL0gI8KDM=; fpPostInitStatus=SuccessfulResponse; _vid_t=32Wrtu0MjaVThYGsNZU3AmadDFyTkWynThKdZAQb2bLJhVL/fXhUg3HWFXifDTQYXOAE5+oTNf1tRwJ4xjL9f9Ra2JshGnxw63YExVE=; fppro_id={"rid":"1726148801954.6LwjS4","vid":"QY9VQsvezRldiCIrr5FY","exp":1726753680213}; _RCRTX03=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _RCRTX03-samesite=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _ga_18116CKN3R=GS1.1.1726153332.1.1.1726157023.0.0.0; sid=8f545594-8556-4c17-b1c6-c828b261e93b; x-feature-preview=false; ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; KP_UIDz-ssn=0a4RJMw9qeIxlLDhFFEhJrh17mLS9onFYtcfXPRPruzOSof8KNgUJ3mTxEPo7RU9BZBr0JX3NwTJQ9GSlApIXiISzxHTEvV34DOG2cWdrZvVGisdFpYcZPivYPuTlvRQ9iZdwCsVVtES3mhKPHA1gKUOqrPcyb10hbf2CbGruDZ; KP_UIDz=0a4RJMw9qeIxlLDhFFEhJrh17mLS9onFYtcfXPRPruzOSof8KNgUJ3mTxEPo7RU9BZBr0JX3NwTJQ9GSlApIXiISzxHTEvV34DOG2cWdrZvVGisdFpYcZPivYPuTlvRQ9iZdwCsVVtES3mhKPHA1gKUOqrPcyb10hbf2CbGruDZ; pageviewCount=130; _abck=5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaMty2/ORAQAAsbB9/AzCHqIOSpNJeWTDPF2DqEtnwkK86z4G28LzgY/a8kRM63vccXLzhqwhwFAilpIbJhrTiHsxdQyfRN+0CMqBh3SPhl/nA4RRFa30qr0PBvnwCiT+jAvdatsKfBoxSESWK3j8/0pWKW6StiS7fepfAfwjx/V3W+W0jn/fwUTgEl0O/krh2UxqH5z4dBn/FewMWsrYBcJk/Xry2sAGt/P2Pj9TkJ5HWbjxYFbQwvStjQ5stS3Hxk3/RMvLjqpCEpWm4OLhTgShKZbZetNI1C/uRidIvxcJatBdH2An34LbazDH+movQtH6FZPUSEohN8fHv9YLneiE1wNah1P+FdDGe6w5p6Gjl7iGddV3Pf2737jyNHzZGhyiTkHTyQA8zdBZL/Vca/S8oWAnPKW2Np0LNItrLNzOna3xE0n6BwMaYIQNreerRV0syJqqSEOZYt38p33hJ6QmXDAgZ8ZxtG0L2Q3/mN002l7fCv92aAwzs857TGF+FrcwExf93EziA6ZZUaM1obry1Q==~-1~||0||~-1; _uetsid=9e4ceb80710d11ef96a5e78feb9245ee; _uetvid=9e4d37e0710d11efae7c991463647fcd; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+16+2024+22%3A19%3A43+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; akavpau_defaultvp=1726518458~id=5fb879d3657c8bc46f45b8dae944a67d; dtCookie=v_4_srv_-2D79_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; _clck=1vwylvv%7C2%7Cfp9%7C0%7C1716; _clsk=c8wiz7%7C1726560717261%7C1%7C0%7Cu.clarity.ms%2Fcollect; _ga_GM4GWYGVKP=GS1.1.1726560722.21.0.1726560722.60.0.0; rxvt=1726562522056|1726560412217; dtPC=-79$317979330_358h25vHDEWSRNROKQSORRJCJLUPTRGRMDFKCPV-0e0; RT="z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m15g7ygy&sl=1&tt=cop&nu=12cc2c38&cl=pgcro&ld=pgcwp&ul=pgcwq"; dtSa=false%7CC%7C25%7CCat%7Cfetch%7C1726560721919%7C317979330_358%7Chttps%3A%2F%2Fwww.chewy.com%2Fpedigree-complete-nutrition-grilled%2Fdp%2F141433%7C%7C%7C%7C',
    'priority': 'u=0, i',
    'referer': 'https://www.chewy.com/pedigree-complete-nutrition-grilled/dp/141433',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
    
def write_first_row(sh, first_row):
    column = 1
    for field in first_row:
        sh.cell(row=1, column=column).value = field
        sh.cell(row=1, column=column).font = Font(bold=True)
        column = column + 1
        
def get_links(sh, url):

    links = []
    for row in sh: 
        name = row[0].value.replace('https://www.chewy.com/', '').split('/')[0].replace('/', '')
        links.append(name)
    
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    items = soup.find_all("div", class_="kib-product-card")
    
    for item in items:
        link = item.find("a", class_="kib-product-title")["href"]
        
        link_stripped = link.replace('https://www.chewy.com/', '').split('/')[0]
        
        if link_stripped not in links:
        
            row = sh.max_row + 1
            
            if 'chewy.com' not in link:
                sh.cell(row=row, column=1).value = 'https://www.chewy.com' + link
            elif 'api/event' in link:
                sh.cell(row=row, column=1).value = link.split('redirect=')[1].strip()
            else:
                sh.cell(row=row, column=1).value = link
            
            links.append(link_stripped)

    time.sleep(1)
    
def get_details(sh_details, url, id_for_items):

    link_for_items = "https://www.chewy.com/_next/data/chewy-pdp-ui-"+id_for_items+"/en-US/"+url.replace("https://www.chewy.com/", "")+".json?id="+url.split('/')[-1]+"&slug="+url.split('/')[-3]
    
    response_items = requests.get(link_for_items, cookies=cookies, headers=headers)
    soup_items = BeautifulSoup(response_items.text, 'html.parser')
    
    if "__N_REDIRECT" in json.loads(soup_items.text)["pageProps"]:
        new_link = "https://www.chewy.com/_next/data/chewy-pdp-ui-"+id_for_items+"/en-US/" + json.loads(soup_items.text)["pageProps"]["__N_REDIRECT"] + ".json?id="+url.split('/')[-1]+"&slug="+url.split('/')[-3]
        response_items = requests.get(link_for_items, cookies=cookies, headers=headers)
        soup_items = BeautifulSoup(response_items.text, 'html.parser')
        
    items_json=json.loads(soup_items.text)["pageProps"]["__APOLLO_STATE__"]
    items = [key for key, val in items_json.items() if "Item" in key]
    
    products = [key for key, val in items_json.items() if "Product" in key]
    manufacturer = items_json[products[0]]["manufacturerName"]
    
    swatches_list = {}
    swatch_types = [val for key, val in items_json.items() if "MDA:" in key]
    for st in swatch_types:
        if "isEnsemble" in st:
            #print(st)
            new_swatch = []
            title = st["name"]
            options = st["options"]
            for option in options:
                swatch_variant = json.loads(('{' + option["__ref"] + '}').replace('AttributeValue', '"AttributeValue"'))["AttributeValue"]["value"].strip()
                new_swatch.append(swatch_variant)
            swatches_list[title] = new_swatch
            if title not in first_row:
                first_row.append(title)
                write_first_row(sh_details, first_row)
    
    categories = [val["name"] for key, val in items_json.items() if "Breadcrumb" in key]
    details_short = ''
    
    for item in items:
        if ("inStock" in items_json[item] and items_json[item]["inStock"] == True) or ("isInStock" in items_json[item] and items_json[item]["isInStock"] == True):            
            row = sh_details.max_row + 1            
            attributeValues = items_json[item]['attributeValues({"includeEnsemble":true,"usage":["DEFINING"]})']
            for attr in attributeValues:
                variants = json.loads(('{' + attr['__ref'] + '}').replace('AttributeValue', '"AttributeValue"'))
                variant = variants["AttributeValue"]["value"].strip()
                for swatch in swatches_list:
                    if variant in swatches_list[swatch]:
                        index = first_row.index(swatch)
                        sh_details.cell(row=row, column=index+1).value = variant
            
            details_long = items_json[item]["description"]
            details_short = ''
            if "keyBenefits" in items_json[item] and items_json[item]["keyBenefits"] != None:
                for benefit in items_json[item]["keyBenefits"]:
                    details_short = details_short + " " + benefit
            sh_details.cell(row=row, column=11).value = str(details_short) + " " + details_long
            sh_details.cell(row=row, column=2).value = items_json[item]["name"]
            sh_details.cell(row=row, column=3).value = manufacturer
            sh_details.cell(row=row, column=4).value = items_json[item]["advertisedPrice"]
            if "strikeThroughPrice" in items_json[item]:
                sh_details.cell(row=row, column=5).value = items_json[item]["strikeThroughPrice"]
            sh_details.cell(row=row, column=12).value = items_json[item]["partNumber"]
            sh_details.cell(row=row, column=1).value = url.replace(url.split('/')[-1], items_json[item]["entryID"])
            
            for category in range(len(categories)):       
                sh_details.cell(row=row, column=6+category).value = categories[category]
            
            images = []
            
            if "images" in items_json[item]:
                for image in items_json[item]["images"]:
                    images.append(image['url({"autoCrop":true,"sideLongest":1800})'])
            else:
                images.append(items_json[item]["fullImage"]['url({"autoCrop":true,"square":1800})'])
            
            
            for image in range(len(images)):
                sh_details.cell(row=row, column=13+image).value = images[image]
    
if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_stage(stage):
    st.session_state.stage = stage

workbook = openpyxl.Workbook()
sh = workbook.active
workbook_details = openpyxl.Workbook()
sh_details = workbook_details.active

first_row = ["URL", "Product Title", "Manufacturer", "Price", "Regular Price", "Category 1", "Category 2", "Category 3", "Category 4", "Category 5", "Details", "Item Number", "Photo1", "Photo2", "Photo3", "Photo4", "Photo5", "Photo6", "Photo7", "Photo8", "Photo9", "Photo10", "Photo11", "Photo12", "Photo13", "Photo14", "Photo15"]
write_first_row(sh, first_row)
write_first_row(sh_details, first_row)

st.write("Write your category here (format: dental-treats-1539):")
category = st.text_input("Category")

st.button('Go!', on_click=set_stage, args=(2,))

if st.session_state.stage > 0:
    
    if st.session_state.stage == 2:
        response = requests.get("https://www.chewy.com/b/" + category, cookies=cookies, headers=headers)
        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')
            max_page = 1
            max_page_container = soup.find_all('li', class_= 'kib-pagination-new__list-item')
            if max_page_container != []:
                max_page = max_page_container[-1].find('a')['aria-label'].replace("Page", "").strip()
            
            st.write("Scraping in progress...")
            
            st.write("Getting links..")
            for i in stqdm(range(int(max_page))):
                url = "https://www.chewy.com/b/" + category.rsplit("-", 1)[0] +"_c" + category.rsplit("-", 1)[1] + "_p" + str(i+1)
                get_links(sh, url)
                time.sleep(1)
            
            workbook.save("chewy.xlsx")

            id_for_items = ""

            st.write("Going through the products...")
            for row in stqdm (range(2, sh.max_row)):    
                url = sh[row+1][0].value

                if row == 2 or row % 50 == 1:
                    response = requests.get(url, cookies=cookies, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')    
                    scripts = soup.find("head").find_all("script")
                    for script in scripts:
                        #print(script)
                        if script.has_attr("src"):
                            if "/static/spa/chewy-pdp-ui/_next/static/chewy-pdp-ui-" in script["src"]:
                                id_for_items = script["src"].replace("/static/spa/chewy-pdp-ui/_next/static/chewy-pdp-ui-", "").replace("/_buildManifest.js", "").replace("/_ssgManifest.js", "")
                                break
                
                if "URL" not in url:
                    try:
                        get_details(sh_details, url, id_for_items)
                    except Exception as e:
                        print(e)
                time.sleep(1)
                
        
                workbook_details.save('chewy_data.xlsx')
            set_stage(1)

        elif (response.status_code == 404):
            st.write("Wrong category!")
        else:
            st.write("An error occured! Status code: " + str(response.status_code))
    
    st.write("Done!")

    with open("./chewy_data.xlsx", "rb") as file:
        st.download_button("Download file", data=file, file_name=("chewy-"+category+".xlsx"), mime="application/vnd.ms-excel")
    
    
