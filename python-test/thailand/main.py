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
    # ! tag없는 text추출
    # if main_table.previous_silbing ==
    list_custom_detail = []
    for index, table in enumerate(main_table, 0) :
      # ! tag가 없는 요소인 협정세율 네이밍 가져오기 br태그 기준
      _br = table.find_previous_sibling("br")
      # * 협정세율 네이밍
      rate_title = table.previous_sibling if _br == None else _br.next_sibling
      # * 혐정세율 duty rate
      inside_tbody = table.find_all("td")[0]
      start_date = table.select_one("td:nth-last-child(3)").get_text(strip=True)
      end_date = table.select_one("td:nth-last-child(2)").get_text(strip=True)
      print(rate_title.split(":", 1)[0],start_date, end_date)

      # if _br == None:
      #   rate_title =
      #
      #   print(inside_tbody)
      # else:
      #   rate_title =


      # if  _font == None:
      #   print(table.previous_sibling, "prev not font")
      # else:
      #   print(_font.previous_sibling)

    # _font_list = main_div.find_all("font", recursive=False)
    # text_list = []
    # for font in _font_list:
    #   imp_tariff_code = font.previous_sibling.strip().replace("\r", "").replace("\n","")
    #   text_list.append(imp_tariff_code)

    # print(text_list)


# ! ------------------------------------------------------------------------------

search_list = []

for i in range(97):
  current_code = f"0{i + 1}" if i + 1 < 10  else str(i + 1)
  search_list.append(current_code)


def get_hs_code():
  results = []

  # for code in search_list:
  #   params = {"lang": "t", "taffCode": f"{code}", "docBegnDate": "07/09/2565", "param": "search"}
  params = {"lang": "t", "taffCode": "01", "docBegnDate": "07/09/2565", "param": "search"}

  sleep(3)

  response = requests.post(base_url, params=params)

  if response.status_code != 200:
    print(f"status {response.status_code}")
  else:
    soup = bs(response.text, "html.parser")
    t_body = soup.find("tbody")

    tr_list = t_body.find_all("tr")

    for code in tr_list:

      hs_code = code.find("a").string if code.find("a") != None else " "

      if len(hs_code.replace(".","")) >= 8:
        get_final_hs_code_detil_english(hs_code.replace(".",""))

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













