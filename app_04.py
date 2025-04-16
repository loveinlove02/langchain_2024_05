from openai import OpenAI
import os
from PIL import Image
import requests
from datetime import datetime
from io import BytesIO

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_and_save_image(prompt):
    # 이미지 생성
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    # 이미지 URL 가져오기
    image_url = response.data[0].url
    
    # 이미지 다운로드
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    
    # 저장할 디렉토리 생성
    if not os.path.exists('generated_images'):
        os.makedirs('generated_images')
    
    # 현재 시간을 파일명에 포함
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'generated_images/dalle_image_{timestamp}.png'
    
    # 이미지 저장
    image.save(filename)
    print(f'이미지가 저장되었습니다: {filename}')
    return filename

# 사용 예시
generate_and_save_image('소녀가 고양이를 앉고 있는 사진을 만들어 주세요.')
