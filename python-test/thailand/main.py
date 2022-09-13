from time import sleep
from bs4 import BeautifulSoup as bs
import  requests


# ! hs code :  "01 ~ 97"
# ! 두번째 박스  "-" 로 indent 구분할 수 있음
# ! HS CODE가 없는 품명도 반영되어야함

# ! HS 0101.21.00의 최종 관세율을 확인하려면 첫번째 빨간 박스인 HS CODE를 클릭하거나,
# ! 아니면 우측의 드롭다운을 선택하여 ALL로 선택하여 검색버튼을 누르면 다음 페이지와 같이 화면이 나옴

class HsCode:
  def __init__(self, hs_code,indent, origin, english ):
    self.hs_code = hs_code
    self.indent = indent
    self.origin = origin
    self.english = english

  def get_hscode(self):
    return {"hs_code": self.hs_code, "indent": self.indent, "origin": self.origin, "english": self.english}

base_url= "http://itd.customs.go.th/igtf/viewerImportTariff.do"




def get_final_hs_code_detil_english(keyword):

  exact_keyword = keyword.replace(".","")

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
  sleep(1.5)
  if response.status_code != 200:
    print(f"status {response.status_code}")
  else:
    soup = bs(response.text, "html.parser")
    main_div = soup.find(id="divprint")
    main_table_list = main_div.find_all("div", class_="table-responsive")


    new_hscode_list = []
    rate_dict_list = []

    for table in main_table_list :
      # ! tag가 없는 요소인 협정세율 네이밍 가져오기 br태그 기준
      _br = table.find_previous_sibling("br")
      # * 협정세율 네이밍
      rate_title = table.previous_sibling.replace("\r\n","") if _br == None else _br.next_sibling.replace("\r\n","")
      str_rate_title = rate_title.split(":")[0].strip() + ": " + rate_title.split(":")[1].strip()

      _tbody = table.find("tbody")
      _tr_list = _tbody.find_all("tr", reculsive = False)

      for tr in _tr_list:
        _td_list = tr.find_all("td")

        sub_heading = _td_list[1].string.strip()

        description = _td_list[2].string.strip()

        ad_valorem_rate = "Exempted" if len(_td_list)  == 8 else _td_list[3].text.strip().replace("\r\n","").replace("**","").strip()
        unit = "Exempted" if len(_td_list)  == 8 else _td_list[4].text.strip().replace("\r\n","").replace("**","")
        baht = "Exempted" if len(_td_list)  == 8 else _td_list[5].text.strip().replace("\r\n","").replace("**","")
        start_date = _td_list[-3].string.strip()
        end_date = _td_list[-2].string.strip()

        if f"{exact_keyword}00" != (sub_heading.replace(".", "") + "00" if len(sub_heading.replace(".", "")) == 8 else sub_heading.replace(".", "")) :

          exist_code_list = []
          for new_hscode_duple in new_hscode_list:
            exist_code_list.append(new_hscode_duple["hs_code"])

          if sub_heading in exist_code_list:
            for new_hscode_duple in new_hscode_list:
              if new_hscode_duple["hs_code"] == sub_heading:
                new_hscode_duple["custom_rate"].append({
                "rate_title": str_rate_title,
                "ad_valorem_rate" : ad_valorem_rate,
                "unit" : unit,
                "baht" : baht,
                "start_date" : start_date,
                "end_date" : end_date
                })
          else:
            new_hscode = {
                "hs_code": sub_heading,
                "description": description,
                "custom_rate": [
                  {
                    "rate_title": str_rate_title,
                    "ad_valorem_rate" : ad_valorem_rate,
                    "unit" : unit,
                    "baht" : baht,
                    "start_date" : start_date,
                    "end_date" : end_date
                    }
                ]
              }
            new_hscode_list.append(new_hscode)
        else:
          rate_dict = {
              "rate_title": str_rate_title,
              "sub_heading" : sub_heading,
              "description" : description,
              "ad_valorem_rate" : ad_valorem_rate,
              "unit" : unit,
              "baht" : baht,
              "start_date" : start_date,
              "end_date" : end_date,
            }

          rate_dict_list.append(rate_dict)



    return {"new_hscode_list":new_hscode_list, "rate_dict_list":rate_dict_list}





# ! ------------------------------------------------------------------------------

search_list = []

for i in range(97):
  current_code = f"0{i + 1}" if i + 1 < 10  else str(i + 1)
  search_list.append(current_code)


def get_hs_code():
  results = []

  # for code in search_list:
  #   params = {"lang": "t", "taffCode": f"{code}", "docBegnDate": "07/09/2565", "param": "search"}
  params = {"lang": "t", "taffCode": "0813", "docBegnDate": "07/09/2565", "param": "search"}


  response = requests.post(base_url, params=params)
  sleep(1.5)

  if response.status_code != 200:
    print(f"status {response.status_code}")
  else:
    soup = bs(response.text, "html.parser")
    t_body = soup.find("tbody")

    tr_list = t_body.find_all("tr")

    for code in tr_list:

      hs_code = code.find("a").string.strip() if code.find("a") != None else " "

      t_desc = code.select_one("td:nth-last-child(2)").get_text(strip=True).replace(",", " ")
      e_desc = code.select_one("td:last-child").get_text(strip=True).replace(",", " ")

      count = 0
      for word in t_desc:
          if word == '-':
              count = count + 1
          elif word != ' ':
              break
      indent = f'{count}'

      hs_code_dict = HsCode(hs_code, indent, t_desc, e_desc).get_hscode()

      results.append(hs_code_dict)

      if len(hs_code.replace(".","")) >= 8:
        custom_rate_dict = get_final_hs_code_detil_english(hs_code.replace(".",""))

        if len(custom_rate_dict["new_hscode_list"]) >= 1:
          for new_code in custom_rate_dict["new_hscode_list"]:
            new_code_dict = {"hs_code": new_code["hs_code"], "indent": indent, "origin": "", "english": new_code["description"], }
            results.append(new_code_dict)



  print(results)
  file = open(f"thiland.csv", "w")

  file.write("hscode, indent, origin, english\n")

  for result in results:
    file.write(f"{result['hs_code']},{result['indent']},{result['origin']},{result['english']}\n")

  file.close()


get_hs_code()


