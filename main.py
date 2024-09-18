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
    'dtSa': '-',
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
    'RT': '"z=1&dm=www.chewy.com&si=e2a4c6f1-b216-4769-9d7d-a662a70d12c5&ss=m16n3yi8&sl=1&tt=3z3&rl=1&ld=3z4&ul=bck&hd=bff"',
    'experiment_': '',
    'KP_UIDz-ssn': '02ryFOXkpHBACSfLTb2eicT9GpiFm8eXU541ZbpDVi1UXv4Dt1WuivD7YZioPw50KWQ9KD5Zv8lm8eQ0Q41iJ0eDeN5gImIi7pOg0G5sRHGhA4ptOWszXEhn2wUFAP0h7UrcwV0mTB7dOHL2APwXbjkxqCo1imt3THFREr7Y2elUz1tT4845MAnaM2hula4Q1dF3cRNjwntPh',
    'KP_UIDz': '02ryFOXkpHBACSfLTb2eicT9GpiFm8eXU541ZbpDVi1UXv4Dt1WuivD7YZioPw50KWQ9KD5Zv8lm8eQ0Q41iJ0eDeN5gImIi7pOg0G5sRHGhA4ptOWszXEhn2wUFAP0h7UrcwV0mTB7dOHL2APwXbjkxqCo1imt3THFREr7Y2elUz1tT4845MAnaM2hula4Q1dF3cRNjwntPh',
    'AKA_A2': 'A',
    'ak_bmsc': '04D947401BC2588FDE0EAF3E0A6857E9~000000000000000000000000000000~YAAQilgWAs1QoOKRAQAAqcIaBBlvSlGWBy0rOH7XgUBB64DuoPxVydqyp73RRfipxE9tDQahUkfVRwE9dyvZYMuxFTf/rdmrZE+50X6QZuZn20Zn0jt6tcS+GgB3KTeGiu4G1E8+uVkQnfoicc9H5m1n84HEaR3OF2KEI7eYpT6zhCAbPyTrYw1pwqQ5j3DFnDogkMbpH1ec9cdGpjghCs9qttKJlYL8ZA6+nv1uBm4QVIUM1+aYy+0X/RAvWZ/6MLEH/qLfYObVvdApJo8LFbvjByMz/gu8+pCZvBgtIWWUkWPUm1yW23J57ndrin1yaoFJig1dJzB40V0SIPU6hvlmeIApgmGoKBeDRM06NmxQSG9/Kj4eEPeARmmT3akSqLQz/Xw9NPRo',
    'bm_sz': '8A27820CC3CE2D212B5C6ADADFA80D6F~YAAQilgWAs9QoOKRAQAAqcIaBBnfGHXhFA1iJ2zRaI9KqO0kR0HQhwjGZBT6ZpRR0On4Y86Rft39cRoCic4i22nXwmNMvZn0dp5b8MybXSaSPXV47Dy6DJwXnD48lcOhYru2SRJ9NA/IGRPZqn9/MiOM/fElOKcqH1ReMKxxHQdhzcrJ5Y2W+rautM/XT06RvamG/r2okScjB1a7+t90canQU24ee4J73BgUWpFJVZcRKYxvzbS5tSNoorumceHt7MUFU9B8h/NlDQiZhsDAg+V2ngOEOw1J9I3MghQMUGIgflzn+nZeLAwhGI76ywpopjerYYR5cxKv9eqtNk4QmEqpIfDArvWLIah8062SAEQc/epYJV8dhCcKFZI05K6Wy+XvBnBXPyOQg/h4Ew==~3618886~4470850',
    'chewy-insights': 'ts=https://www.chewy.com/',
    'bm_sv': 'F55694C4E8FA728355C856F5AA25FB09~YAAQhlgWAt4Obf2RAQAA4sgaBBmozr01gaHE+QgMj/IwECFB0OvxLKXWtdFqUqyBdQMCHRuhK4QxIEfaIS0H8WCEQQejp2tXXUe5zaimidt4vFfNczd2L9vKIRr2jHEJ299EETkCUQsdm5mswhwQ0qxRfqy+qke+RcZpXGuuPh9G5q2o9epn9SaCRnXgKOTZn30McyI7FrnHMdZcLpuvcxHYLvtTfDUuqtUWG2U2bM/POhXl4fNxPWa4EaFFeMI=~1',
    '_abck': 'D72CA898F39A1BD80917F567A9F1B7E1~-1~YAAQhlgWAvEObf2RAQAAeM4aBAxVLev2+rS4rnbMPD1hnV/60kINHYrsnE6edR+WcIckIZiMQ+hyJVFPlVMPqWYDTe7LG4edAAFteHlQrSgACFwsxM7umnLkdwUPm9RX1wpz8STtQu1u0dPTXElmnFgyUlwMcv4hGXUsIZhG8k1+/sRlJzkDaC9L0UOzaRc4iW67Cn6h2qYciLOfE8sI7EZjAuzHWJ4yLLjqRMmcv2BLGQN2RMksfOvkAr+9Fuq/wZI1dNli05qBaB4tRLhrUv0ll/vUdclz0sfEeaUNzHlOnZfCw5VsTwMk4cYzqopEPQjkvG5YZa65Pk/PIidld00tLgI4vj3VNdZ7nyWesXPdx0OmJcc6PgfQ7aw06uc0pxrxvZAY22Avumzpbra06qd86gfxhbMX++suqcgMmcV/GT1KMhiIIvNwzdFXBGHXDePRoWZPySjh0sMDhHsrrphsZpo+z1arTGEiziNlUwQeEaXoAhRBTVOg8xzqOGVlBhGDJuwRHkCvo5BOTgB1FiA/aSQ=~-1~-1~-1',
    'pageviewCount': '4',
    'pageviewCount30m': '1',
    '_uetsid': 'c38d390074d111efab3fe3763a2d5640',
    '_uetvid': 'c38d6f3074d111efaa4d197904445237',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Sep+18+2024+09%3A48%3A39+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    'dtCookie': 'v_4_srv_11_sn_P0BCVKEJ8PU0IAQ36NHB98TJMEJCQNOV_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    'rxvt': '1726647520947|1726645718958',
    'dtPC': '11$445718954_758h-vPWAHWWWHEWWHLDJROFORUWSPLGAALMUQ-0e0',
    '_clck': '7tp568%7C2%7Cfpa%7C0%7C1720',
    '_clsk': 'vekcug%7C1726645721446%7C1%7C0%7Cr.clarity.ms%2Fcollect',
    '_ga_GM4GWYGVKP': 'GS1.1.1726645719.3.0.1726645730.49.0.0',
    'akavpau_defaultvp': '1726646030~id=7a946bc02c82fd494c12eeae80766dc6',
    'akaalb_chewy_ALB': '1726646330~op=chewy_com_ALB:www-chewy-use2|prd_kasada:prd-kasada-haproxy-use1|~rv=16~m=www-chewy-use2:0|prd-kasada-haproxy-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=be31e0a6e3aa8f0882c6df9fe1e81363',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    # 'cookie': 'device-id=501d37e6-79ae-465c-b0c7-9766d38d59dc; pid=4J3Di1eUQcuZ_RD4u85HmA; sid=1839bb0a-1971-4312-b667-0c883a662da3; x-feature-preview=false; abTestingAnonymousPID=K9AjefB4QVy6zeKGnFqADg; _gcl_au=1.1.1916444144.1726562974; _ga=GA1.1.39900230.1726562974; rxVisitor=172656297441797CIT7PKGJ3VDF1O2ETEFSK4KL1U1URM; dtSa=-; _fbp=fb.1.1726562974779.68070706348477632; _mibhv=anon-1726562974923-2204694577_6593; fpGetInitStatus=SuccessfulResponse; _tt_enable_cookie=1; _ttp=dTv3piPSJT1P5m5IYcWHUhi4Juj; ajs_anonymous_id=0e516ba1-4662-4a70-8628-bff483311dd7; _iidt=fQzUHXU9waSIkMr7IF1KgUEA1CO1oXIzvULeQAC/qlMIjuKQHWLAiQZCvtdOxOPJcZXpVllCNaQUww==; fpPostInitStatus=SuccessfulResponse; _vid_t=9OV6ytAcv9CN98xyhDvS1JiyrpZSiKFuw3TJXf4hwjckXTiF3xH5k++LrY1fthCHq1sXLJXA+6gSHw==; fppro_id={"rid":"1726508880084.MXcdEb","vid":"z8RX4Dez2DdvMwIkaMwe","exp":1727167775921}; addshoppers.com=2%7C1%3A0%7C10%3A1726508880%7C15%3Aaddshoppers.com%7C44%3AMDhiMWQ4MmU4NmI4NDI2NWJhMzhjNzNmMWQxZTYyNGQ%3D%7C80e05a031f510e961d9c521fa68174f4ab6d12b458840624879e4522863c980e; RT="z=1&dm=www.chewy.com&si=e2a4c6f1-b216-4769-9d7d-a662a70d12c5&ss=m16n3yi8&sl=1&tt=3z3&rl=1&ld=3z4&ul=bck&hd=bff"; experiment_=; KP_UIDz-ssn=02ryFOXkpHBACSfLTb2eicT9GpiFm8eXU541ZbpDVi1UXv4Dt1WuivD7YZioPw50KWQ9KD5Zv8lm8eQ0Q41iJ0eDeN5gImIi7pOg0G5sRHGhA4ptOWszXEhn2wUFAP0h7UrcwV0mTB7dOHL2APwXbjkxqCo1imt3THFREr7Y2elUz1tT4845MAnaM2hula4Q1dF3cRNjwntPh; KP_UIDz=02ryFOXkpHBACSfLTb2eicT9GpiFm8eXU541ZbpDVi1UXv4Dt1WuivD7YZioPw50KWQ9KD5Zv8lm8eQ0Q41iJ0eDeN5gImIi7pOg0G5sRHGhA4ptOWszXEhn2wUFAP0h7UrcwV0mTB7dOHL2APwXbjkxqCo1imt3THFREr7Y2elUz1tT4845MAnaM2hula4Q1dF3cRNjwntPh; AKA_A2=A; ak_bmsc=04D947401BC2588FDE0EAF3E0A6857E9~000000000000000000000000000000~YAAQilgWAs1QoOKRAQAAqcIaBBlvSlGWBy0rOH7XgUBB64DuoPxVydqyp73RRfipxE9tDQahUkfVRwE9dyvZYMuxFTf/rdmrZE+50X6QZuZn20Zn0jt6tcS+GgB3KTeGiu4G1E8+uVkQnfoicc9H5m1n84HEaR3OF2KEI7eYpT6zhCAbPyTrYw1pwqQ5j3DFnDogkMbpH1ec9cdGpjghCs9qttKJlYL8ZA6+nv1uBm4QVIUM1+aYy+0X/RAvWZ/6MLEH/qLfYObVvdApJo8LFbvjByMz/gu8+pCZvBgtIWWUkWPUm1yW23J57ndrin1yaoFJig1dJzB40V0SIPU6hvlmeIApgmGoKBeDRM06NmxQSG9/Kj4eEPeARmmT3akSqLQz/Xw9NPRo; bm_sz=8A27820CC3CE2D212B5C6ADADFA80D6F~YAAQilgWAs9QoOKRAQAAqcIaBBnfGHXhFA1iJ2zRaI9KqO0kR0HQhwjGZBT6ZpRR0On4Y86Rft39cRoCic4i22nXwmNMvZn0dp5b8MybXSaSPXV47Dy6DJwXnD48lcOhYru2SRJ9NA/IGRPZqn9/MiOM/fElOKcqH1ReMKxxHQdhzcrJ5Y2W+rautM/XT06RvamG/r2okScjB1a7+t90canQU24ee4J73BgUWpFJVZcRKYxvzbS5tSNoorumceHt7MUFU9B8h/NlDQiZhsDAg+V2ngOEOw1J9I3MghQMUGIgflzn+nZeLAwhGI76ywpopjerYYR5cxKv9eqtNk4QmEqpIfDArvWLIah8062SAEQc/epYJV8dhCcKFZI05K6Wy+XvBnBXPyOQg/h4Ew==~3618886~4470850; chewy-insights=ts=https://www.chewy.com/; bm_sv=F55694C4E8FA728355C856F5AA25FB09~YAAQhlgWAt4Obf2RAQAA4sgaBBmozr01gaHE+QgMj/IwECFB0OvxLKXWtdFqUqyBdQMCHRuhK4QxIEfaIS0H8WCEQQejp2tXXUe5zaimidt4vFfNczd2L9vKIRr2jHEJ299EETkCUQsdm5mswhwQ0qxRfqy+qke+RcZpXGuuPh9G5q2o9epn9SaCRnXgKOTZn30McyI7FrnHMdZcLpuvcxHYLvtTfDUuqtUWG2U2bM/POhXl4fNxPWa4EaFFeMI=~1; _abck=D72CA898F39A1BD80917F567A9F1B7E1~-1~YAAQhlgWAvEObf2RAQAAeM4aBAxVLev2+rS4rnbMPD1hnV/60kINHYrsnE6edR+WcIckIZiMQ+hyJVFPlVMPqWYDTe7LG4edAAFteHlQrSgACFwsxM7umnLkdwUPm9RX1wpz8STtQu1u0dPTXElmnFgyUlwMcv4hGXUsIZhG8k1+/sRlJzkDaC9L0UOzaRc4iW67Cn6h2qYciLOfE8sI7EZjAuzHWJ4yLLjqRMmcv2BLGQN2RMksfOvkAr+9Fuq/wZI1dNli05qBaB4tRLhrUv0ll/vUdclz0sfEeaUNzHlOnZfCw5VsTwMk4cYzqopEPQjkvG5YZa65Pk/PIidld00tLgI4vj3VNdZ7nyWesXPdx0OmJcc6PgfQ7aw06uc0pxrxvZAY22Avumzpbra06qd86gfxhbMX++suqcgMmcV/GT1KMhiIIvNwzdFXBGHXDePRoWZPySjh0sMDhHsrrphsZpo+z1arTGEiziNlUwQeEaXoAhRBTVOg8xzqOGVlBhGDJuwRHkCvo5BOTgB1FiA/aSQ=~-1~-1~-1; pageviewCount=4; pageviewCount30m=1; _uetsid=c38d390074d111efab3fe3763a2d5640; _uetvid=c38d6f3074d111efaa4d197904445237; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Sep+18+2024+09%3A48%3A39+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; dtCookie=v_4_srv_11_sn_P0BCVKEJ8PU0IAQ36NHB98TJMEJCQNOV_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; rxvt=1726647520947|1726645718958; dtPC=11$445718954_758h-vPWAHWWWHEWWHLDJROFORUWSPLGAALMUQ-0e0; _clck=7tp568%7C2%7Cfpa%7C0%7C1720; _clsk=vekcug%7C1726645721446%7C1%7C0%7Cr.clarity.ms%2Fcollect; _ga_GM4GWYGVKP=GS1.1.1726645719.3.0.1726645730.49.0.0; akavpau_defaultvp=1726646030~id=7a946bc02c82fd494c12eeae80766dc6; akaalb_chewy_ALB=1726646330~op=chewy_com_ALB:www-chewy-use2|prd_kasada:prd-kasada-haproxy-use1|~rv=16~m=www-chewy-use2:0|prd-kasada-haproxy-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=be31e0a6e3aa8f0882c6df9fe1e81363',
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
    
    
