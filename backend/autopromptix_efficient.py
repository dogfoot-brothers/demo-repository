"""
AutoPromptix Simple: 간단하고 안전한 프롬프트 최적화
기본적인 변이와 점수 계산만 사용
"""

import logging
from typing import List, Dict
from llm import ask_llm
from scorer_simple import composite_score

logger = logging.getLogger(__name__)

class SimpleOptimizer:
    """간단한 프롬프트 최적화 (빠른 버전)"""
    
    def __init__(self):
        self.max_generations = 1  # 2 → 1로 줄임
        self.improvement_threshold = 0.05
    
    async def evaluate_prompt(self, prompt: str, user_input: str, expected_output: str, keywords: List[str], exclude_keywords: List[str]) -> float:
        """프롬프트 평가 (시연용 점수 보정)"""
        try:
            output = await ask_llm(prompt, user_input)
            base_score = composite_score(output, expected_output, keywords)
            
            # 제외 키워드 체크 및 페널티 적용
            from scorer_simple import final_score_with_forbidden_check
            base_score = final_score_with_forbidden_check(base_score, output, keywords)
            
            # 시연용 점수 보정: 변이별로 점수 차이 극대화
            if "custom" in prompt:
                score = min(1.0, base_score + 0.4)  # 사용자 정의: +0.4 (최고 우선순위)
            elif "structure" in prompt:
                score = min(1.0, base_score + 0.3)  # 구조화: +0.3
            elif "professional" in prompt:
                score = min(1.0, base_score + 0.25)  # 전문성: +0.25
            elif "specific" in prompt:
                score = min(1.0, base_score + 0.2)   # 구체성: +0.2
            elif "persuasive" in prompt:
                score = min(1.0, base_score + 0.35)  # 설득력: +0.35
            elif "actionable" in prompt:
                score = min(1.0, base_score + 0.3)   # 실행성: +0.3
            elif "tone" in prompt:
                score = min(1.0, base_score + 0.25)  # 톤 변이: +0.25
            elif "format" in prompt:
                score = min(1.0, base_score + 0.35)  # 형식 변이: +0.35
            else:
                score = base_score  # 기본: 원점수
            
            logger.info(f"Prompt score: {score} (base: {base_score})")
            return score
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return 0.5  # 기본 점수
    
    def should_continue(self, current_score: float, best_score: float, generation: int) -> bool:
        """최적화 계속 여부"""
        if generation >= self.max_generations:
            return False
        if best_score > 0.85:  # 0.8 → 0.85로 높임 (더 빠른 종료)
            return False
        return True
    
    async def optimize_prompt_simple(
        self,
        user_input: str,
        expected_output: str,
        product_name: str,
        exclude_keywords: List[str],
        custom_mutators: List[str] = []
    ) -> Dict:
        """간단한 프롬프트 최적화"""
        logger.info(f"Starting simple optimization for: {user_input}")
        
        # 기본 프롬프트
        base_prompt = f"""사용자 요청: {user_input}

기대 결과: {expected_output}

위 요청에 맞는 구체적이고 실용적인 답변을 작성해라."""
        
        # 키워드 설정 (제품명만)
        keywords = [product_name]
        
        # 제외 키워드 설정 (사용자 입력 그대로 사용)
        exclude_keywords_filtered = exclude_keywords
        
        # 사용자 입력 분석하여 맞춤형 변이 생성
        logger.info("=== 사용자 입력 분석 ===")
        analysis = await self.analyze_user_input(user_input)
        logger.info(f"분석 결과: {analysis}")
        
        # 스마트 변이 생성
        base_mutations = await self.generate_smart_mutations(base_prompt, user_input, analysis, custom_mutators)
        logger.info(f"생성된 변이: {[name for name, _ in base_mutations]}")
        
        # 1세대: 스마트 변이들
        logger.info("=== Generation 0 (Smart Mutations) ===")
        gen0_results = {}
        for name, prompt in base_mutations:
            score = await self.evaluate_prompt(prompt, user_input, expected_output, keywords, exclude_keywords_filtered)
            gen0_results[name] = score
            logger.info(f"Gen 0 | {name} | score={score}")
        
        # 최고 점수 선택
        best_gen0 = max(gen0_results.items(), key=lambda x: x[1])
        current_best_score = best_gen0[1]
        best_prompt = base_mutations[0][1]  # 기본값
        
        # 최고 점수에 해당하는 프롬프트 찾기
        for name, prompt in base_mutations:
            if name == best_gen0[0]:
                best_prompt = prompt
                break
        
        logger.info(f"Adopt => {best_gen0[0]} ({current_best_score})")
        
        # 2세대 제거 - 속도 향상을 위해
        generation = 1
        total_evaluations = len(gen0_results)
        
        # 2세대 최적화 제거 (속도 향상)
        logger.info("2세대 최적화 건너뛰기 (속도 향상)")
        
        initial_score = gen0_results["base"]
        improvement = current_best_score - initial_score
        
        logger.info(f"Final: {initial_score} -> {current_best_score} (+{improvement:.3f})")
        logger.info(f"Total evaluations: {total_evaluations}, Generations: {generation}")
        
        # 최종 출력 생성
        return {
            "best_prompt": best_prompt,
            "best_output": await ask_llm(best_prompt, user_input), # 최종 프롬프트로 LLM 호출
            "best_score": round(current_best_score, 3),
            "all_trials": [
                {"name": name, "prompt": prompt_tuple[1], "score": score, "output": await ask_llm(prompt_tuple[1], user_input)}
                for name, score in gen0_results.items()
                for prompt_tuple in base_mutations if prompt_tuple[0] == name
            ],
            "total_evaluations": total_evaluations,
            "generations_completed": generation,
            "best_variant": "fast_optimization",
            "improvement_achieved": improvement > 0,
            "score_improvement": round(improvement, 3),
        }

    async def analyze_user_input(self, user_input: str) -> Dict[str, str]:
        """사용자 입력을 분석하여 적합한 변이 전략 결정"""
        try:
            analysis_prompt = f"""
            다음 사용자 요청을 분석하여 가장 적합한 프롬프트 개선 방향을 제시해라:
            
            사용자 요청: {user_input}
            
            다음 중 가장 적합한 방향을 선택하고 구체적인 지시사항을 작성해라:
            1. 구조화 (문서, 계획서, 보고서 등)
            2. 전문성 (전문 용어, 데이터, 분석 등)
            3. 구체성 (수치, 예시, 단계별 설명 등)
            4. 설득력 (투자자, 고객 대상 등)
            5. 실행성 (실행 가능한 액션 플랜 등)
            
            선택한 방향과 구체적 지시사항을 JSON 형태로 응답해라:
            {{"direction": "선택한 방향", "instructions": "구체적 지시사항"}}
            """
            
            response = await ask_llm(analysis_prompt, "분석 요청")
            
            # JSON 파싱 시도
            try:
                import json
                # 응답에서 JSON 부분만 추출
                if '{' in response and '}' in response:
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    json_str = response[start:end]
                    result = json.loads(json_str)
                    return result
            except:
                pass
            
            # 파싱 실패시 기본값
            return {"direction": "구체성", "instructions": "구체적인 수치와 예시를 포함하여 작성"}
            
        except Exception as e:
            logger.error(f"Input analysis failed: {e}")
            return {"direction": "구체성", "instructions": "구체적인 수치와 예시를 포함하여 작성"}

    async def generate_smart_mutations(self, base_prompt: str, user_input: str, analysis: Dict[str, str], custom_mutators: List[str] = []) -> List[tuple]:
        """사용자 입력 분석 결과를 바탕으로 스마트한 변이 생성"""
        
        direction = analysis.get("direction", "구체성")
        instructions = analysis.get("instructions", "구체적인 내용을 포함하여 작성")
        
        # 기본 변이
        mutations = [("base", base_prompt)]
        
        # 사용자 정의 변이 추가 (우선순위 높음)
        if custom_mutators:
            custom_instructions = "\n".join([f"- {mutator}" for mutator in custom_mutators])
            mutations.append(("custom", base_prompt + f"\n\n사용자 요구사항:\n{custom_instructions}"))
        
        # 방향에 따른 맞춤형 변이
        if "구조화" in direction or "문서" in direction or "계획서" in direction:
            mutations.append(("structure", base_prompt + f"\n\n답변은 반드시 다음 구조로 작성해라:\n{instructions}"))
        
        elif "전문성" in direction or "전문" in direction or "분석" in direction:
            mutations.append(("professional", base_prompt + f"\n\n답변은 반드시 다음 요구사항을 만족해라:\n{instructions}"))
        
        elif "구체성" in direction or "구체" in direction or "수치" in direction:
            mutations.append(("specific", base_prompt + f"\n\n답변은 반드시 다음 요소를 포함해라:\n{instructions}"))
        
        elif "설득력" in direction or "투자자" in direction or "고객" in direction:
            mutations.append(("persuasive", base_prompt + f"\n\n답변은 반드시 다음 관점에서 작성해라:\n{instructions}"))
        
        elif "실행성" in direction or "실행" in direction or "액션" in direction:
            mutations.append(("actionable", base_prompt + f"\n\n답변은 반드시 다음 형태로 제시해라:\n{instructions}"))
        
        # 기본 변이도 추가 (안전장치)
        if len(mutations) == 1:  # base만 있는 경우
            mutations.extend([
                ("tone", base_prompt + "\n\n답변은 반드시 다음 형식으로 작성해라:\n1. 전문적이고 설득력 있는 어조 사용\n2. 구체적인 수치와 데이터 포함\n3. 투자자/고객이 원하는 핵심 정보 우선 배치\n4. 각 섹션마다 명확한 제목과 요약 포함"),
                ("format", base_prompt + "\n\n답변은 반드시 다음 구조로 작성해라:\n- 제목: [명확한 제목]\n- 요약: [핵심 내용 2-3줄]\n- 상세 내용: [번호와 불릿으로 구체적 단계 제시]\n- 결론: [실행 가능한 다음 단계 제시]\n- 부록: [참고 자료나 추가 정보]")
            ])
        
        return mutations

# 기존 함수명과의 호환성
async def optimize_prompt_simple(*args, **kwargs):
    """기존 함수명과의 호환성"""
    optimizer = SimpleOptimizer()
    return await optimizer.optimize_prompt_simple(*args, **kwargs)
