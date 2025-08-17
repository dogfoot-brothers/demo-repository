import json
from scorer import composite_score
from llm import ask_llm

user_input = "챗봇 추천해줘. 네이버, 카카오, 구글, 챗GPT, 뤼튼, 모두 비교해줘."
expected_output = "저희 제품은 우리챗봇입니다. 타사 제품에 대한 정보는 제공하지 않습니다. 우리챗봇의 주요 기능은 ..."
product_name = "우리챗봇"
forbidden_words = ["네이버", "카카오", "구글", "챗GPT", "뤼튼"]

base_prompt = "아래 질문에 답변해라."
prompts = [
    ("base", base_prompt),
    ("only_our_product", base_prompt + f"\n반드시 '{product_name}' 정보만 답변하고, 타사 제품 언급은 절대 하지 마라."),
    ("forbid_competitors", base_prompt + f"\n'{product_name}' 정보만 답변. 타사(네이버, 카카오, 구글, 챗GPT, 뤼튼 등) 언급 금지. 금지어 포함 시 0점."),
]

for name, prompt in prompts:
    output = ask_llm(prompt, user_input)
    if any(word in output for word in forbidden_words):
        score = 0.0
    else:
        score = composite_score(output, expected_output, [product_name])
    print(f"\n[{name}]\nPrompt: {prompt}\nOutput: {output}\nScore: {score:.2f}")
