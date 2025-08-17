def mutate_tone_polite(prompt):
    return prompt + "\n정중한 어조로, 존댓말을 사용해라."

def mutate_require_keywords(prompt, keywords):
    return prompt + f"\n반드시 다음 키워드를 포함: {', '.join(keywords)}"

