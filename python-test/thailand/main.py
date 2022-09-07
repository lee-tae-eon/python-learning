from time import sleep
from bs4 import BeautifulSoup as bs
import  requests


# ! hs code :  "01 ~ 97"
# ! 두번째 박스  "-" 로 indent 구분할 수 있음
# ! HS CODE가 없는 품명도 반영되어야함

# ! HS 0101.21.00의 최종 관세율을 확인하려면 첫번째 빨간 박스인 HS CODE를 클릭하거나,
# ! 아니면 우측의 드롭다운을 선택하여 ALL로 선택하여 검색버튼을 누르면 다음 페이지와 같이 화면이 나옴
# options = Options()
# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

# options.add_argument('user-agent=' + user_agent)
# options.add_argument('headless')
# options.add_argument('--blink-settings=imagesEnabled=false')

# driver = webdriver.Chrome(options=options)



search_list = []

for i in range(97):
  current_code = f"0{i + 1}" if i + 1 < 10  else str(i + 1)
  search_list.append(current_code)


def get_page():
  base_url = "http://itd.customs.go.th/igtf/viewerImportTariff.do"
  for code in search_list:
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
        t_desc = code.select("td:nth-last-child(2)")
        e_desc = code.select("td:last-child")
        # t_desc = code.find("td:nth-child(1)").string if code.find("td:nth-child(1)") != None else " "
        # e_desc = code.find("td:nth-child(2)").string if code.find("td:nth-child(2)") != None else " "
        print(hs_code, t_desc, e_desc)
        # print(hs_code ,t_desc, e_desc)
        print("///\n///")



get_page()













