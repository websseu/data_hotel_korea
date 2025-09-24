from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
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
}

# ===== 웹드라이버 설정 (로컬) =====
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
time.sleep(10)

# ===== 주소 키워드 추출 =====
def keyword(url: str) -> str:
    m = re.search(r"/city/([a-z\-]+)\.html", url)
    if not m:
        return "unknown"
    slug = m.group(1)          
    return slug.split("-")[0] 

# 모든 주소에 대해 순차적으로 작업
for city, url in urls.items():
    print(f'▶ {city} 접속: {url}')
    browser.get(url)

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
