from langchain_community.agent_toolkits import FileManagementToolkit

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 폴더 생성하고 시작.
if not os.path.exists('tmp'):   # tmp 라는 폴더가 없으면
    os.mkdir('tmp')             # tmp 라는 이름의 폴더를 만든다

# FileManagementToolkit 
# CopyFileTool      : 파일 복사
# DeleteFileTool    : 파일 삭제
# FileSearchTool    : 파일 검색
# MoveFileTool      : 파일 이동
# ReadFileTool      : 파일 읽기
# WriteFileTool     : 파일 쓰기
# ListDirectoryTool : 디렉토리 목록 조회

working_directory = 'tmp'       # 작업 디렉토리 설정

toolkit = FileManagementToolkit(root_dir=str(working_directory))

available_tools = toolkit.get_tools()       # 사용가능한 도구 가져오기

for tool in available_tools:
    print(f' - {tool.name} : {tool.description}')


# 도구 중에서 필요한 것만 지정해서 사용 가능
tools = FileManagementToolkit(
    root_dir=str(working_directory),
    selected_tools=['read_file', 'file_delete', 'write_file', 'list_directory']     
).get_tools()

print(tools)
