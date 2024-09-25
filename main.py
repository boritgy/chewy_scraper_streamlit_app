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
    'fpPostInitStatus': 'SuccessfulResponse',
    '_RCRTX03': 'd3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8',
    '_RCRTX03-samesite': 'd3bb2b68711711efa8edbd5e4cdcbd3d155b8d8b36e64d6cb01100facca103a8',
    '_ga_18116CKN3R': 'GS1.1.1726153332.1.1.1726157023.0.0.0',
    'sid': '8f545594-8556-4c17-b1c6-c828b261e93b',
    'x-feature-preview': 'false',
    'ajs_anonymous_id': '47dd1547-3473-403a-9b46-f53f1e5c8516',
    'dtSa': '-',
    'chewy-insights': 'ts=https://www.chewy.com/',
    'AKA_A2': 'A',
    'bm_sz': 'BEBC26FAE5B1719E40ED1C5D1F17A612~YAAQFARTaPhmogGSAQAAKaB7KRkxi3AGKvYZtbKvHFLnZWclMqYv8+2buvO6KL+TwionnSusafSxqX2B7YJGwCFmwHGwU9kTk6zG/anIMa/5zZs+J2J7RrWahSp8lWG1Pqyr7LVW2ennNomRDHk1iqb3KW6XVhHIiSM7arpKJ0bP6uDp8JPxVrnMk99xBDk2ycono4wIjWKzcdh0opxhqByAm2Jk1czgbs2Wfc+myLXGc9KEc81p9A80ytVzReqAzJmI/P17IKUWGOCdr2iVXaUkOoLQDyrtl5RiVq+4ZY0K9anbPkaQpVEXsY9KK2ByRPjNxV1Q9oGPmQ3CPcu+hmBjTcIA8Erzyy+ojy2l9Rj4lEHQCAyYkAoDTekWQdCdPdosf4yWFPr0drtLg1Kg/+zUxMr0YOTJU21RtUCHksoH5AkSU7Y=~3618361~4535110',
    'bm_sv': '030F2BE4DAD76982E4025A943E7D107E~YAAQBwRTaNBhLSeSAQAAeqZ7KRnddYeixyV6GJzBgSnaxdCecmX9IaXgdXaPrfVC4V9cPEgscxLqtchhO9mfnyo6mXYndLFUFF0Bgg4mCtMxGINfxNtagoUWAN+bv55t0LkZYZS9zAkXjNlksMHqY/xQMTMxHHasAX0fwSLu8w9xc3s0nNntjOlaz8o3w/yM5WK0URVixHUCPncc8YQJgrKIOwgr58uzLwPRIelDk1fek+RUTP5CGO8/O5IDiOY=~1',
    'KP_UIDz-ssn': '0y18DpmKtm3eZ7I0Sb5kV7GAYvXxdKYJIxmiT1RyqLQF3Y4usjfpJdwp4205btSKweFqTEQK3bOLJ2r7rbQHmE7QOa2981go25pCjoDYHewDoi6zr7VnKm7xQdajpwqUJuUDc4o0QC2fhBBrTEPnVrnYPY4rDdDYKAXE2WZaTAzAkKhhDICHO9sOEgpVPTlOWRZgJ201EMV',
    'KP_UIDz': '0y18DpmKtm3eZ7I0Sb5kV7GAYvXxdKYJIxmiT1RyqLQF3Y4usjfpJdwp4205btSKweFqTEQK3bOLJ2r7rbQHmE7QOa2981go25pCjoDYHewDoi6zr7VnKm7xQdajpwqUJuUDc4o0QC2fhBBrTEPnVrnYPY4rDdDYKAXE2WZaTAzAkKhhDICHO9sOEgpVPTlOWRZgJ201EMV',
    'bm_mi': '554D2ECC5EC17FA0EF228C66BBD1DE69~YAAQBwRTaPBhLSeSAQAAjKx7KRkUkWq/zlcknX44+ifAgilUgvdrrxZY9ARlNQB1GhiZaKrc5Jy2Q8bkIq6U4M5anPswdm7XKqRMPRH0+tfbsG126WV/TObnneKRkAvfJ0dmlZ1FzlIUEQTgelw8Bk0WVHd+jXiI+1e+Cvi9zIoWvZG3euSBFyp4A5aKssUkFrrn0IhR2tU7aYHToBvSnT1H/JRgkA1X5CpJsJKK23rrkgRnXMuxnOPwsd6OcqOxK04uxujcC94RYG3gpBLM1pjegqs0h09rvq7Re1YqXsYjYm40GiQagIicV9f05QrTYXLyGq5zPG1rVqNmuDE=~1',
    'plpids': '3zb4:3zb6|6wr6:6wr9|i986:i98u|3zb7:3zb9|6sic:6sid|3peg:3peh|3pk9:3pkb|3plu:3plv|79xi:79xj|3pgh:3pgi|5622:5623|3pjs:3pjt|5rxg:5rxh|i97a:i97i|3zb1:3zb2|6wr4:6wr5|3pei:3pej|6sie:6sif|3pls:3plt|3pgj:3pgk|5624:5625|epji:epjq|3pkc:3pke|5rxi:5rxj|6sia:6sib|79xk:79xl|5o35:5o36|3pee:3pef|79xg:79xh|5rxe:5rxf|3pgf:3pgg|561v:561w|epjy:epk6|epke:epkm',
    'ak_bmsc': '95F88946E3C9D9E29925BD7B0AD67EA0~000000000000000000000000000000~YAAQBwRTaDdiLSeSAQAA9rZ7KRn5cHJz3cJyPuAdZ5jEVfq8aRS/UupgIioeeLPlDIpb1XPTW3HYr+LxQVFbj6pcx88Eg2yLO6S/IU8oTMkMfKDrw2Rt2+2MDc7XLf61OY8EfYp6a+615wj5lSZzev8xG2bsttWZTD5C3+PwGSXUDKn7Y3l10OS1I636ymV3mTGc317h0v1j83/Yf5fOLwlhc3ETvw84tSOcuoVaj4xDCHyi+o6HJrWcSBGHxhzIdYAcsjr7PyL8NIINZiV3n01sDmVTdDkKfyOI0AaJWubpL5PgaO0j4zdurFsYxYoc8DT+Erm2YQfnOf9NrZFUql5xJ3gSffRAEiWJcherZmr7JrDRty6zBgBerfVgOsfijCqI7xwBhUbAhWHvEcFbUSuQTmFkU06ei1JBY8tb5fQXBd4xyLAINPDH70b5PxUjUKePLKFL03IxKQtm0WklvsWMtX8W81ot3rsiI8+6f0urtjwI2UYu9YWOLOFFIljyU9EfKIJreceHG3FmwLn8/VyHtW0=',
    'pageviewCount': '132',
    'fpGetInitStatus': 'SuccessfulResponse',
    '_ga_GM4GWYGVKP': 'GS1.1.1727272827.22.0.1727272828.59.0.0',
    '_uetsid': '854b3ba07b4611efac2845b9a46d6e0f',
    '_uetvid': '9e4d37e0710d11efae7c991463647fcd',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Sep+25+2024+16%3A00%3A29+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false',
    '_clck': '1vwylvv%7C2%7Cfph%7C0%7C1716',
    'pageviewCount30m': '1',
    '_iidt': 'q47QUTvT7KthCaitnmdFdHjtWwwViBim6aeCmVp+GF5f07w6zCfMh5mhwgBzXJ1EY3FAHdTe9YZ0rfAbykv861nG8rvMlNK98WKQUQ4=',
    '_vid_t': 'ZrKomDr1hfVxVBy4eHfRtseQn2qOAQ16c+N9/BX3xpWo3eyVKGBMmwj/VUHoiVW/uOyJdeErxjm6mHOZFy7CEfCU061loPiyT0H2RNc=',
    'fppro_id': '{"rid":"1727272830324.dBPKL8","vid":"QY9VQsvezRldiCIrr5FY","exp":1727877629763}',
    'rxvt': '1727274630035|1727272828205',
    '_clsk': 'fcacdx%7C1727272830124%7C1%7C0%7Cb.clarity.ms%2Fcollect',
    'dtCookie': 'v_4_srv_1_sn_26PP1ALP0FTJ1SNVLMS0ULP5SPB1Q0HN_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0',
    'dtPC': '1$472828193_724h-vBFKDVWGHOPRQRPLICKCFDCKHTEWWQMJA-0e0',
    'akavpau_defaultvp': '1727273143~id=80e0f7d42d67aab0c8e02a6c1adbb842',
    'akaalb_chewy_ALB': '1727273443~op=chewy_com_ALB:www-chewy-use2|prd_chewy_plp:www-prd-plp-use1|kasada_prd:kasada-prd|prd_kasada_plp:prd-kasada-plp-use1|~rv=94~m=www-chewy-use2:0|www-prd-plp-use1:0|kasada-prd:0|prd-kasada-plp-use1:0|~os=43a06daff4514d805d02d3b6b5e79808~id=193cd7fd9ddea36b8a300b7c78121903',
    '_abck': '5B4A007F283448D453DAE9D2C5A3F834~-1~YAAQBwRTaK1jLSeSAQAA5/h7KQzHyegsHXjlQXkBLIJfXLW5Rw4SxoLH/6ypPtJEw9XdAFfCIYLh3KzANxk/C1ax6w7slNRf6RFquP3WnlkwcScqnA1CvBuv7SKlc+7ENbmX2DtaurCLdf1QBvUs/pOIgWeG3GjjbjAXBC9JX8xSTcFSHzVwF3C0LvxSD+0LVzTZCr8OOyEOBTRyDPUOEcrstemg/K4KRL7rXMsJ5ky21N7uZZ6rp9m1wpwOZfn51I/ln14O/1nntUrP+2UqMyQmFy8r/1GPXNq0HwOF8ykXKWg3NxGDUUdd8/zdfKzs1aiJ8Wv6eEHCDX2+lSl05UDtZ00gIGIQ5i46hZ8HiO2zIXRjrxaLchUK0052Ptc0qutpRw4WlO9P39+ll9NBxQV5+g9Or/2i0EK/MQFK24+WXp/IgYnpemOtnAAq52X7MWw6TxTj1bH0Ju9UPtOQpvSXkrpqk3k/xsZsUbp4czIOYZS9ZH0R0Oo2nQN1XnSwj+SPlzdFsTiFoho0MQU4mMd6qajyqz1EzQ==~-1~-1~-1',
    'RT': '"z=1&dm=www.chewy.com&si=5ee530c4-7d70-40e1-a656-075371217a17&ss=m1hxn2xk&sl=1&tt=628&rl=1&ld=62b&ul=gvo"',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'hu-HU,hu;q=0.9,el-GR;q=0.8,el;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    # 'cookie': 'device-id=501d37e6-79ae-465c-b0c7-9766d38d59dc; pid=4J3Di1eUQcuZ_RD4u85HmA; sid=1839bb0a-1971-4312-b667-0c883a662da3; x-feature-preview=false; abTestingAnonymousPID=K9AjefB4QVy6zeKGnFqADg; _gcl_au=1.1.1916444144.1726562974; _ga=GA1.1.39900230.1726562974; rxVisitor=172656297441797CIT7PKGJ3VDF1O2ETEFSK4KL1U1URM; _fbp=fb.1.1726562974779.68070706348477632; _mibhv=anon-1726562974923-2204694577_6593; fpGetInitStatus=SuccessfulResponse; _tt_enable_cookie=1; _ttp=dTv3piPSJT1P5m5IYcWHUhi4Juj; ajs_anonymous_id=0e516ba1-4662-4a70-8628-bff483311dd7; _iidt=fQzUHXU9waSIkMr7IF1KgUEA1CO1oXIzvULeQAC/qlMIjuKQHWLAiQZCvtdOxOPJcZXpVllCNaQUww==; fpPostInitStatus=SuccessfulResponse; _vid_t=9OV6ytAcv9CN98xyhDvS1JiyrpZSiKFuw3TJXf4hwjckXTiF3xH5k++LrY1fthCHq1sXLJXA+6gSHw==; fppro_id={"rid":"1726508880084.MXcdEb","vid":"z8RX4Dez2DdvMwIkaMwe","exp":1727167775921}; addshoppers.com=2%7C1%3A0%7C10%3A1726508880%7C15%3Aaddshoppers.com%7C44%3AMDhiMWQ4MmU4NmI4NDI2NWJhMzhjNzNmMWQxZTYyNGQ%3D%7C80e05a031f510e961d9c521fa68174f4ab6d12b458840624879e4522863c980e; experiment_=; dtSa=-; AKA_A2=A; bm_sz=292C776F226F427013AB614B59A376DE~YAAQilgWApKleQ+SAQAAkaz5IhnndkBFR5voCsXL9Z/S54/izVzCof28dRAQuCq0H25T4MGyltyv08sLpjjP1YiTSBKbnEGnrC3RdaRU8TdcwhcJeUqQYXFFhYNlZujENDf9NLU0mFVoD3GspJ2HGH3D7fPmendUqXCIsdmmKcA7ZOBYjRlWcGFRyOAPQhEk8CN+GaovsZd8Vm7Vjy7QY2zv/0CLagv5Dq+vEgUclfvvOxqE5a+aR4E4wBotnC+qQETyrroU/pCYMQEHw6zFuxSxIvdTpc9GQdJc/YyXsk5iYlq0z7OkOqaYBKoyre2xFoI4aUCges8IvBk/7cZ4j2NQ0wJn5h53BpTGG49hmBNwrNSm7FhoQKedWdn86yj+siz4OMSDz3K4e9Fl5Q==~3158585~3617092; chewy-insights=ts=https://www.chewy.com/; bm_sv=80CBE4EDDD86486A66C0B7C5921AAF03~YAAQhlgWAuoqTxCSAQAATrP5Ihm1T+yF+jWg4eJ++vj51htzGexvCsJv6b58zpswQzeLLE4G2KZ8WiO7ULHXML73WqOWYJS6eV+UUhlrDLdL/ua6jPN0qwcbrkjP1DrI1oNQ0hCyQy8Gn9H4xmyVEZvQArriT5AdyFtQn/hNEdZPE8xi/dNwmbC83rFO7M8jwLmjv3I/t1SpGkLn5VfPElU87q6rvapfyhpswvvNZ5AduDSHESvZEW4Ckyqxygo=~1; KP_UIDz-ssn=02TkNlsztTqo0BJsk7qMbp0L65OV6oEXbcunZYSENh0MyT3kwBxvX2Od7DE7Yb80t32PC849pxMsf0mXHXHZQfAZXwPCD6V06lCY4DRwuXgPoeIzQNDumZunigEJ0uhPAFEoa3UP9oZK5St0vYWyP9Pn9vDbKZTn4crvoUvpJM; KP_UIDz=02TkNlsztTqo0BJsk7qMbp0L65OV6oEXbcunZYSENh0MyT3kwBxvX2Od7DE7Yb80t32PC849pxMsf0mXHXHZQfAZXwPCD6V06lCY4DRwuXgPoeIzQNDumZunigEJ0uhPAFEoa3UP9oZK5St0vYWyP9Pn9vDbKZTn4crvoUvpJM; bm_mi=5512A9A714F8E381539336C590AEDF60~YAAQhlgWAvkqTxCSAQAAoLf5IhkjSc5Wt2TP7Hkw5eq14nl0p8zcJc0YUdRWBsvc84+J4ZsoogwGVOaR2UcqYQDzZa1W0hBkBPqrQ2xuMn7FWLG4tinhGzPkM33WXuwK/Dn0gYbdVlaxOuD8ZfZiqQgJsEmilXhRvmvxKP9djKnvrE0BxXfK/TEDDntOfu2b1csvQhh2ea00kOQeRa3Xa/kUTY8LUzYl92aPdMsWpFANtquqZXTTiKhU63+yeJ1vHdncH94P5GMPSzmvWhZrf49mPtQL2MJDPRPdwy/WPmK/wDYYl4efZJrGox7d~1; ak_bmsc=0C7085A3C9B039A2B4E7F5B3871DA7FD~000000000000000000000000000000~YAAQhlgWAk8rTxCSAQAASsT5IhnWoDAWiwQR92Ihye84G+3ruulVK/7rhmGa19hlYNiDg+vJI/zzM/ycHQm/mYiJDdTmUdRuFxq8/TdpQc+yBTWSdf1HbJ0OMLqw7Pu0mnuXk+tAjOoGCgqTW2aEIrjosF6tJFRszZFmed34UT/BoqA1waZ0WBygbQMitxBcWJghhvZy25GI4yL9zQqObfbwFWgEv989GgTPgX3u8INYlDHf2pVRnbosc3nd3FFg9Nmo2ND6JKic+fThIA5auMTN4V7rhglx0yOMwh/TrcqOvCC6F3Wee5WInsgPJfDOeLe6dsBUukyhr2sMDdID4oQWcubixQy5rjFrJJlW2oa5AsEQMog3vyJRS7vqztw+cDRoz84DENSelX4zJYJmIu3oXm4MfBRE8AN0UqK6k0ijU14YwULYR/F8V24rXqQkP1bkzWP1Uzgtxm5YBhywF+e4eMykaHN2neA=; pageviewCount=11; pageviewCount30m=1; _ga_GM4GWYGVKP=GS1.1.1727163653.7.0.1727163653.60.0.0; _uetsid=5459c0c07a4811ef83bb49f55d3395d6; _uetvid=c38d6f3074d111efaa4d197904445237; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+24+2024+09%3A40%3A54+GMT%2B0200+(k%C3%B6z%C3%A9p-eur%C3%B3pai+ny%C3%A1ri+id%C5%91)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=BG36%3A1%2CC0004%3A1%2CC0010%3A1%2CC0011%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false; dtCookie=v_4_srv_1_sn_P0BCVKEJ8PU0IAQ36NHB98TJMEJCQNOV_app-3A7077613abb396c51_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; _clck=7tp568%7C2%7Cfpg%7C0%7C1720; _clsk=fwnvkg%7C1727163655556%7C1%7C0%7Cr.clarity.ms%2Fcollect; dtPC=1$363654020_98h-vHFHRQPIKHARCOUGQRQVAPRIAMSVNMCHA-0e0; rxvt=1727165456177|1727163654026; _abck=D72CA898F39A1BD80917F567A9F1B7E1~-1~YAAQilgWAlmoeQ+SAQAA8O75IgzaFH5hbBP+ZfNV/uyW7uH9jzptYLBHMDC4fFdYBxc2B2iXTi0fvb6OhlbzuGl0gkFvYBpHhhOUeXMCbf1czlombIkNtx6puCHjZXa6kn0Z713A2Uk43m1LfS5mI59eayyCen928PRCbmcsWLLlnrcqB9xOldKsJ+WCeV2ZgDqUxMSplbLjdFi3xjmiUTdvTasYJ3hiDwMCsddS3Cd5rwEcN1qcIFuUBBoD5UNDWl+Ujz+cfycuJpVyPPxZJCLJoN8iBJTqSA7c/o1iC3Vs1p7FRwzL6V/BHkggJoSFJrYtIOr0H/CpPDfbl6+hqaAdepLxYGT86Txzor/DpLmQYIvWTt5sdB4vCnOor4bsH042hje4CYO9e27esPoPn1Lcn6YXDiV9ZMTf0IEXdUN0gV6xYVqkzSioFjniyT0C5cR760I6FhkUasAilgAOKorqJKv8Kz3OU80NEKvNek6FztQyb92mAb2IStMWdbsR/53Ej+OkdVekJk+zGTnvlzq8sY0=~0~-1~-1; akavpau_defaultvp=1727163958~id=7e64f25f8925481ce98e160aecd7c4be; akaalb_chewy_ALB=1727164258~op=prd_chewy_lando:www-prd-lando-use1|chewy_com_ALB:www-chewy-use1|kasada_prd:kasada-prd|prd_kasada:prd-kasada-haproxy-use2|~rv=55~m=www-prd-lando-use1:0|www-chewy-use1:0|kasada-prd:0|prd-kasada-haproxy-use2:0|~os=43a06daff4514d805d02d3b6b5e79808~id=ea1d443f605ba0a9a15e5901d6bad095; RT="z=1&dm=www.chewy.com&si=e2a4c6f1-b216-4769-9d7d-a662a70d12c5&ss=m1g4n0kz&sl=1&tt=488&rl=1&ld=48a&nu=4vgiys1n&cl=8if&ul=bvn"',
    'priority': 'u=0, i',
    'referer': 'https://www.chewy.com/',
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
    
    
