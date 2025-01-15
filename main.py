import os
import re
from PIL import Image
import pytesseract

# Tesseract-OCR 경로 설정 (필요 시 경로 수정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 영수증에서 날짜와 총 금액 추출 함수
def extract_date_and_total(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='kor+eng')
        # 날짜 추출 (YYYYMMDD 형식)
        date_match = re.search(r'(\d{4}[.-]?\d{2}[.-]?\d{2})', text)
        if date_match:
            date = date_match.group(1).replace(".", "").replace("-", "")
        else:
            print(f"날짜를 찾을 수 없습니다: {image_path}")
            return None, None

        # 총 금액 추출 (숫자 뒤에 '원'이 포함된 패턴)
        total_match = re.search(r'(\d{1,3}(,\d{3})*원)', text)
        if total_match:
            total = total_match.group(1).replace(",", "")
        else:
            print(f"==> 금액 정보를 찾을 수 없습니다: {image_path}")
            return None, None

        return date, total
    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")
        return None, None

# 파일 이름 변경 함수
def rename_receipt_files(directory):
    total_price = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory, filename)

            # 날짜와 총 금액 추출
            date, total = extract_date_and_total(file_path)

            if date and total:
                # 새로운 파일 이름 생성
                new_filename = f"{date}-{total}.PNG"
                new_file_path = os.path.join(directory, new_filename)

                # 파일 이름 변경
                os.rename(file_path, new_file_path)
                print(f"파일 이름 변경 완료: {filename} -> {new_filename}")

                total_price = total_price + int(total[:-1])

    print("총 금액(인식 불가 제외): ", total_price)

# 실행 예제
directory_path = '.\src'  # 영수증 이미지 폴더 경로를 지정하세요.
rename_receipt_files(directory_path)
