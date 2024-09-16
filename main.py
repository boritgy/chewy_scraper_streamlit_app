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
    'dtSa': '-',
    'chewy-insights': 'ts=https://www.chewy.com/',
    'AKA_A2': 'A',
    'bm_sz': '9715736B1A2B8A631429F5C04AE80999~YAAQFARTaF+VGPSRAQAA95t0+RnpGqakJWPPBJpygE52GmHWvf5FJbT2ZIy4Cz1tRde8+MSGJIXgrXstAwNldc9pMYcY8FWWfR3rPU0lc8XB4fqogPCE+3iHsX8g4v1n9e184/T1ZzrW2iLnrH1oEuJ+udyx6K8rnPY/u/hleMACueKO1AChH5WaHG5coaJyFajyC8P1OBv+FiueZ/N8klp6qGkGS68yOqUskCxYOZDrPX3GJG2OT9D8wdI8TFd64XQBuTkC78JUvdzdm35LMHdtjDiZBTlwC4hk9U6+atfokcDc/vFns9Cd8r1rAH7yTwD13P/RTCuBQbMT6Pk5V15zJYeqNoOaWgk0KrRW/Nrr6GITv5EvgcYMIwbNkw6CMavoBmCIRhUyhnaB4wpFtxS1agT3Ds0Rhha6ivfBljYU+uYh0pkS~3290425~4342851',
    'bm_sv': '01149FB6ECEFC147174C40D88A15FFFF~YAAQBwRTaO8nvfORAQAAnKJ0+Rk38BItp0u6HGLrqFbhM01eQv80GylgetyYqqq6xGTW5W8rqJxvsjywcayHcgEcyzgNtjStmbEHdKjshcQLIVRGKFZIuH/AL6wGLUb9vTVl7IU5Mp3bZJJU3ND874WUjg97Zw19G4sKyytJw+ZddvVRX7GMa68xqUwiXXjd1ks4fqp7MvMMz1lpFqYbq6DptRnqy6RpNaIZLRZXXq8IiN3iuzoa+lVqwXFsxRU=~1',
    'plpids': '5dxy:5dxz|3pnx:3pny|3pis:6i47|3poi:3pok|3po1:3po2|3psy:6wfh|3zb7:3zb9|ja8u:ja9a|3pnz:3po0|3pou:3pov|i986:i98u|5dxu:5dxv|3pof:3poh|kkfy:ko9q|5dxw:6xa5|3pjx:3pjy|3pl3:3pl5|63tn:fj72|ja7y:ja8e|3zb4:3zb6|ja9q:jaae|3q33:3q35|3pq0:3pq1|dr3q:lzpi|3pol:3pon|3yp2:3yp3|8j05:nr3y|5dxs:5dxt|3py7:6xbk|3pyy:jv3y|6sic:6sid|3y1l:3y1n|3pkx:3pkz|3pt2:6wfk|3ppw:3ppx|3poc:3pod',
    'ak_bmsc': '7B72E342A59466D9665806269CD17A8D~000000000000000000000000000000~YAAQBwRTaAEovfORAQAAeqh0+RmD+Mw5ZrK96Rqjj0QSTAylhCA2NFZtyX2LY2amT7e8Ka5ZwtcOvUY2ixLeti36c8iouoqJkum8IwcjvwuIVp6+nWWnlsujjWn9ZUpzpf4TVtqm/mT+vzLSSmcIeBR+3Cu8B2g1P9e/rk+NbS516N0mmBX99+1I+oZPjNJo1xkSUMBapmnZrEvnqtdcX8H87PU1QlOPZiGCn3xgfDL0vXTjvkUJzXq+b961c33dwW6T8Tryj4XKpCxwuf3R6wVLL2GmTUzHe9wTAheCaFA6pcYTLycOcPM3ya9Pyrc4toWmUjzowrZs5QXbNR/EHtzyPC8EFAkFRIkbPwclFrbYv6n31kvs0SWqpoIZnQwtiSObv5KSsJI5sb27YDplXK7EnhcrhHOsQHw1JJ9Am9xCQIeSEVH4jSyHZWP7a+iwxektItlg6UxwU5qf8AcUWiAyWL1EOIEo4Hr0M6yOtXzs',
    'pageviewCount': '90',
    '_ga_GM4GWYGVKP': 'GS1.1.1726467058.16.0.1726467058.60.0.0',
    '_uetsid': '9e4ceb80710d11ef96a5e78feb9245ee',
    '_uetvid': '9e4d37e0710d11efae7c991463647fcd',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Sep+16+2024+08%3A10%3A59+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    '_clck': '1vwylvv%7C2%7Cfp8%7C0%7C1716',
    'pageviewCount30m': '1',
    '_clsk': 'b3ffhy%7C1726467059814%7C1%7C0%7Cw.clarity.ms%2Fcollect',
    'dtCookie': 'v_4_srv_10_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    'rxvt': '1726468860503|1726467058654',
    'dtPC': '10$267058648_629h-vVDGOPSWHMQCFCJMDMBUUBPDQBPHERIHG-0e0',
    'KP_UIDz-ssn': '0bFDOSJ7bt7glp2jQIraDXyhYFR7EuNJYo4eJ9pqTTnX9edyM3bkSD3O0Onmq3YXBEc9BTnKFiDJaZBnofIPnPUr5tRMqO5fo7SIROiO67sHg4bt5rF4i1sg72bKANiE1e71bwZfEqMw8AVidZNps5MpyLUmVZseNSuXWNMjBtP',
    'KP_UIDz': '0bFDOSJ7bt7glp2jQIraDXyhYFR7EuNJYo4eJ9pqTTnX9edyM3bkSD3O0Onmq3YXBEc9BTnKFiDJaZBnofIPnPUr5tRMqO5fo7SIROiO67sHg4bt5rF4i1sg72bKANiE1e71bwZfEqMw8AVidZNps5MpyLUmVZseNSuXWNMjBtP',
    'akavpau_defaultvp': '1726467367~id=a04cad6b5b3cf75723dea7a2fb4f325c',
    '_abck': '5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaM8ovfORAQAA6sx0+Qwyu0/agKGvA5Ncd9b5FINOCRKA3E3TV+paBaoJMTEoeOLLs4CmYL84e5scL8vO+pAltC4DFqqjOJG7V+nffJYdUDmmTuIytA3HWEzt0FuaTLDUYpNWRz+gXsk5AU1ZHWk6KJeHV6oLLHIzvAE4qdEgr7TNflTkeB30Y9v0skozKnOaKFDqiRBqaicqPysTaHPFU57P63YBv7J5xlQHkCaI5fnislrGong7UPuOH6liUlQVeHtL9u3VRePLZlS7cPlupkQACmzoecl8Opy5JTPrEw+RptwHFf1zzcnk1pcG4MJEco7sopVV3lqlq188xXs3dgutYXKNyOiU3olaXyKm3ep2GXAfWTBK+t3L3gs7tlVLRJf9IhjOvaJovL5sRsxHYowh+76u05/X8GoP7wn6FhnRGRVAkhfzFxVhCwDNT6XiM4eyB6MOiMr/uQB+auL3Si6dqX+ukgZa2u/UniQx8WWbsWRNtLe9ji8/~0~-1~-1',
    'akaalb_chewy_ALB': '1726467667~op=prd_chewy_lando:www-prd-lando-use2|chewy_com_ALB:www-chewy-use1|prd_kasada_plp:prd-kasada-plp-use2|~rv=59~m=www-prd-lando-use2:0|www-chewy-use1:0|prd-kasada-plp-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=6b5eb54aaf3fa0a1ee8b4f375a8f7978',
    'RT': '"z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m14lwn6b&sl=1&tt=5ki&rl=1&ld=5kl&ul=e8n"',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    # 'cookie': 'ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; device-id=e75aec2b-9f6a-45bd-8585-325684e1ccae; experiment_=; pid=zAdfeO0gQteR3EwdvManIw; rxVisitor=172614886550717S0UUK9BMOTP7EGAPL4A5G9REERETCE; abTestingAnonymousPID=zAdfeO0gQteR3EwdvManIw; _gcl_au=1.1.1261460882.1726148875; _ga=GA1.1.1996544349.1726148875; _mibhv=anon-1726148876453-4913162035_6593; _fbp=fb.1.1726148877979.83309416726697474; _tt_enable_cookie=1; _ttp=qRgXiEjWS4DFlo_-NnL2tBZn4cQ; addshoppers.com=2%7C1%3A0%7C10%3A1726148801%7C15%3Aaddshoppers.com%7C44%3AOWU2YTY0NjhmYjQ4NGFlZGE0ZmMxZmNiZjgzMjhiN2I%3D%7C0590968691d8fb528fbbb09d12aa8c13d660abfa8cbb39463eb00328f6712991; _iidt=BonYizeKv/gjvDwQzJQo9W/tZLy5bBPdswJpAyXAQoBf04FrgFFjFb4JvtlSFVGG38fkH+3XesfsXGDGE7DRGSh6YQFevJXL0gI8KDM=; fpPostInitStatus=SuccessfulResponse; _vid_t=32Wrtu0MjaVThYGsNZU3AmadDFyTkWynThKdZAQb2bLJhVL/fXhUg3HWFXifDTQYXOAE5+oTNf1tRwJ4xjL9f9Ra2JshGnxw63YExVE=; fppro_id={"rid":"1726148801954.6LwjS4","vid":"QY9VQsvezRldiCIrr5FY","exp":1726753680213}; _RCRTX03=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _RCRTX03-samesite=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _ga_18116CKN3R=GS1.1.1726153332.1.1.1726157023.0.0.0; sid=8f545594-8556-4c17-b1c6-c828b261e93b; x-feature-preview=false; ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; dtSa=-; chewy-insights=ts=https://www.chewy.com/; AKA_A2=A; bm_sz=9715736B1A2B8A631429F5C04AE80999~YAAQFARTaF+VGPSRAQAA95t0+RnpGqakJWPPBJpygE52GmHWvf5FJbT2ZIy4Cz1tRde8+MSGJIXgrXstAwNldc9pMYcY8FWWfR3rPU0lc8XB4fqogPCE+3iHsX8g4v1n9e184/T1ZzrW2iLnrH1oEuJ+udyx6K8rnPY/u/hleMACueKO1AChH5WaHG5coaJyFajyC8P1OBv+FiueZ/N8klp6qGkGS68yOqUskCxYOZDrPX3GJG2OT9D8wdI8TFd64XQBuTkC78JUvdzdm35LMHdtjDiZBTlwC4hk9U6+atfokcDc/vFns9Cd8r1rAH7yTwD13P/RTCuBQbMT6Pk5V15zJYeqNoOaWgk0KrRW/Nrr6GITv5EvgcYMIwbNkw6CMavoBmCIRhUyhnaB4wpFtxS1agT3Ds0Rhha6ivfBljYU+uYh0pkS~3290425~4342851; bm_sv=01149FB6ECEFC147174C40D88A15FFFF~YAAQBwRTaO8nvfORAQAAnKJ0+Rk38BItp0u6HGLrqFbhM01eQv80GylgetyYqqq6xGTW5W8rqJxvsjywcayHcgEcyzgNtjStmbEHdKjshcQLIVRGKFZIuH/AL6wGLUb9vTVl7IU5Mp3bZJJU3ND874WUjg97Zw19G4sKyytJw+ZddvVRX7GMa68xqUwiXXjd1ks4fqp7MvMMz1lpFqYbq6DptRnqy6RpNaIZLRZXXq8IiN3iuzoa+lVqwXFsxRU=~1; plpids=5dxy:5dxz|3pnx:3pny|3pis:6i47|3poi:3pok|3po1:3po2|3psy:6wfh|3zb7:3zb9|ja8u:ja9a|3pnz:3po0|3pou:3pov|i986:i98u|5dxu:5dxv|3pof:3poh|kkfy:ko9q|5dxw:6xa5|3pjx:3pjy|3pl3:3pl5|63tn:fj72|ja7y:ja8e|3zb4:3zb6|ja9q:jaae|3q33:3q35|3pq0:3pq1|dr3q:lzpi|3pol:3pon|3yp2:3yp3|8j05:nr3y|5dxs:5dxt|3py7:6xbk|3pyy:jv3y|6sic:6sid|3y1l:3y1n|3pkx:3pkz|3pt2:6wfk|3ppw:3ppx|3poc:3pod; ak_bmsc=7B72E342A59466D9665806269CD17A8D~000000000000000000000000000000~YAAQBwRTaAEovfORAQAAeqh0+RmD+Mw5ZrK96Rqjj0QSTAylhCA2NFZtyX2LY2amT7e8Ka5ZwtcOvUY2ixLeti36c8iouoqJkum8IwcjvwuIVp6+nWWnlsujjWn9ZUpzpf4TVtqm/mT+vzLSSmcIeBR+3Cu8B2g1P9e/rk+NbS516N0mmBX99+1I+oZPjNJo1xkSUMBapmnZrEvnqtdcX8H87PU1QlOPZiGCn3xgfDL0vXTjvkUJzXq+b961c33dwW6T8Tryj4XKpCxwuf3R6wVLL2GmTUzHe9wTAheCaFA6pcYTLycOcPM3ya9Pyrc4toWmUjzowrZs5QXbNR/EHtzyPC8EFAkFRIkbPwclFrbYv6n31kvs0SWqpoIZnQwtiSObv5KSsJI5sb27YDplXK7EnhcrhHOsQHw1JJ9Am9xCQIeSEVH4jSyHZWP7a+iwxektItlg6UxwU5qf8AcUWiAyWL1EOIEo4Hr0M6yOtXzs; pageviewCount=90; _ga_GM4GWYGVKP=GS1.1.1726467058.16.0.1726467058.60.0.0; _uetsid=9e4ceb80710d11ef96a5e78feb9245ee; _uetvid=9e4d37e0710d11efae7c991463647fcd; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+16+2024+08%3A10%3A59+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; _clck=1vwylvv%7C2%7Cfp8%7C0%7C1716; pageviewCount30m=1; _clsk=b3ffhy%7C1726467059814%7C1%7C0%7Cw.clarity.ms%2Fcollect; dtCookie=v_4_srv_10_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; rxvt=1726468860503|1726467058654; dtPC=10$267058648_629h-vVDGOPSWHMQCFCJMDMBUUBPDQBPHERIHG-0e0; KP_UIDz-ssn=0bFDOSJ7bt7glp2jQIraDXyhYFR7EuNJYo4eJ9pqTTnX9edyM3bkSD3O0Onmq3YXBEc9BTnKFiDJaZBnofIPnPUr5tRMqO5fo7SIROiO67sHg4bt5rF4i1sg72bKANiE1e71bwZfEqMw8AVidZNps5MpyLUmVZseNSuXWNMjBtP; KP_UIDz=0bFDOSJ7bt7glp2jQIraDXyhYFR7EuNJYo4eJ9pqTTnX9edyM3bkSD3O0Onmq3YXBEc9BTnKFiDJaZBnofIPnPUr5tRMqO5fo7SIROiO67sHg4bt5rF4i1sg72bKANiE1e71bwZfEqMw8AVidZNps5MpyLUmVZseNSuXWNMjBtP; akavpau_defaultvp=1726467367~id=a04cad6b5b3cf75723dea7a2fb4f325c; _abck=5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaM8ovfORAQAA6sx0+Qwyu0/agKGvA5Ncd9b5FINOCRKA3E3TV+paBaoJMTEoeOLLs4CmYL84e5scL8vO+pAltC4DFqqjOJG7V+nffJYdUDmmTuIytA3HWEzt0FuaTLDUYpNWRz+gXsk5AU1ZHWk6KJeHV6oLLHIzvAE4qdEgr7TNflTkeB30Y9v0skozKnOaKFDqiRBqaicqPysTaHPFU57P63YBv7J5xlQHkCaI5fnislrGong7UPuOH6liUlQVeHtL9u3VRePLZlS7cPlupkQACmzoecl8Opy5JTPrEw+RptwHFf1zzcnk1pcG4MJEco7sopVV3lqlq188xXs3dgutYXKNyOiU3olaXyKm3ep2GXAfWTBK+t3L3gs7tlVLRJf9IhjOvaJovL5sRsxHYowh+76u05/X8GoP7wn6FhnRGRVAkhfzFxVhCwDNT6XiM4eyB6MOiMr/uQB+auL3Si6dqX+ukgZa2u/UniQx8WWbsWRNtLe9ji8/~0~-1~-1; akaalb_chewy_ALB=1726467667~op=prd_chewy_lando:www-prd-lando-use2|chewy_com_ALB:www-chewy-use1|prd_kasada_plp:prd-kasada-plp-use2|~rv=59~m=www-prd-lando-use2:0|www-chewy-use1:0|prd-kasada-plp-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=6b5eb54aaf3fa0a1ee8b4f375a8f7978; RT="z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m14lwn6b&sl=1&tt=5ki&rl=1&ld=5kl&ul=e8n"',
    'priority': 'u=0, i',
    'referer': 'https://www.chewy.com/deals/chewy-pharmacy-fall-sale-20-off-any-143446',
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
    
    
