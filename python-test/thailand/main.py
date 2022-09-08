from time import sleep
from bs4 import BeautifulSoup as bs
import  requests


# ! hs code :  "01 ~ 97"
# ! 두번째 박스  "-" 로 indent 구분할 수 있음
# ! HS CODE가 없는 품명도 반영되어야함

# ! HS 0101.21.00의 최종 관세율을 확인하려면 첫번째 빨간 박스인 HS CODE를 클릭하거나,
# ! 아니면 우측의 드롭다운을 선택하여 ALL로 선택하여 검색버튼을 누르면 다음 페이지와 같이 화면이 나옴

base_url= "http://itd.customs.go.th/igtf/viewerImportTariff.do"



def get_final_hs_code_detil_english(keyword):
  params ={
    "param": "display1",
    "lang": "e",
    "key2": f"{keyword}",
    "key": "z",
    "keyName": "All",
    "docBegnDate": "07/09/2022",
    "piveName": "z"
  }

  response = requests.post(base_url, params=params)
  if response.status_code != 200:
    print(f"status {response.status_code}")
  else:
    soup = bs(response.text, "html.parser")
    main_div = soup.find(id="divprint")
    main_table = main_div.find_all("div", class_="table-responsive")

    list_custom_detail = []
    for index, table in enumerate(main_table, 0) :
      # ! tag가 없는 요소인 협정세율 네이밍 가져오기 br태그 기준
      _br = table.find_previous_sibling("br")
      # * 협정세율 네이밍
      rate_title = table.previous_sibling if _br == None else _br.next_sibling

      _tbody = table.find("tbody")
      _tr_list = _tbody.find_all("tr", reculsive = False)

      for tr in _tr_list:
        _td_list = tr.find_all("td")

        hs_code = _td_list[1].string.strip()
        description = _td_list[2].string.strip()
        ad_valorem_rate = _td_list[3].select_one("font").get_text(strip=True) if len(_td_list)  == 8 else _td_list[3].text.strip()
        unit = _td_list[3].select_one("font").get_text(strip=True) if len(_td_list)  == 8 else _td_list[4].text.strip()
        baht = _td_list[3].select_one("font").get_text(strip=True) if len(_td_list)  == 8 else _td_list[5].text.strip()
        start_date = _td_list[-3].string.strip()
        end_date = _td_list[-2].string.strip()
        rate_dict = {
          "rate_title": rate_title.strip(),
          "hs_code" : hs_code,
          "description" : description,
          "ad_valorem_rate" : ad_valorem_rate,
          "unit" : unit,
          "baht" : baht,
          "start_date" : start_date,
          "end_date" : end_date,
        }
        list_custom_detail.append(rate_dict)
    return list_custom_detail





# ! ------------------------------------------------------------------------------

search_list = []

for i in range(97):
  current_code = f"0{i + 1}" if i + 1 < 10  else str(i + 1)
  search_list.append(current_code)


def get_hs_code():
  results = []

  # for code in search_list:
  #   params = {"lang": "t", "taffCode": f"{code}", "docBegnDate": "07/09/2565", "param": "search"}
  params = {"lang": "t", "taffCode": "02", "docBegnDate": "07/09/2565", "param": "search"}

  sleep(2)

  response = requests.post(base_url, params=params)

  if response.status_code != 200:
    print(f"status {response.status_code}")
  else:
    soup = bs(response.text, "html.parser")
    t_body = soup.find("tbody")

    tr_list = t_body.find_all("tr")

    for code in tr_list:
      sleep(1)
      hs_code = code.find("a").string if code.find("a") != None else " "

      if len(hs_code.replace(".","")) >= 8:
        custom_rate_dict = get_final_hs_code_detil_english(hs_code.replace(".",""))
        print(custom_rate_dict)
        if(hs_code == "0203.12.00"):
          print(custom_rate_dict)
      t_desc = code.select_one("td:nth-last-child(2)").get_text(strip=True).replace(",", " ")
      e_desc = code.select_one("td:last-child").get_text(strip=True).replace(",", " ")

      count = 0
      for word in t_desc:
          if word == '-':
              count = count + 1
          elif word != ' ':
              break
      indent = f'{count}'



      code_dict = {"hs_code": hs_code,"indent": indent, "origin": t_desc, "english": e_desc, "ceiling_rate": "",  "general_Rate": "", }
      results.append(code_dict)

    # file = open(f"thiland.csv", "w")

    # file.write("hscode, indent, origin, english\n")

    # for result in results:
    #   file.write(f"{result['hs_code']},{result['indent']},{result['origin']},{result['english']}\n")

    # file.close()


get_hs_code()













