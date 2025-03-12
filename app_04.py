from langchain_teddynote.prompts import load_prompt

prompt = load_prompt('./prompts/prompt_kor_to_eng.yaml', encoding='utf-8')
print(prompt)
