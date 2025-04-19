from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from PIL import Image
from io import BytesIO
from datetime import datetime
import requests

from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')

prompt = '`트랄랄레로 트랄랄라`를 지브리풍으로 생성해주세요.'

dalle = DallEAPIWrapper(
    api_key=key,
    model='dall-e-3',
    size='1024x1024',
    quality='standard',
    n=1
)

print('생성 시작')

image_url = dalle.run(prompt)
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
# file_name = datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
image.save('b.png')



