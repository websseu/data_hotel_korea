from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import os, time, json, re

# ===== 공통 설정 =====
current_date = datetime.now().strftime("%Y-%m-%d")
base_folder = "CityTop10"
date_folder = os.path.join(base_folder, current_date)
os.makedirs(date_folder, exist_ok=True)

# ===== 주소 설정 =====
urls = {
    "발리": "https://www.agoda.com/ko-kr/city/bali-id.html",
    "반둥": "https://www.agoda.com/ko-kr/city/bandung-id.html",
    "방콕": "https://www.agoda.com/ko-kr/city/bangkok-th.html",
    "보라카이": "https://www.agoda.com/ko-kr/city/boracay-island-ph.html",
    "부산": "https://www.agoda.com/ko-kr/city/busan-kr.html",
    "세부": "https://www.agoda.com/ko-kr/city/cebu-ph.html",
    "치앙마이": "https://www.agoda.com/ko-kr/city/chiang-mai-th.html",
    "다낭": "https://www.agoda.com/ko-kr/city/da-nang-vn.html",
    "후쿠오카": "https://www.agoda.com/ko-kr/city/fukuoka-jp.html",
    "하노이": "https://www.agoda.com/ko-kr/city/hanoi-vn.html",
    "핫야이": "https://www.agoda.com/ko-kr/city/hat-yai-th.html",
    "호치민": "https://www.agoda.com/ko-kr/city/ho-chi-minh-city-vn.html",
    "호이안": "https://www.agoda.com/ko-kr/city/hoi-an-vn.html",
    "홍콩": "https://www.agoda.com/ko-kr/city/hong-kong-hk.html",
    "후아힌": "https://www.agoda.com/ko-kr/city/hua-hin-cha-am-th.html",
    "화롄/화연": "https://www.agoda.com/ko-kr/city/hualien-tw.html",
    "이포": "https://www.agoda.com/ko-kr/city/ipoh-my.html",
    "자카르타": "https://www.agoda.com/ko-kr/city/jakarta-id.html",
    "제주도": "https://www.agoda.com/ko-kr/city/jeju-island-kr.html",
    "조호바루": "https://www.agoda.com/ko-kr/city/johor-bahru-my.html",
    "가오슝": "https://www.agoda.com/ko-kr/city/kaohsiung-tw.html",
    "코타키나발루": "https://www.agoda.com/ko-kr/city/kota-kinabalu-my.html",
    "끄라비/크라비": "https://www.agoda.com/ko-kr/city/krabi-th.html",
    "쿠알라룸푸르": "https://www.agoda.com/ko-kr/city/kuala-lumpur-my.html",
    "쿠안탄": "https://www.agoda.com/ko-kr/city/kuantan-my.html",
    "교토": "https://www.agoda.com/ko-kr/city/kyoto-jp.html",
    "마카오": "https://www.agoda.com/ko-kr/city/macau-mo.html",
    "말라카": "https://www.agoda.com/ko-kr/city/malacca-my.html",
    "마닐라": "https://www.agoda.com/ko-kr/city/manila-ph.html",
    "나고야": "https://www.agoda.com/ko-kr/city/nagoya-jp.html",
    "나트랑/나짱": "https://www.agoda.com/ko-kr/city/nha-trang-vn.html",
    "오키나와": "https://www.agoda.com/ko-kr/city/okinawa-main-island-jp.html",
    "오사카": "https://www.agoda.com/ko-kr/city/osaka-jp.html",
    "파타야": "https://www.agoda.com/ko-kr/city/pattaya-th.html",
    "페낭": "https://www.agoda.com/ko-kr/city/penang-my.html",
    "푸켓": "https://www.agoda.com/ko-kr/city/phuket-th.html",
    "삿포로": "https://www.agoda.com/ko-kr/city/sapporo-jp.html",
    "서울": "https://www.agoda.com/ko-kr/city/seoul-kr.html",
    "상하이": "https://www.agoda.com/ko-kr/city/shanghai-cn.html",
    "싱가포르": "https://www.agoda.com/ko-kr/city/singapore-sg.html",
    "수라바야": "https://www.agoda.com/ko-kr/city/surabaya-id.html",
    "타이중": "https://www.agoda.com/ko-kr/city/taichung-tw.html",
    "타이난": "https://www.agoda.com/ko-kr/city/tainan-tw.html",
    "타이베이": "https://www.agoda.com/ko-kr/city/taipei-tw.html",
    "도쿄/동경": "https://www.agoda.com/ko-kr/city/tokyo-jp.html",
    "이란": "https://www.agoda.com/ko-kr/city/yilan-tw.html",
    "족자카르타/욕야카르타": "https://www.agoda.com/ko-kr/city/yogyakarta-id.html",
    "런던": "https://www.agoda.com/ko-kr/city/london-gb.html",
    "파리": "https://www.agoda.com/ko-kr/city/paris-fr.html"
}

