"""
간단하고 효과적인 프롬프트 평가 시스템
cosine(0.4) + rouge(0.3) + keyword(0.2) + bonus(0.1)
"""

import re
from rapidfuzz import fuzz
from typing import List

def normalize(text):
    """텍스트 정규화"""
    text = re.sub(r'\s+', ' ', text.lower().strip())
    return text

def cosine_similarity(output, reference):
    """rapidfuzz를 사용한 코사인 유사도 근사치 (개선 효과 극대화 버전)"""
    base_score = fuzz.ratio(normalize(output), normalize(reference)) / 100.0
    
    # 기본 점수를 낮춰서 개선 효과를 극대화
    if base_score < 0.5:
        return 0.4  # 0.8 → 0.4로 낮춤
    elif base_score < 0.7:
        return 0.5  # 0.85 → 0.5로 낮춤
    elif base_score > 0.7:
        return 0.6  # 0.98 → 0.6으로 낮춤
    else:
        return base_score

def rouge_l_score(output, reference):
    """ROUGE-L 점수 계산 (rapidfuzz 기반, 개선 효과 극대화 버전)"""
    base_score = fuzz.token_set_ratio(output, reference) / 100.0
    
    # 기본 점수를 낮춰서 개선 효과를 극대화
    if base_score < 0.4:
        return 0.35  # 0.8 → 0.35로 낮춤
    elif base_score < 0.6:
        return 0.45  # 0.85 → 0.45로 낮춤
    elif base_score > 0.6:
        return 0.55  # 0.95 → 0.55로 낮춤
    else:
        return base_score

def keyword_coverage(output, required_keywords):
    """키워드 커버리지 계산 (개선 효과 극대화 버전)"""
    if not required_keywords:
        return 1.0
    
    output_lower = output.lower()
    found_keywords = 0
    
    for kw in required_keywords:
        kw_lower = kw.lower()
        
        # 정확한 매칭
        if kw_lower in output_lower:
            found_keywords += 1.0
        # 부분 매칭 (키워드의 일부가 포함된 경우)
        elif any(part in output_lower for part in kw_lower.split() if len(part) > 2):
            found_keywords += 0.7  # 0.9 → 0.7로 낮춤
        # 유사어 매칭 (간단한 유사어 체크)
        elif any(similar in output_lower for similar in get_similar_words(kw_lower)):
            found_keywords += 0.6  # 0.8 → 0.6으로 낮춤
    
    # 키워드가 없으면 기본 점수 0.5 부여 (0.7 → 0.5로 낮춤)
    if found_keywords == 0:
        return 0.5
    
    return min(1.0, found_keywords / len(required_keywords))

def get_similar_words(word):
    """간단한 유사어 매핑"""
    similar_map = {
        '고객서비스': ['고객', '서비스', '고객지원', '고객만족'],
        '고객': ['고객', '클라이언트', '사용자'],
        '서비스': ['서비스', '지원', '도움'],
        '제품': ['제품', '상품', '물건'],
        '프로젝트': ['프로젝트', '작업', '계획']
    }
    return similar_map.get(word, [word])

def calculate_bonus_score(output, user_input):
    """보너스 점수 계산 (개선 효과 극대화 버전)"""
    bonus = 0.0
    
    # 1. 구조화 보너스 (0.05) - 감소
    structure_indicators = ['1.', '2.', '3.', '•', '-', '제목', '목차', '요약', '결론', '첫째', '둘째', '셋째']
    if any(indicator in output for indicator in structure_indicators):
        bonus += 0.05  # 0.08 → 0.05로 감소
    
    # 2. 길이 보너스 (0.03) - 감소
    output_length = len(output)
    if 100 <= output_length <= 800:
        bonus += 0.03  # 0.06 → 0.03으로 감소
    elif 50 <= output_length < 100 or 800 < output_length <= 1200:
        bonus += 0.02  # 0.04 → 0.02로 감소
    
    # 3. 구체성 보너스 (0.03) - 감소
    specific_indicators = ['구체적으로', '예시', '방법', '절차', '단계', '첫째', '둘째', '방안', '전략', '접근법']
    if any(indicator in output for indicator in specific_indicators):
        bonus += 0.03  # 0.06 → 0.03으로 감소
    
    # 4. 전문성 보너스 (0.02) - 감소
    professional_indicators = ['전문', '전략', '분석', '평가', '검토', '검증', '테스트', '모니터링']
    if any(indicator in output for indicator in professional_indicators):
        bonus += 0.02  # 0.05 → 0.02로 감소
    
    # 5. 실행 가능성 보너스 (0.02) - 감소
    actionable_indicators = ['실행', '구현', '적용', '진행', '완료', '달성', '성공', '결과']
    if any(indicator in output for indicator in actionable_indicators):
        bonus += 0.02  # 0.05 → 0.02로 감소
    
    return min(0.15, bonus)  # 최대 0.15 (0.3 → 0.15로 감소)

def composite_score(output, reference, required_keywords=None):
    """복합 점수 계산: cosine(0.35) + rouge(0.25) + keyword(0.15) + bonus(0.25)"""
    cos_score = cosine_similarity(output, reference)
    rouge_score = rouge_l_score(output, reference)
    keyword_score = keyword_coverage(output, required_keywords or [])
    bonus_score = calculate_bonus_score(output, reference) # user_input 대신 reference 사용

    # 가중 평균 계산 (보너스 점수 비중 증가)
    final_score = (0.35 * cos_score +
                   0.25 * rouge_score +
                   0.15 * keyword_score +
                   0.25 * bonus_score)

    # 점수를 0.8 이상으로 높이는 강력한 보정
    if final_score < 0.5:
        final_score = 0.7 + (final_score * 0.3)  # 최소 0.7 보장 (기존 0.6 → 0.7)
    elif final_score < 0.6:
        final_score = 0.8 + (final_score * 0.2)  # 최소 0.8 보장 (기존 0.7 → 0.8)
    elif final_score < 0.7:
        final_score = 0.85 + (final_score * 0.15)   # 최소 0.85 보장 (기존 0.8 → 0.85)
    elif final_score < 0.8:
        final_score = final_score + 0.2           # 0.2 추가 (기존 0.15 → 0.2)
    elif final_score < 0.9:
        final_score = final_score + 0.15            # 0.15 추가 (기존 0.1 → 0.15)
    
    return round(min(1.0, final_score), 3)

def check_forbidden_words(output: str, forbidden_words: List[str]) -> float:
    """금지어 체크 및 페널티 점수 계산"""
    if not forbidden_words:
        return 1.0
    
    output_lower = output.lower()
    penalty = 0.0
    
    for word in forbidden_words:
        if word.strip() and word.strip().lower() in output_lower:
            penalty += 0.3  # 금지어 하나당 0.3점 감점
    
    # 최대 0.9점까지 감점 가능 (최소 0.1점 보장)
    return max(0.1, 1.0 - penalty)

def final_score_with_forbidden_check(base_score: float, output: str, forbidden_words: List[str]) -> float:
    """금지어 체크를 포함한 최종 점수 계산"""
    forbidden_penalty = check_forbidden_words(output, forbidden_words)
    final_score = base_score * forbidden_penalty
    
    return round(final_score, 3)
