from bs4 import BeautifulSoup
import json, os, re
from datetime import datetime

# ===== 1) 날짜 기반 경로 설정 =====
year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")

base_folder = os.path.join("klookCity", year, month)
os.makedirs(base_folder, exist_ok=True)

# ===== 2) HTML 파일 목록 =====
html_files = [f for f in os.listdir(base_folder) if f.endswith(".html")]

if not html_files:
    print(f"❌ HTML 파일이 없습니다 → {base_folder}")
    exit()

print(f"✅ {year}/{month} 폴더에서 {len(html_files)}개의 파일 처리 시작...")

# ===== 3) 파일 반복 =====
for html_file in html_files:
    html_path = os.path.join(base_folder, html_file)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # ==============================
    # 🔹 1) 가볼만한곳
    # ==============================
    attractions = []
    for card in soup.select("#s-DestinationTopPois .responsive-card-item .poi-card"):
        title_tag = card.select_one("h3.poi-card-title a")
        title = re.sub(r"\s+", " ", title_tag.get_text(strip=True)) if title_tag else ""
        link = title_tag.get("href") if title_tag else ""

        score_tag = card.select_one(".poi-score")
        score = score_tag.get_text(strip=True) if score_tag else ""

        desc_tag = card.select_one(".poi-card-desc")
        desc = re.sub(r"\s+", " ", desc_tag.get_text(separator=" ", strip=True)) if desc_tag else ""

        attractions.append({
            "title": title,
            "link": link,
            "score": score,
            "description": desc
        })

    # ==============================
    # 🔹 2) 숙소
    # ==============================
    hotels = []
    for card in soup.select("#s-DestinationHotelActs .responsive-card-item"):
        title_tag = card.select_one("h3.card-title a")
        title = re.sub(r"\s+", " ", title_tag.get_text(strip=True)) if title_tag else ""
        link = title_tag.get("href") if title_tag else ""

        score_tag = card.select_one(".review-star")
        score = score_tag.get_text(strip=True).replace("★", "").strip() if score_tag else ""

        review_tag = card.select_one(".review-booked")
        reviews = ""
        if review_tag:
            match = re.search(r"\(([\d,]+)\)", review_tag.get_text())
            if match:
                reviews = match.group(1).replace(",", "")

        price_tag = card.select_one(".sell-price .price-number")
        price = price_tag.get_text(strip=True) if price_tag else "" 

        hotels.append({
            "title": title,
            "link": link,
            "score": score,
            "reviews": reviews,
            "price": price
        })

    # ==============================
    # 🔹 3) 인기 순위 (#s-Recommended 안 첫 번째 섹션만)
    # ==============================
    popular = []

    wrapper = soup.select_one("#s-Recommended .internal-linking-wrapper-desktop")
    if wrapper:
        first_section = wrapper.select_one("div.internal-linking-section")
        if first_section:
            for li in first_section.select("ul.link-list-wrapper li"):
                rank_tag = li.select_one(".link-index")
                title_tag = li.select_one("a")

                rank = rank_tag.get_text(strip=True) if rank_tag else ""
                title = re.sub(r"\s+", " ", title_tag.get_text(strip=True)) if title_tag else ""
                link = title_tag.get("href") if title_tag else ""

                popular.append({
                    "rank": rank,
                    "title": title,
                    "link": link
                })

    # ==============================
    # 🔹 JSON 저장
    # ==============================
    json_name = f"{os.path.splitext(html_file)[0]}.json"
    output_path = os.path.join(base_folder, json_name)

    data = {
        "가볼만한곳": attractions,
        "숙소": hotels,
        "인기순위": popular
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 변환 완료 → {json_name}")

print(f"\n🎉 전체 {len(html_files)}개 파일 처리 완료 → {base_folder}")