# ===== 언어 설정 =====
def language(browser, wait):
    try:
        # 헤더 먼저 안전하게 클릭
        header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header")))
        ActionChains(browser).move_to_element_with_offset(header, 10, 10).click().perform()
        time.sleep(1)

        # 언어 버튼 클릭
        lang_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-element-name="language-container-selected-language"]'))
        )
        lang_button.click()
        time.sleep(0.5)

        # English 옵션 클릭
        english_option = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-element-name="language-popup-menu-item"][data-value="ko-kr"]'))
        )
        english_option.click()
        time.sleep(1)

        print("언어를 Korean로 변경 완료")

    except TimeoutException:
        print("언어 변경 실패: 요소를 찾지 못했습니다.")
    except Exception as e:
        print(f"어 변경 중 오류 발생: {e}")

# ===== 주소 키워드 추출 =====
def keyword(url: str) -> str:
    m = re.search(r"/city/([a-z\-]+)\.html", url)
    if not m:
        return "unknown"
    slug = m.group(1)          
    return slug.split("-")[0] 

# ===== 웹드라이버 설정 =====
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1440,2000") 
options.add_argument("--lang=ko-KR")
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2,
})
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
time.sleep(2)

# 모든 주소에 대해 순차적으로 작업
for city, url in urls.items():
    print(f'▶ {city} 접속: {url}')
    browser.get(url)

    # 언어 설정 실행
    language(browser, wait)

    # 호텔 카드 로드 대기
    try:
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".DatelessPropertyCard")
            )
        )
    except TimeoutException:
        print(f"{city} 페이지에서 호텔 카드를 찾지 못했습니다. 다음으로 넘어갑니다.")
        continue

    hotels_data = []

    # 호텔 카드 최대 10개 추출
    hotel_cards = browser.find_elements(By.CSS_SELECTOR, ".DatelessPropertyCard")[:10]

    for idx, hotel_card in enumerate(hotel_cards, start=1):
        try:
            # 호텔 이름
            store_name = hotel_card.find_element(By.CSS_SELECTOR, ".DatelessPropertyCard__ContentHeader").text.strip()

            # 후기 설명
            store_detail = hotel_card.find_element(By.CSS_SELECTOR, ".DatelessPropertyCard__ContentDetail").text.strip()
            store_detail = store_detail.replace('"', "")

            # 지역 추출
            store_area = hotel_card.find_element(By.CSS_SELECTOR, ".DatelessPropertyCard__ContentAreaCity").text.strip()

            additional = hotel_card.find_element(By.CSS_SELECTOR, ".DatelessPropertyCard__Additional")

            # 호텔 ID & URL
            hotel_id = hotel_card.get_attribute("data-hotel-id")
            hotel_url = hotel_card.get_attribute("data-element-url")
            if hotel_url and hotel_url.startswith("/"):
                hotel_url = "https://www.agoda.com" + hotel_url

            # 평점
            try:
                rating = additional.find_element(By.CSS_SELECTOR, "span").text.strip()
            except:
                rating = ""

            # 이용후기 건수
            try:
                reviews = ""
                for p in additional.find_elements(By.CSS_SELECTOR, "p"):
                    txt = p.text.strip()
                    if "이용후기" in txt or "reviews" in txt.lower():
                        reviews = txt
                        break
            except:
                reviews = ""

            # 가격
            try:
                price = ""
                price_block = additional.find_element(By.CSS_SELECTOR, ".DatelessPropertyCard__AdditionalPrice")
                divs = price_block.find_elements(By.CSS_SELECTOR, "div")
                for div in divs:
                    txt = div.text.strip()
                    # 숫자가 포함되어 있고, "박" 같은 단어가 없을 때만 가격으로 인식
                    if re.search(r"\d", txt) and "박" not in txt:
                        # 정규식으로 숫자만 추출
                        numbers = re.findall(r"\d+", txt)
                        if numbers:
                            price = "".join(numbers)  # "95112" 같은 순수 숫자
                        break
            except:
                price = ""

            # 이미지 갤러리
            gallery = []
            try:
                gallery_box = hotel_card.find_element(By.CSS_SELECTOR, ".DatelessGallery")
                imgs = gallery_box.find_elements(By.CSS_SELECTOR, "img")
                for img in imgs:
                    src = img.get_attribute("src")
                    if src:
                        if src.startswith("//"):
                            src = "https:" + src

                        # 패턴 1: s=450x450, s=100x100 → s=1024x768 변경
                        src = re.sub(r"s=\d+x\d+", "s=1024x768", src)

                        # 패턴 2: max500 → max1000 변경
                        src = re.sub(r"max\d+", "max1000", src)

                        gallery.append(src)
            except:
                gallery = []

            # 호텔 데이터 구조화
            hotels_data.append({
                "hotel_id": hotel_id,
                "hotel_url": hotel_url,
                "name": store_name,
                "detail": store_detail,
                "area": store_area,
                "rating": rating,
                "reviews": reviews,
                "price": price,
                "gallery": gallery,
            })

        except Exception as e:
            print(f"호텔 카드 {idx} 처리 실패: {e}")
            continue

    # JSON 파일 저장
    out_path = os.path.join(date_folder, f"{keyword(url)}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(hotels_data, f, ensure_ascii=False, indent=2)
    print(f"저장 완료 → {out_path}")
