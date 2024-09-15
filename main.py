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
    'KP_UIDz-ssn': '0aQxrcNeYjBkYrSGA0IUmiIdhrwSeLoUFG7eTKN8l2rWH1cpfaRVoAetr3h6ik3oRW4POm8MZTmTFJ2rsLcZEw6U4LtbiO2cSKwvRtVWPgYh35vwWJvrVmD64uOgcR8v5cobXV5RHFIDLusvXRVCmJyiiYtXWsIxMzQUbT1rMZy',
    'KP_UIDz': '0aQxrcNeYjBkYrSGA0IUmiIdhrwSeLoUFG7eTKN8l2rWH1cpfaRVoAetr3h6ik3oRW4POm8MZTmTFJ2rsLcZEw6U4LtbiO2cSKwvRtVWPgYh35vwWJvrVmD64uOgcR8v5cobXV5RHFIDLusvXRVCmJyiiYtXWsIxMzQUbT1rMZy',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    # 'cookie': 'ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; device-id=e75aec2b-9f6a-45bd-8585-325684e1ccae; experiment_=; pid=zAdfeO0gQteR3EwdvManIw; rxVisitor=172614886550717S0UUK9BMOTP7EGAPL4A5G9REERETCE; abTestingAnonymousPID=zAdfeO0gQteR3EwdvManIw; _gcl_au=1.1.1261460882.1726148875; _ga=GA1.1.1996544349.1726148875; _mibhv=anon-1726148876453-4913162035_6593; _fbp=fb.1.1726148877979.83309416726697474; _tt_enable_cookie=1; _ttp=qRgXiEjWS4DFlo_-NnL2tBZn4cQ; addshoppers.com=2%7C1%3A0%7C10%3A1726148801%7C15%3Aaddshoppers.com%7C44%3AOWU2YTY0NjhmYjQ4NGFlZGE0ZmMxZmNiZjgzMjhiN2I%3D%7C0590968691d8fb528fbbb09d12aa8c13d660abfa8cbb39463eb00328f6712991; _clck=1vwylvv%7C2%7Cfp4%7C0%7C1716; _iidt=BonYizeKv/gjvDwQzJQo9W/tZLy5bBPdswJpAyXAQoBf04FrgFFjFb4JvtlSFVGG38fkH+3XesfsXGDGE7DRGSh6YQFevJXL0gI8KDM=; fpPostInitStatus=SuccessfulResponse; _vid_t=32Wrtu0MjaVThYGsNZU3AmadDFyTkWynThKdZAQb2bLJhVL/fXhUg3HWFXifDTQYXOAE5+oTNf1tRwJ4xjL9f9Ra2JshGnxw63YExVE=; fppro_id={"rid":"1726148801954.6LwjS4","vid":"QY9VQsvezRldiCIrr5FY","exp":1726753680213}; _RCRTX03=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _RCRTX03-samesite=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; dtSa=-; RT="z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m0zf52zy&sl=1&tt=9it&rl=1&ld=9iz&ul=ch8&hd=d0b"; bm_sz=78528120793233C1EB848C8F569C3E2E~YAAQbqfLF6BUhdiRAQAAcE7B5hl0fc1NOkTfcsSnQS5u6IontgFsz6V7M2YEWwSAVSG1olA91sW9ECnbOOTCx0XxID6y63yK0TWZ7BbIKH9rcXblAzXj/6PNl4PasndpCwIkLhtCyzxH0SjaQxanBnRz1xOn3rU3Fphq02Vkk/6SdhDve+9C7iJH5/vSIXkkDs3wT/KoRiU/eo3FhagN2Yu4RoC8ax2yWfSWoEhicAerAHPkg0BcfobAZZclVNTjCK+joXcHBSKVX8+kwj2Bo51KOl5IR9caUftEHl7T1ns6XnhIgY1IfFBCJVQVVIskaV5Kx1AEoZ/tyHNEDe7tHS7HScp4MhjP1Q+boQwrlILbYSKTDN4WFrzwnxgQStIIqJLO4VfUVHT3y8ChTxU959hgTbW6IJrOsuV+wvy+3GB7tEeVD8+vCb5lg3nDCS4sQW96gLtbwQCqj/8DYVxUoy2WfolyoPCNAt9IPfLNMZ/VqtwAPqXyWjHtcZ6l+iTnZVytwnIcZNeLEG+fOmA=~3753538~3616837; _ga_18116CKN3R=GS1.1.1726153332.1.1.1726157023.0.0.0; AKA_A2=A; ak_bmsc=9D61CE4116128F659658F0A31489F19F~000000000000000000000000000000~YAAQFARTaCrRyNiRAQAAiT0L5xlhX95NnZ7uR+daDzk0BVbGWwJ7vGW658+6oP2Bk2iM2n3TwflJqR1lor6RMEiPfIgxb//V28oSrwt6bH8DsAwQo0Vn0pwKmSfLszt4+jDtDwoS2bfqlCzmj16SmfzoDHV36JyEOKgmg4pFZCujrEKe+d6FIRHW4IJRMKU91jHxviR9G42MWHdfNmSrhG//W0ttKyEb0Z64WFTtoQ9BHAiCB7ELePV0vH2eTwUwTVCPGrSGXKEJCcWzGm9yG/0610FSGZjq8C5g03ydsqxQPhOeFWmvNDCtizVs/LEok4Iiqev+WrXhKORFuLO3uo6uQscyugBXxnf8X13N9b/mErhI2VJl8kylpUEJXFyiqqzbPEwBiC+M781SX18hkMG9GI42DBFslu8UgsG3jhvtDQ==; KP_UIDz-ssn=0389xa5rg2IXOa4VqRsfS97BoGyMKvxlnOyh1HZlUYkfxOFYQvTlaYJMSZfpiF6b1y0pfnmqqFnmYOfyf4BaSxaia5cwF8uaufrQrk4VpjID6SQGxDdUamsdF70WKNzY3E9ONgppS2XmHNrA74RFlMdolO7CFuZY8yon0SP3z9; KP_UIDz=0389xa5rg2IXOa4VqRsfS97BoGyMKvxlnOyh1HZlUYkfxOFYQvTlaYJMSZfpiF6b1y0pfnmqqFnmYOfyf4BaSxaia5cwF8uaufrQrk4VpjID6SQGxDdUamsdF70WKNzY3E9ONgppS2XmHNrA74RFlMdolO7CFuZY8yon0SP3z9; bm_mi=E1ADE3AA085676CACDEC847481DD5D32~YAAQBwRTaGnZqciRAQAAjjkN5xnkh47hed1Esdp5Kvl4kNNQST69EgzaLrDbtveQLc9CPDDLj/FeidN6jYhDK2Qdy5Nwe0hr5E56ktw0UxpU1/lrQKMeqGpVUlbxTYSGf+opZ8O0hR9PUP75CN9PI0um/IWfBwazMXKFG/X3QlNDE0hpWunjdYEW/EHfzQkf+Ys1lC2CtFxoiaHmscX/3OfUSlemGWQ6YwHqyzSrOPtcNdPmprHaVAzCMUjKVcyxLstVabrejNxQmYzNiu27hrf+7dLjcHAdwoG8Wggi2pYKP2k/NF/zdVcn7/Y=~1; bm_sv=5E41C54131A0D1812152475B2BF7F768~YAAQBwRTaGrZqciRAQAAjjkN5xnFavmjNzC+BYkJ3pMu+Uad/pvpI9Sb3qu4H/yJ0Pj4RXUlAZfTI42hKXIue7p/mfC2B0TGbn9a9EGLGE4JORt5beWSf8cZQpzWfTkJL8pJfUUcjSfYNYxT6dFYgX6mFdXCbkqxxAAIcXdO41eErY7vIv1Cf9D862pGfWNbBmFYehwjA1V+tr0/7fI+gr68bGt26aNHztMlKITbJWU5Yv8qTk6o4yN4wG2Q908=~1; chewy-insights=ts=https://www.chewy.com/; pageviewCount=13; pageviewCount30m=1; _uetsid=9e4ceb80710d11ef96a5e78feb9245ee; _uetvid=9e4d37e0710d11efae7c991463647fcd; dtPC=-63$558371360_293h-vOGQPNWVKMVRMCURGPODCEHFWFKVEPOFE-0e0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+12+2024+18%3A26%3A12+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; dtCookie=v_4_srv_10_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; _clsk=5lnfs%7C1726158372866%7C2%7C0%7Co.clarity.ms%2Fcollect; _abck=5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaDbdqciRAQAAXr0N5wyxtBwdLFljBUjfWnnNg7T1scuz2TazTdvdgGWtnNdYpdRz6HLU4w5x8INsC5lHv85oFcZLR0f490Jkvw4xorGX6m48sMfAXImEY3l46YbxEpXGjEeM05QjWSysMq2PpkThNhw0jqSIxzRTVYHdFRjFZSSA6rYLqps7WlEDwaG6ZQzPYytUm41O7XLxqRyNDGb6Cg6EMQl/zjvZGdqtMhkr3i0qhGyeVY2yx4d2Pbjf3j3xMy78x0tiGPyeJzV1j8VHLHPoJ5WJ1AJ2poasEbRyUsGeoqvS7ASr3K8gVHOmMal6OaOYFPuS5sCiZCWRLWc2cvbeN15O9/xbpZ+B1Ouw8gYJzTyHFAwfgKf0FTW+uhxPMx4gKGxmKOceUjseGfMxPvSf8Bxey2FmZ9i7SnMAgfa6xIjvQvwPFPv1Jnu2oe2WQRzKWYlHAaFFlLVzVqhT/EBI9LsOSLg9wH0U0H7o5HxZaevltkhB~-1~-1~-1; _ga_GM4GWYGVKP=GS1.1.1726157012.3.1.1726158400.30.0.0; akavpau_defaultvp=1726158625~id=632719299b032801a11bcee4b3a697cf; akaalb_chewy_ALB=1726158925~op=prd_chewy_lando:www-prd-lando-use1|prd_kasada:prd-kasada-haproxy-use2|chewy_com_ALB:www-chewy-use1|~rv=53~m=www-prd-lando-use1:0|prd-kasada-haproxy-use2:0|www-chewy-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=fb92201113796bcd1cd3fec689227a16; rxvt=1726160204055|1726157001414',
    'priority': 'u=0, i',
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
            max_page = soup.find_all('li', class_= 'kib-pagination-new__list-item')[-1].find('a')['aria-label'].replace("Page", "").strip()
            
            st.write("Scraping in progress...")
            
            st.write("Getting links..")
            for i in stqdm(range(int(2))):
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
    
    
