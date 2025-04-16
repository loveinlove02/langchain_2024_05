from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from IPython.display import Image, display
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(verbose=True)
google_key = os.getenv('GOOGLE_API_KEY')


# Gemini 2.0 Flash Experimental 이미지 생성 모델 사용
llm = ChatGoogleGenerativeAI(
    api_key=google_key,
    model="models/gemini-2.0-flash-exp-image-generation"
)

# 생성할 이미지에 대한 프롬프트 작성
message = {
    "role": "user",
    "content": "A Bengal cat with golden and brown fur is cooking ramen on a stove, standing on two legs like a human. The cat is wearing a small apron and holding a wooden spoon, steam rising from the pot. The kitchen is cozy and warm, illustrated in a Studio Ghibli or whimsical anime style."
}

# 이미지와 텍스트 모두 응답받도록 설정
response = llm.invoke(
    [message],
    generation_config=dict(response_modalities=["TEXT", "IMAGE"])
)

# 이미지 데이터 추출 (리스트에서 이미지 URL 찾기)
image_url = None
for content_part in response.content:
    if "image_url" in content_part:
        image_url = content_part["image_url"]["url"]
        break


if image_url:
    image_base64 = image_url.split(",")[-1]
    image_data = base64.b64decode(image_base64)
    display(Image(data=image_data, width=300))

    # 현재 시, 분, 초를 이용해 파일명 생성
    now = datetime.now()
    filename = f"generated_image_{now.strftime('%H%M%S')}.png"  # 예: generated_image_153045.png

    # 파일로 저장
    with open(filename, "wb") as f:
        f.write(image_data)
    print("이미지가 ", filename, "로 저장되었습니다.")
else:
    print("이미지를 찾을 수 없습니다.")
