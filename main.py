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
    '_clck': '1vwylvv%7C2%7Cfp7%7C0%7C1716',
    'dtSa': '-',
    'pageviewCount': '83',
    '_uetsid': '9e4ceb80710d11ef96a5e78feb9245ee',
    '_uetvid': '9e4d37e0710d11efae7c991463647fcd',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Sep+15+2024+17%3A05%3A39+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    '_abck': '5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaK5Pq/ORAQAAvLdP9gwMAwhq/Gy9blzoz5f+FfKJDnpgw/t1nSHhcDhdbZ8+/4yGx5dU0S6Vb604UpFKAUvtHHJxmuh4PI+6+3986y8FH/jK4MHGsakZdHO3LLTQ2tgNJY7hj6TiKFnVejP18bkjkdELjctu+dEqa4tGdELnhmYjl9J++EIN+9mYpLd+U73qZE3keJPAm0tzeaKUWXWjyhx2uEM1PuAPXrLkQPhzYq+9+48s2Vow99NUe/D5uN3zaVDiSLjSIAK+hSXz32Pf8VjKGryc8XsTYVUgar+uDykQkre0l0L4KJEKyORSV0OHXq8g+HhDItTFyHCrVu3S6MV8XBI+eVV3KJ9SRkNtIdm+s+bZBcTLl7T9MQBxn9ZP5a0QQb5jIIxys7HoQIXUGwwUyhoXpTn1MRwWtnWhrR87awK0A0bW5QWEhDxh89kXiP6QRLIGEtHgeGiDZn9FIRipVPF6apgN33EgP0jts836uoxmnadtAUeRmA==~-1~-1~-1',
    'plpids': '6khx:6khy|6zu1:6xji|my2:86w8|66p4:3svq|67n4:3yx6|3wqk:3wql|3ahp:3ahq|w3p:2kwu|3f7u:3f7v|5o8e:5o8g|evqm:evqu|kgp2:kgpa|68t2:68t3|3ya5:86wu|izr2:izra|67n5:4xhm|15w5:15w6|fwmm:fwmu|m9b:26d5|2fj8:2fj9|2aba:5o84|evq6:evqe|69m4:8gwt|b9sm:4ups|2fup:86wb|mjcu:mjd2|67n6:4xhl|izq6:izqe|b71a:3wqm|76oi:76oj|2fjm:2fjn|j166:j1a6|3xff:3xfh|6ihs:6iht|bffq:2q25|2fux:86wj',
    'AKA_A2': 'A',
    'bm_sv': '99CFF84CD1F85F7D4BB8B164EFFAE56D~YAAQFARTaH5V7vORAQAAh6Vz9hk2Ya47eUXUq1QNiLiyQO/TslKe/z+xLC3URff0ThCFtOIs2q0GU8xck+DA0Kf/g6c/rbghmcieqi9ABvaIS8E/Cc6LpU4vgqFJgxvXUU3oKSOCkuXPr9ibqVnzDOeHb74FDWlfroRYozT59UISQOqDgcU1PCo5kDBWTispDEtHdxb2RRcMuPFSas1Nnq+2Ub+Mt62Sau1g6trXkzXQencW3WGQMmwJO63VeF4=~1',
    'bm_sz': '2F8AB98AD84C32E9AB8B769B7D8B3BEF~YAAQFARTaH9V7vORAQAAh6Vz9hmZ6egumEbZnSz0Xxv2zBdD+zMXIdq++xnIgk4Q/uuZAv4C8SM9ZeIMr4MX245TkDc9zP8AKqjkvjok5Cy8RNxNiZp5c9/ChLeqw6pedp7jvnCAIzwnVo4Td91zMSQceMzip3x4KtgdeDbqP+tgMqYxZ73m9Mq/jY7ANYozSU0cBfjf8dJxBTOJ3H+DYXCxCKzKZVq52yCLTcvPN+FAtTzmpV0QNG+BLlKbQGMjmaT5TpnI5BuvX1REmdfs+2+/iFa8DvkLLKTdLEJr/onRUUkmNV8y4dTDUXRtCz1Sl1N7thq0blW678DsDsq/cOYJapoKR4oL2bwZD7M1r90Cc0PnaWxqOS7DaKWCk4XOClfhjgnx/ooLeglS1BLdzzuR5/8H1PzAGQp543qLHw7nZ869M9nU5FHupatd6OOd0LeBUmwXXKuNGRKUchXL6JZkRykkrHqFYe8wzB6GBH5HR64x~3552052~3748918',
    'chewy-insights': 'ts=https://www.chewy.com/',
    '_clsk': '11a1jli%7C1726417722910%7C2%7C0%7Ce.clarity.ms%2Fcollect',
    'rxvt': '1726419521495|1726416336675',
    '_ga_GM4GWYGVKP': 'GS1.1.1726412737.12.1.1726417723.60.0.0',
    'dtCookie': 'v_4_srv_12_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    'bm_mi': '9C0F051EB9D5FD8C6374367750051056~YAAQBwRTaGKHrfORAQAAVOSD9hlI4SOHF9qCr4FJHKKk2NUcDixUVTcM6HLtnYhs1yr2oEGazUucMOyqFCyxEBvC6Wq/zNNS2jPw7ZOIJcuM2rfGFE1seKBIF1XAMlznb82bhnqZaNmUMx0H9dSavhlNlCwyCjfd5pN9qG5h03rArc8bjhR1ooxBArXLlGXL6PfzfEMzncD0A8lVceMde53HjoudxofdIjmpt2Me/qn/c03Bv5Kg/TJ4/g2yOZZN97FO21dCr9jurIbEDzTeD3ZyNQQ0Dcjt5xIa0khcts7PLpkCSHKiNXvv9boxrxeAiWJFw+YN5g==~1',
    'RT': '"z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m13eqhyd&sl=1&tt=g21&nu=3ys2flk8&cl=brk3m&ld=dsti6&ul=dstis&hd=dsuf7"',
    'dtPC': '12$194560385_692h-vJJGRPQTFFMFSLKHAURMBMSQMCJMKMTGK-0e0',
    'KP_UIDz-ssn': '0bVXVGCZ8y2P5zvVPgLnZmGRMBPWSPW76x3vfPpmBJPYcZN63rdp24xXuqFjN70nHUdCLwust44Ajywjw1bvlC5ozu1ZG78uyp6uNeogVeNTCli42FZc1lp9UuVFAwJjk1gQPmQ4Tv2nBQUToFOXIDU1kwkArsL0bOrsMIZp6UB',
    'KP_UIDz': '0bVXVGCZ8y2P5zvVPgLnZmGRMBPWSPW76x3vfPpmBJPYcZN63rdp24xXuqFjN70nHUdCLwust44Ajywjw1bvlC5ozu1ZG78uyp6uNeogVeNTCli42FZc1lp9UuVFAwJjk1gQPmQ4Tv2nBQUToFOXIDU1kwkArsL0bOrsMIZp6UB',
    'akavpau_defaultvp': '1726418026~id=ccba9eb2b032d8fc123d2edf0b6a5878',
    'akaalb_chewy_ALB': '1726418326~op=prd_kasada_plp:prd-kasada-plp-use2|chewy_com_ALB:www-chewy-use1|prd_chewy_plp:www-prd-plp-use1|~rv=92~m=prd-kasada-plp-use2:0|www-chewy-use1:0|www-prd-plp-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=2408473521a8a179ed9e170d3cc98dce',
    'ak_bmsc': '74C94BE5EBF12DB0CF9D64E15A8E1FAD~000000000000000000000000000000~YAAQBwRTaMSHrfORAQAAe+yD9hk8hRTmCi3UfekoMlimFyFv6bLIoY3c0pIzXvQbv1X3gBIdyXaYM8oq90zCg8IMjsII9hvu04/dnTTOEpdsoWp+XYgO3l2MFT2lmKDCFsAJj3sh38+YZ50ScR8WFyoNlDvTNMrEhQKNTmtiG8TxvunxhxiKu4GeZ/fE/Do0uDcBb+nxyF1LFpSSgBdnqpDHI15/kdNYaZrIHTqKIEfs1G8YMVNPihkVkuWvau5iWYxs46KJb/XvZH6bKBPHOFkNQ54nofzzF1BeIlEIqtNnmQHxYNEQbiD/SKRCc2lSk+SVJC7nxyzgUK6PI+5RX3rAfN1H3SQJkeV93cLeIHIyBQmGxoiDKGlYnKU/hWm+BIJZu0dHRtJEVboKczRAdha1WW5BFr2+pg0uPcsQ1OcWVySckFUb9aA5b364uiCi+elCwkUHyhHmViBJxShSGZwmnSVoeEzT4HvqOjtGhJv/va0/Sb+PoGW1eRaU0b6PPtPePg==',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    # 'cookie': 'ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; device-id=e75aec2b-9f6a-45bd-8585-325684e1ccae; experiment_=; pid=zAdfeO0gQteR3EwdvManIw; rxVisitor=172614886550717S0UUK9BMOTP7EGAPL4A5G9REERETCE; abTestingAnonymousPID=zAdfeO0gQteR3EwdvManIw; _gcl_au=1.1.1261460882.1726148875; _ga=GA1.1.1996544349.1726148875; _mibhv=anon-1726148876453-4913162035_6593; _fbp=fb.1.1726148877979.83309416726697474; _tt_enable_cookie=1; _ttp=qRgXiEjWS4DFlo_-NnL2tBZn4cQ; addshoppers.com=2%7C1%3A0%7C10%3A1726148801%7C15%3Aaddshoppers.com%7C44%3AOWU2YTY0NjhmYjQ4NGFlZGE0ZmMxZmNiZjgzMjhiN2I%3D%7C0590968691d8fb528fbbb09d12aa8c13d660abfa8cbb39463eb00328f6712991; _iidt=BonYizeKv/gjvDwQzJQo9W/tZLy5bBPdswJpAyXAQoBf04FrgFFjFb4JvtlSFVGG38fkH+3XesfsXGDGE7DRGSh6YQFevJXL0gI8KDM=; fpPostInitStatus=SuccessfulResponse; _vid_t=32Wrtu0MjaVThYGsNZU3AmadDFyTkWynThKdZAQb2bLJhVL/fXhUg3HWFXifDTQYXOAE5+oTNf1tRwJ4xjL9f9Ra2JshGnxw63YExVE=; fppro_id={"rid":"1726148801954.6LwjS4","vid":"QY9VQsvezRldiCIrr5FY","exp":1726753680213}; _RCRTX03=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _RCRTX03-samesite=d3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8; _ga_18116CKN3R=GS1.1.1726153332.1.1.1726157023.0.0.0; sid=8f545594-8556-4c17-b1c6-c828b261e93b; x-feature-preview=false; ajs_anonymous_id=47dd1547-3473-403a-9b46-f53f1e5c8516; _clck=1vwylvv%7C2%7Cfp7%7C0%7C1716; dtSa=-; pageviewCount=83; _uetsid=9e4ceb80710d11ef96a5e78feb9245ee; _uetvid=9e4d37e0710d11efae7c991463647fcd; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Sep+15+2024+17%3A05%3A39+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; _abck=5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaK5Pq/ORAQAAvLdP9gwMAwhq/Gy9blzoz5f+FfKJDnpgw/t1nSHhcDhdbZ8+/4yGx5dU0S6Vb604UpFKAUvtHHJxmuh4PI+6+3986y8FH/jK4MHGsakZdHO3LLTQ2tgNJY7hj6TiKFnVejP18bkjkdELjctu+dEqa4tGdELnhmYjl9J++EIN+9mYpLd+U73qZE3keJPAm0tzeaKUWXWjyhx2uEM1PuAPXrLkQPhzYq+9+48s2Vow99NUe/D5uN3zaVDiSLjSIAK+hSXz32Pf8VjKGryc8XsTYVUgar+uDykQkre0l0L4KJEKyORSV0OHXq8g+HhDItTFyHCrVu3S6MV8XBI+eVV3KJ9SRkNtIdm+s+bZBcTLl7T9MQBxn9ZP5a0QQb5jIIxys7HoQIXUGwwUyhoXpTn1MRwWtnWhrR87awK0A0bW5QWEhDxh89kXiP6QRLIGEtHgeGiDZn9FIRipVPF6apgN33EgP0jts836uoxmnadtAUeRmA==~-1~-1~-1; plpids=6khx:6khy|6zu1:6xji|my2:86w8|66p4:3svq|67n4:3yx6|3wqk:3wql|3ahp:3ahq|w3p:2kwu|3f7u:3f7v|5o8e:5o8g|evqm:evqu|kgp2:kgpa|68t2:68t3|3ya5:86wu|izr2:izra|67n5:4xhm|15w5:15w6|fwmm:fwmu|m9b:26d5|2fj8:2fj9|2aba:5o84|evq6:evqe|69m4:8gwt|b9sm:4ups|2fup:86wb|mjcu:mjd2|67n6:4xhl|izq6:izqe|b71a:3wqm|76oi:76oj|2fjm:2fjn|j166:j1a6|3xff:3xfh|6ihs:6iht|bffq:2q25|2fux:86wj; AKA_A2=A; bm_sv=99CFF84CD1F85F7D4BB8B164EFFAE56D~YAAQFARTaH5V7vORAQAAh6Vz9hk2Ya47eUXUq1QNiLiyQO/TslKe/z+xLC3URff0ThCFtOIs2q0GU8xck+DA0Kf/g6c/rbghmcieqi9ABvaIS8E/Cc6LpU4vgqFJgxvXUU3oKSOCkuXPr9ibqVnzDOeHb74FDWlfroRYozT59UISQOqDgcU1PCo5kDBWTispDEtHdxb2RRcMuPFSas1Nnq+2Ub+Mt62Sau1g6trXkzXQencW3WGQMmwJO63VeF4=~1; bm_sz=2F8AB98AD84C32E9AB8B769B7D8B3BEF~YAAQFARTaH9V7vORAQAAh6Vz9hmZ6egumEbZnSz0Xxv2zBdD+zMXIdq++xnIgk4Q/uuZAv4C8SM9ZeIMr4MX245TkDc9zP8AKqjkvjok5Cy8RNxNiZp5c9/ChLeqw6pedp7jvnCAIzwnVo4Td91zMSQceMzip3x4KtgdeDbqP+tgMqYxZ73m9Mq/jY7ANYozSU0cBfjf8dJxBTOJ3H+DYXCxCKzKZVq52yCLTcvPN+FAtTzmpV0QNG+BLlKbQGMjmaT5TpnI5BuvX1REmdfs+2+/iFa8DvkLLKTdLEJr/onRUUkmNV8y4dTDUXRtCz1Sl1N7thq0blW678DsDsq/cOYJapoKR4oL2bwZD7M1r90Cc0PnaWxqOS7DaKWCk4XOClfhjgnx/ooLeglS1BLdzzuR5/8H1PzAGQp543qLHw7nZ869M9nU5FHupatd6OOd0LeBUmwXXKuNGRKUchXL6JZkRykkrHqFYe8wzB6GBH5HR64x~3552052~3748918; chewy-insights=ts=https://www.chewy.com/; _clsk=11a1jli%7C1726417722910%7C2%7C0%7Ce.clarity.ms%2Fcollect; rxvt=1726419521495|1726416336675; _ga_GM4GWYGVKP=GS1.1.1726412737.12.1.1726417723.60.0.0; dtCookie=v_4_srv_12_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; bm_mi=9C0F051EB9D5FD8C6374367750051056~YAAQBwRTaGKHrfORAQAAVOSD9hlI4SOHF9qCr4FJHKKk2NUcDixUVTcM6HLtnYhs1yr2oEGazUucMOyqFCyxEBvC6Wq/zNNS2jPw7ZOIJcuM2rfGFE1seKBIF1XAMlznb82bhnqZaNmUMx0H9dSavhlNlCwyCjfd5pN9qG5h03rArc8bjhR1ooxBArXLlGXL6PfzfEMzncD0A8lVceMde53HjoudxofdIjmpt2Me/qn/c03Bv5Kg/TJ4/g2yOZZN97FO21dCr9jurIbEDzTeD3ZyNQQ0Dcjt5xIa0khcts7PLpkCSHKiNXvv9boxrxeAiWJFw+YN5g==~1; RT="z=1&dm=www.chewy.com&si=98b81efb-454e-424b-a1e9-2d9063314156&ss=m13eqhyd&sl=1&tt=g21&nu=3ys2flk8&cl=brk3m&ld=dsti6&ul=dstis&hd=dsuf7"; dtPC=12$194560385_692h-vJJGRPQTFFMFSLKHAURMBMSQMCJMKMTGK-0e0; KP_UIDz-ssn=0bVXVGCZ8y2P5zvVPgLnZmGRMBPWSPW76x3vfPpmBJPYcZN63rdp24xXuqFjN70nHUdCLwust44Ajywjw1bvlC5ozu1ZG78uyp6uNeogVeNTCli42FZc1lp9UuVFAwJjk1gQPmQ4Tv2nBQUToFOXIDU1kwkArsL0bOrsMIZp6UB; KP_UIDz=0bVXVGCZ8y2P5zvVPgLnZmGRMBPWSPW76x3vfPpmBJPYcZN63rdp24xXuqFjN70nHUdCLwust44Ajywjw1bvlC5ozu1ZG78uyp6uNeogVeNTCli42FZc1lp9UuVFAwJjk1gQPmQ4Tv2nBQUToFOXIDU1kwkArsL0bOrsMIZp6UB; akavpau_defaultvp=1726418026~id=ccba9eb2b032d8fc123d2edf0b6a5878; akaalb_chewy_ALB=1726418326~op=prd_kasada_plp:prd-kasada-plp-use2|chewy_com_ALB:www-chewy-use1|prd_chewy_plp:www-prd-plp-use1|~rv=92~m=prd-kasada-plp-use2:0|www-chewy-use1:0|www-prd-plp-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=2408473521a8a179ed9e170d3cc98dce; ak_bmsc=74C94BE5EBF12DB0CF9D64E15A8E1FAD~000000000000000000000000000000~YAAQBwRTaMSHrfORAQAAe+yD9hk8hRTmCi3UfekoMlimFyFv6bLIoY3c0pIzXvQbv1X3gBIdyXaYM8oq90zCg8IMjsII9hvu04/dnTTOEpdsoWp+XYgO3l2MFT2lmKDCFsAJj3sh38+YZ50ScR8WFyoNlDvTNMrEhQKNTmtiG8TxvunxhxiKu4GeZ/fE/Do0uDcBb+nxyF1LFpSSgBdnqpDHI15/kdNYaZrIHTqKIEfs1G8YMVNPihkVkuWvau5iWYxs46KJb/XvZH6bKBPHOFkNQ54nofzzF1BeIlEIqtNnmQHxYNEQbiD/SKRCc2lSk+SVJC7nxyzgUK6PI+5RX3rAfN1H3SQJkeV93cLeIHIyBQmGxoiDKGlYnKU/hWm+BIJZu0dHRtJEVboKczRAdha1WW5BFr2+pg0uPcsQ1OcWVySckFUb9aA5b364uiCi+elCwkUHyhHmViBJxShSGZwmnSVoeEzT4HvqOjtGhJv/va0/Sb+PoGW1eRaU0b6PPtPePg==',
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
    
    
