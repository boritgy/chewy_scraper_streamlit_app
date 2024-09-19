import streamlit as st
import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font
import time
import json
from stqdm import stqdm
import pandas as pd 
import hmac

st.title("Chewy scraper")

def check_password():

    def password_entered():
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Wrong password")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

cookies = {
    'device-id': '501d37e6-79ae-465c-b0c7-9766d38d59dc',
    'pid': '4J3Di1eUQcuZ_RD4u85HmA',
    'sid': '1839bb0a-1971-4312-b667-0c883a662da3',
    'x-feature-preview': 'false',
    'abTestingAnonymousPID': 'K9AjefB4QVy6zeKGnFqADg',
    '_gcl_au': '1.1.1916444144.1726562974',
    '_ga': 'GA1.1.39900230.1726562974',
    'rxVisitor': '172656297441797CIT7PKGJ3VDF1O2ETEFSK4KL1U1URM',
    '_fbp': 'fb.1.1726562974779.68070706348477632',
    '_mibhv': 'anon-1726562974923-2204694577_6593',
    'fpGetInitStatus': 'SuccessfulResponse',
    '_tt_enable_cookie': '1',
    '_ttp': 'dTv3piPSJT1P5m5IYcWHUhi4Juj',
    'ajs_anonymous_id': '0e516ba1-4662-4a70-8628-bff483311dd7',
    '_iidt': 'fQzUHXU9waSIkMr7IF1KgUEA1CO1oXIzvULeQAC/qlMIjuKQHWLAiQZCvtdOxOPJcZXpVllCNaQUww==',
    'fpPostInitStatus': 'SuccessfulResponse',
    '_vid_t': '9OV6ytAcv9CN98xyhDvS1JiyrpZSiKFuw3TJXf4hwjckXTiF3xH5k++LrY1fthCHq1sXLJXA+6gSHw==',
    'fppro_id': '{"rid":"1726508880084.MXcdEb","vid":"z8RX4Dez2DdvMwIkaMwe","exp":1727167775921}',
    'addshoppers.com': '2%7C1%3A0%7C10%3A1726508880%7C15%3Aaddshoppers.com%7C44%3AMDhiMWQ4MmU4NmI4NDI2NWJhMzhjNzNmMWQxZTYyNGQ%3D%7C80e05a031f510e961d9c521fa68174f4ab6d12b458840624879e4522863c980e',
    'experiment_': '',
    'dtSa': '-',
    'RT': '"z=1&dm=www.chewy.com&si=e2a4c6f1-b216-4769-9d7d-a662a70d12c5&ss=m17kh8k5&sl=0&tt=0&bcn=%2F%2F17de4c19.akstat.io%2F&ul=1n9f5&hd=1n9gk"',
    'KP_UIDz-ssn': '02o5NozCirX4xGymfsUE9NM1C7coaw4v3KODjryB4zAo06DRxuQn5FJp5hEhcJX0iE4ptAa9BIbbJ4HC66niN9bGWqGNhiingXYdl8R9U1Vr2LE1FRWNKUjFnLY5QDF2CGSJLc7NSODv2Trlq3Ne7rBVsAz9nUucKgy4fQIbTqlS8g1TDbiMeezDKPxqa9v9k79OAvONju49d',
    'KP_UIDz': '02o5NozCirX4xGymfsUE9NM1C7coaw4v3KODjryB4zAo06DRxuQn5FJp5hEhcJX0iE4ptAa9BIbbJ4HC66niN9bGWqGNhiingXYdl8R9U1Vr2LE1FRWNKUjFnLY5QDF2CGSJLc7NSODv2Trlq3Ne7rBVsAz9nUucKgy4fQIbTqlS8g1TDbiMeezDKPxqa9v9k79OAvONju49d',
    'AKA_A2': 'A',
    'ak_bmsc': '68150CBC4BFB424A489C30BB4DC05062~000000000000000000000000000000~YAAQhqEkFxrW7OaRAQAA2B/hCBkBVF4PI4rKXxMnikpMBKaP4PKT2vRjU3G+yepdpvCdhWFiqj0KvnJNZmIwebk9CFJun1OmEFvLikIiQmJpilhgaCmxAGz+WZHiSLxc47Apce4cEC3yGvTwMMd9d8cMOTtNmHVptx3olTv36yVX68xv9QUh71WqQEQpIMpJggw5nfp5Cp3LOfRqkLGaSUyhIR4opTUus6FmJtqZ+RhRbW2sKH60I2bo5j38Q55r6pO8xbV8rXDVEtkkVXH9IuoOyBDqsyyiF/bVXEb15AXlvj4dR9oMVt5798XpEhLcXiX1bUYZzwkoWnH7Cwd1Not+LDwe7yyE8PrQAJzeam+PSZGtCh92ii4LEN/ExNA5N90nUqqZOVdUo9727DfpKoYwSXnLqVcPkgg4/Ffv9KdFpQ==',
    'bm_sz': '995DCC12F7C39FBC44327AE476578694~YAAQhqEkFxzW7OaRAQAA2B/hCBmRSZXoSnj5iFQG9iwX8feFeFP4X6uBHG6AVCquoiOJIeeRNU5vtoBcLcodg0aYzXj8+QOXuzKIQ93Gykr4XuwpzZmJW5mmZHOd0JptCpVgZ9eNxv+Nv/zMXYuHkn0bTt3GwJMjG2M6nBhwZeUHFhUlkEBq7mhuDZXQaFX8/X5UgJEFdhLZFsGQ225Vh8/bCR4sw4gmWmxW/gQZmQAh5+1QBsNTw1R3lRqlZiuCh+dSC1c9ncPa8quobBHW0bdTw3INmbvJWm2I7IY/ffptXSNWgZ+C6vYYQ1zlKCUZKpFHSwFY+GNCYuQwcmwxK8haWXRI+SIdIBykbT2qCnhm5O2tw0ycLXW+NMXH6Gj4qk/hOxH+pFxZaLRlUwSpypaAPSGJcmsJpAPeXEwXYOlQXTSl9k8=~3291449~4277553',
    'chewy-insights': 'ts=https://www.chewy.com/',
    'bm_sv': '97CAB47FDBBA535CCD55900586049254~YAAQhqEkF0fW7OaRAQAA7yXhCBkO5vAJ24Yl3INzTKenOOrWIk84azw382Tjm/PSk3CzQhSDs5j8V1mtvdupOudH86uABHy8TfL0ksBRJvUIG/CoPKW3C6h83dH/SqQHFeALWs1kkiqrkMPyBkeHqEH1eRD3+MbDPGZilPHPACk6dnT1mk7yPjwRPPV+mbrkdRDQUBK9O/C5bpAahC+0d4BtaBBB1iipF0ePJRK2iGuBKL3KFfXD3wQxv3zzg98=~1',
    'pageviewCount': '7',
    'pageviewCount30m': '1',
    '_ga_GM4GWYGVKP': 'GS1.1.1726725829.5.0.1726725829.60.0.0',
    'dtPC': '-68$525830039_613h-vFQJONTADGROLCJHORQTAKLMEASEMDFRE-0e0',
    '_uetsid': 'c38d390074d111efab3fe3763a2d5640',
    '_uetvid': 'c38d6f3074d111efaa4d197904445237',
    'dtCookie': 'v_4_srv_3_sn_P0BCVKEJ8PU0IAQ36NHB98TJMEJCQNOV_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    '_abck': 'D72CA898F39A1BD80917F567A9F1B7E1~-1~YAAQhqEkF/fW7OaRAQAAREjhCAxqYsyZ1dtkmchCZCSyfZoThnk3A+0icIBlzWTUiMBq/u8yIWCShFaCmZFDJ32tiqPBFX05R6mPuvhT+f3gGBaxe6vVzWSaoNZdW1V4iX05QpJsnD5V7JpcEe4ONkh/t1DtcAgWl22FncHQoqRYMrtY67mNKhvBFALvyQD1gwF+tDUZY6xx9ohxwCVE2aFYVEdtOu9nlbJZnnQv9yJZa5pStDrEK0arLsNlcoh5mj8Eaa+ocD4qIRShY85ySMWo74X6OHhZPdIBfCQ5pbxF+XN66sHVzIcYRUmJ52dR4bEzjuIAsaCsprXltbwRnPUX/Pv0a5eMHofr/0Pxki5XfZuY4L7+cNO3klmycVykBELCC7hJTettO3fsBt0Y7aZtT2998HV2d2TNGfqFZbu+P9MnnO5+0GMqgKQvfoz4XQC9KV5EJo/ajEGrCrooOVkZDGuV5s9GHjFSYMDi1yPGTs7cT0qHy2fzX9c4E2Lib/kztxvelaca16WT65lar6sA2/k=~-1~-1~-1',
    'akavpau_defaultvp': '1726726135~id=06549e5fb4e3690ca181c23d842a4258',
    'akaalb_chewy_ALB': '1726726435~op=chewy_com_ALB:www-chewy-use1|prd_kasada:prd-kasada-haproxy-use1|~rv=51~m=www-chewy-use1:0|prd-kasada-haproxy-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=4235d1d85f7e239b9bcb58bb7d5dcde3',
    'rxvt': '1726727636023|1726725830049',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Sep+19+2024+08%3A03%3A56+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    '_clck': '7tp568%7C2%7Cfpb%7C0%7C1720',
    '_clsk': '197b6l1%7C1726725837835%7C1%7C0%7Cs.clarity.ms%2Fcollect',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    # 'cookie': 'device-id=501d37e6-79ae-465c-b0c7-9766d38d59dc; pid=4J3Di1eUQcuZ_RD4u85HmA; sid=1839bb0a-1971-4312-b667-0c883a662da3; x-feature-preview=false; abTestingAnonymousPID=K9AjefB4QVy6zeKGnFqADg; _gcl_au=1.1.1916444144.1726562974; _ga=GA1.1.39900230.1726562974; rxVisitor=172656297441797CIT7PKGJ3VDF1O2ETEFSK4KL1U1URM; _fbp=fb.1.1726562974779.68070706348477632; _mibhv=anon-1726562974923-2204694577_6593; fpGetInitStatus=SuccessfulResponse; _tt_enable_cookie=1; _ttp=dTv3piPSJT1P5m5IYcWHUhi4Juj; ajs_anonymous_id=0e516ba1-4662-4a70-8628-bff483311dd7; _iidt=fQzUHXU9waSIkMr7IF1KgUEA1CO1oXIzvULeQAC/qlMIjuKQHWLAiQZCvtdOxOPJcZXpVllCNaQUww==; fpPostInitStatus=SuccessfulResponse; _vid_t=9OV6ytAcv9CN98xyhDvS1JiyrpZSiKFuw3TJXf4hwjckXTiF3xH5k++LrY1fthCHq1sXLJXA+6gSHw==; fppro_id={"rid":"1726508880084.MXcdEb","vid":"z8RX4Dez2DdvMwIkaMwe","exp":1727167775921}; addshoppers.com=2%7C1%3A0%7C10%3A1726508880%7C15%3Aaddshoppers.com%7C44%3AMDhiMWQ4MmU4NmI4NDI2NWJhMzhjNzNmMWQxZTYyNGQ%3D%7C80e05a031f510e961d9c521fa68174f4ab6d12b458840624879e4522863c980e; experiment_=; dtSa=-; RT="z=1&dm=www.chewy.com&si=e2a4c6f1-b216-4769-9d7d-a662a70d12c5&ss=m17kh8k5&sl=0&tt=0&bcn=%2F%2F17de4c19.akstat.io%2F&ul=1n9f5&hd=1n9gk"; KP_UIDz-ssn=02o5NozCirX4xGymfsUE9NM1C7coaw4v3KODjryB4zAo06DRxuQn5FJp5hEhcJX0iE4ptAa9BIbbJ4HC66niN9bGWqGNhiingXYdl8R9U1Vr2LE1FRWNKUjFnLY5QDF2CGSJLc7NSODv2Trlq3Ne7rBVsAz9nUucKgy4fQIbTqlS8g1TDbiMeezDKPxqa9v9k79OAvONju49d; KP_UIDz=02o5NozCirX4xGymfsUE9NM1C7coaw4v3KODjryB4zAo06DRxuQn5FJp5hEhcJX0iE4ptAa9BIbbJ4HC66niN9bGWqGNhiingXYdl8R9U1Vr2LE1FRWNKUjFnLY5QDF2CGSJLc7NSODv2Trlq3Ne7rBVsAz9nUucKgy4fQIbTqlS8g1TDbiMeezDKPxqa9v9k79OAvONju49d; AKA_A2=A; ak_bmsc=68150CBC4BFB424A489C30BB4DC05062~000000000000000000000000000000~YAAQhqEkFxrW7OaRAQAA2B/hCBkBVF4PI4rKXxMnikpMBKaP4PKT2vRjU3G+yepdpvCdhWFiqj0KvnJNZmIwebk9CFJun1OmEFvLikIiQmJpilhgaCmxAGz+WZHiSLxc47Apce4cEC3yGvTwMMd9d8cMOTtNmHVptx3olTv36yVX68xv9QUh71WqQEQpIMpJggw5nfp5Cp3LOfRqkLGaSUyhIR4opTUus6FmJtqZ+RhRbW2sKH60I2bo5j38Q55r6pO8xbV8rXDVEtkkVXH9IuoOyBDqsyyiF/bVXEb15AXlvj4dR9oMVt5798XpEhLcXiX1bUYZzwkoWnH7Cwd1Not+LDwe7yyE8PrQAJzeam+PSZGtCh92ii4LEN/ExNA5N90nUqqZOVdUo9727DfpKoYwSXnLqVcPkgg4/Ffv9KdFpQ==; bm_sz=995DCC12F7C39FBC44327AE476578694~YAAQhqEkFxzW7OaRAQAA2B/hCBmRSZXoSnj5iFQG9iwX8feFeFP4X6uBHG6AVCquoiOJIeeRNU5vtoBcLcodg0aYzXj8+QOXuzKIQ93Gykr4XuwpzZmJW5mmZHOd0JptCpVgZ9eNxv+Nv/zMXYuHkn0bTt3GwJMjG2M6nBhwZeUHFhUlkEBq7mhuDZXQaFX8/X5UgJEFdhLZFsGQ225Vh8/bCR4sw4gmWmxW/gQZmQAh5+1QBsNTw1R3lRqlZiuCh+dSC1c9ncPa8quobBHW0bdTw3INmbvJWm2I7IY/ffptXSNWgZ+C6vYYQ1zlKCUZKpFHSwFY+GNCYuQwcmwxK8haWXRI+SIdIBykbT2qCnhm5O2tw0ycLXW+NMXH6Gj4qk/hOxH+pFxZaLRlUwSpypaAPSGJcmsJpAPeXEwXYOlQXTSl9k8=~3291449~4277553; chewy-insights=ts=https://www.chewy.com/; bm_sv=97CAB47FDBBA535CCD55900586049254~YAAQhqEkF0fW7OaRAQAA7yXhCBkO5vAJ24Yl3INzTKenOOrWIk84azw382Tjm/PSk3CzQhSDs5j8V1mtvdupOudH86uABHy8TfL0ksBRJvUIG/CoPKW3C6h83dH/SqQHFeALWs1kkiqrkMPyBkeHqEH1eRD3+MbDPGZilPHPACk6dnT1mk7yPjwRPPV+mbrkdRDQUBK9O/C5bpAahC+0d4BtaBBB1iipF0ePJRK2iGuBKL3KFfXD3wQxv3zzg98=~1; pageviewCount=7; pageviewCount30m=1; _ga_GM4GWYGVKP=GS1.1.1726725829.5.0.1726725829.60.0.0; dtPC=-68$525830039_613h-vFQJONTADGROLCJHORQTAKLMEASEMDFRE-0e0; _uetsid=c38d390074d111efab3fe3763a2d5640; _uetvid=c38d6f3074d111efaa4d197904445237; dtCookie=v_4_srv_3_sn_P0BCVKEJ8PU0IAQ36NHB98TJMEJCQNOV_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; _abck=D72CA898F39A1BD80917F567A9F1B7E1~-1~YAAQhqEkF/fW7OaRAQAAREjhCAxqYsyZ1dtkmchCZCSyfZoThnk3A+0icIBlzWTUiMBq/u8yIWCShFaCmZFDJ32tiqPBFX05R6mPuvhT+f3gGBaxe6vVzWSaoNZdW1V4iX05QpJsnD5V7JpcEe4ONkh/t1DtcAgWl22FncHQoqRYMrtY67mNKhvBFALvyQD1gwF+tDUZY6xx9ohxwCVE2aFYVEdtOu9nlbJZnnQv9yJZa5pStDrEK0arLsNlcoh5mj8Eaa+ocD4qIRShY85ySMWo74X6OHhZPdIBfCQ5pbxF+XN66sHVzIcYRUmJ52dR4bEzjuIAsaCsprXltbwRnPUX/Pv0a5eMHofr/0Pxki5XfZuY4L7+cNO3klmycVykBELCC7hJTettO3fsBt0Y7aZtT2998HV2d2TNGfqFZbu+P9MnnO5+0GMqgKQvfoz4XQC9KV5EJo/ajEGrCrooOVkZDGuV5s9GHjFSYMDi1yPGTs7cT0qHy2fzX9c4E2Lib/kztxvelaca16WT65lar6sA2/k=~-1~-1~-1; akavpau_defaultvp=1726726135~id=06549e5fb4e3690ca181c23d842a4258; akaalb_chewy_ALB=1726726435~op=chewy_com_ALB:www-chewy-use1|prd_kasada:prd-kasada-haproxy-use1|~rv=51~m=www-chewy-use1:0|prd-kasada-haproxy-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=4235d1d85f7e239b9bcb58bb7d5dcde3; rxvt=1726727636023|1726725830049; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+19+2024+08%3A03%3A56+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; _clck=7tp568%7C2%7Cfpb%7C0%7C1720; _clsk=197b6l1%7C1726725837835%7C1%7C0%7Cs.clarity.ms%2Fcollect',
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
    
    
