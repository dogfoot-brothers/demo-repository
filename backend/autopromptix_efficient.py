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
    
    async def evaluate_prompt(self, prompt: str, user_input: str, expected_output: str, keywords: List[str], exclude_keywords: List[str], custom_mutators: List[str] = [], evaluation_weights: Dict = {}) -> float:
        """AI 기반 프롬프트 평가 (0-100점)"""
        try:
            output = await ask_llm(prompt, user_input)
            
            # 가중치 설정 (비율 기반)
            raw_weights = {
                'exclude_keywords': evaluation_weights.get('exclude_keywords', 25),
                'product_name': evaluation_weights.get('product_name', 25), 
                'expected_output': evaluation_weights.get('expected_output', 25),
                'custom_requirements': evaluation_weights.get('custom_requirements', 25)
            }
            
            # 총합을 구해서 비율로 변환 (0-100점 기준)
            total_weight = sum(raw_weights.values())
            if total_weight > 0:
                weights = {key: (value / total_weight) * 100 for key, value in raw_weights.items()}
            else:
                weights = {key: 25 for key in raw_weights.keys()}  # 기본값
            
            logger.info(f"Evaluation weights: {weights}")
            
            # AI 평가 프롬프트 생성
            evaluation_prompt = f"""
다음 응답을 4가지 기준으로 평가하여 0-100점 사이의 점수를 매겨라:

**평가 대상 응답:**
{output}

**평가 기준 (가중치 적용):**

1. **제외 키워드 준수 ({weights['exclude_keywords']}점)**: 다음 단어들이 포함되지 않았는가?
   제외 키워드: {', '.join(exclude_keywords) if exclude_keywords else '없음'}
   - 제외 키워드가 하나도 없으면 {weights['exclude_keywords']}점
   - 제외 키워드가 1개 있으면 {weights['exclude_keywords'] * 0.6:.0f}점
   - 제외 키워드가 2개 이상 있으면 0점

2. **제품/서비스 이름 포함 ({weights['product_name']}점)**: 다음 이름이 적절히 포함되었는가?
   필수 포함: {', '.join(keywords) if keywords else '없음'}
   - 자연스럽게 여러 번 포함되면 {weights['product_name']}점
   - 1-2번 포함되면 {weights['product_name'] * 0.6:.0f}점
   - 포함되지 않으면 0점

3. **기대 결과 달성 ({weights['expected_output']}점)**: 다음 기대 결과를 얼마나 잘 충족했는가?
   기대 결과: {expected_output}
   - 완벽히 충족하면 {weights['expected_output']}점
   - 대부분 충족하면 {weights['expected_output'] * 0.8:.0f}점
   - 부분적으로 충족하면 {weights['expected_output'] * 0.4:.0f}점
   - 충족하지 못하면 0점

4. **추가 요구사항 반영 ({weights['custom_requirements']}점)**: 다음 요구사항이 얼마나 잘 반영되었는가?
   추가 요구사항: {', '.join(custom_mutators) if custom_mutators else '없음'}
   - 모든 요구사항 반영하면 {weights['custom_requirements']}점
   - 대부분 반영하면 {weights['custom_requirements'] * 0.8:.0f}점
   - 일부만 반영하면 {weights['custom_requirements'] * 0.4:.0f}점
   - 반영되지 않으면 0점

**총점 계산:**
각 기준별 점수를 합산하여 최종 점수 산출 (최대 100점)

**응답 형식:**
{{"score": 점수(0-100), "breakdown": {{"exclude_keywords": 점수1, "product_name": 점수2, "expected_output": 점수3, "custom_requirements": 점수4}}, "reasoning": "각 기준별 평가 이유와 점수 산정 근거"}}

점수를 정확히 계산하여 JSON 형태로 응답해라.
"""
            
            # AI 평가 실행
            evaluation_response = await ask_llm(evaluation_prompt, "평가 요청")
            logger.info(f"AI evaluation response: {evaluation_response}")
            
            # JSON 파싱 시도
            try:
                import json
                # 응답에서 JSON 부분만 추출
                if '{' in evaluation_response and '}' in evaluation_response:
                    start = evaluation_response.find('{')
                    end = evaluation_response.rfind('}') + 1
                    json_str = evaluation_response[start:end]
                    evaluation_result = json.loads(json_str)
                    
                    score = evaluation_result.get('score', 50) / 100.0  # 0-1 범위로 변환
                    breakdown = evaluation_result.get('breakdown', {})
                    reasoning = evaluation_result.get('reasoning', '')
                    
                    logger.info(f"AI Evaluation - Score: {score*100:.1f}/100")
                    logger.info(f"Breakdown: {breakdown}")
                    logger.info(f"Reasoning: {reasoning}")
                    
                    # AI 평가 결과를 그대로 사용 (기존 점수 보정 제거)
                    return max(0.0, min(1.0, score))  # 0-1 범위 보장
                    
            except Exception as parse_error:
                logger.error(f"Failed to parse AI evaluation: {parse_error}")
                
            # 파싱 실패시 기본 평가로 폴백
            logger.info("Falling back to basic evaluation")
            base_score = composite_score(output, expected_output, keywords)
            from scorer_simple import final_score_with_forbidden_check
            final_score = final_score_with_forbidden_check(base_score, output, exclude_keywords)
            
            logger.info(f"Fallback score: {final_score}")
            return final_score
            
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
            score = await self.evaluate_prompt(prompt, user_input, expected_output, keywords, exclude_keywords_filtered, custom_mutators)
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

    async def generate_smart_mutations(self, base_prompt: str, user_input: str, analysis: Dict[str, str], custom_mutators: List[str] = [], exclude_keywords: List[str] = [], product_name: str = "") -> List[tuple]:
        """사용자 입력 분석 결과를 바탕으로 스마트한 변이 생성"""
        
        direction = analysis.get("direction", "구체성")
        instructions = analysis.get("instructions", "구체적인 내용을 포함하여 작성")
        
        # 공통 텍스트 준비
        exclude_text = ""
        if exclude_keywords:
            exclude_text = f"\n\n중요: 다음 단어들은 절대 사용하지 마라: {', '.join(exclude_keywords)}"
        
        product_text = ""
        if product_name:
            product_text = f"\n\n제품/서비스 이름: '{product_name}'을(를) 답변에 자연스럽게 포함시켜라."
        
        custom_text = ""
        if custom_mutators:
            custom_instructions = "\n".join([f"- {mutator}" for mutator in custom_mutators])
            custom_text = f"\n\n추가 요구사항:\n{custom_instructions}"
        
        # 기본 변이 (이미 모든 요구사항 포함됨)
        mutations = [("base", base_prompt)]
        
        # 사용자 정의 변이 추가 (우선순위 높음) - 기본 변이와 동일하게 모든 요구사항 포함
        mutations.append(("custom", base_prompt + f"\n\n강화된 사용자 맞춤 접근법 적용"))
        
        # 방향에 따른 맞춤형 변이 (모든 요구사항 포함)
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
                ("tone", base_prompt + f"\n\n답변은 반드시 다음 형식으로 작성해라:\n1. 전문적이고 설득력 있는 어조 사용\n2. 구체적인 수치와 데이터 포함\n3. 투자자/고객이 원하는 핵심 정보 우선 배치\n4. 각 섹션마다 명확한 제목과 요약 포함{exclude_text}"),
                ("format", base_prompt + f"\n\n답변은 반드시 다음 구조로 작성해라:\n- 제목: [명확한 제목]\n- 요약: [핵심 내용 2-3줄]\n- 상세 내용: [번호와 불릿으로 구체적 단계 제시]\n- 결론: [실행 가능한 다음 단계 제시]\n- 부록: [참고 자료나 추가 정보]{exclude_text}")
            ])
        
        return mutations

# 기존 함수명과의 호환성
async def optimize_prompt_simple(*args, **kwargs):
    """기존 함수명과의 호환성"""
    optimizer = SimpleOptimizer()
    return await optimizer.optimize_prompt_simple(*args, **kwargs)

async def optimize_prompt_streaming(
    user_input: str,
    expected_output: str,
    product_name: str,
    exclude_keywords: List[str],
    custom_mutators: List[str] = [],
    evaluation_weights: Dict = {},
    stop_event=None
):
    """Streaming version of prompt optimization that yields results as they're generated"""
    optimizer = SimpleOptimizer()
    
    # Send initial status
    yield {
        "type": "status",
        "data": {
            "message": "Starting prompt optimization...",
            "step": "init"
        }
    }
    # Force async yield to allow message to be sent
    import asyncio
    await asyncio.sleep(0)
    
    # 키워드 설정 (제품명만)
    keywords = [product_name]
    exclude_keywords_filtered = exclude_keywords
    
    # 기본 프롬프트 - 모든 요구사항 포함
    exclude_text = ""
    if exclude_keywords_filtered:
        exclude_text = f"\n\n중요: 다음 단어들은 절대 사용하지 마라: {', '.join(exclude_keywords_filtered)}"
    
    product_text = ""
    if product_name:
        product_text = f"\n\n제품/서비스 이름: '{product_name}'을(를) 답변에 자연스럽게 포함시켜라."
    
    custom_text = ""
    if custom_mutators:
        custom_instructions = "\n".join([f"- {mutator}" for mutator in custom_mutators])
        custom_text = f"\n\n추가 요구사항:\n{custom_instructions}"
    
    base_prompt = f"""사용자 요청: {user_input}

기대 결과: {expected_output}

위 요청에 맞는 구체적이고 실용적인 답변을 작성해라.{product_text}{custom_text}{exclude_text}"""
    
    # 사용자 입력 분석
    yield {
        "type": "status",
        "data": {
            "message": "Analyzing user input...",
            "step": "analysis"
        }
    }
    
    analysis = await optimizer.analyze_user_input(user_input)
    
    yield {
        "type": "analysis",
        "data": {
            "analysis": analysis,
            "message": f"Analysis complete: {analysis.get('direction', 'Unknown')}"
        }
    }
    # Force async yield to allow message to be sent
    await asyncio.sleep(0)
    
    # 스마트 변이 생성
    yield {
        "type": "status",
        "data": {
            "message": "Generating prompt variations...",
            "step": "mutation"
        }
    }
    
    base_mutations = await optimizer.generate_smart_mutations(base_prompt, user_input, analysis, custom_mutators, exclude_keywords_filtered, product_name)
    
    yield {
        "type": "mutations",
        "data": {
            "mutations": [{"name": name, "prompt": prompt} for name, prompt in base_mutations],
            "message": f"Generated {len(base_mutations)} variations"
        }
    }
    # Force async yield to allow message to be sent
    await asyncio.sleep(0)
    
    # 평가 시작
    yield {
        "type": "status",
        "data": {
            "message": "Evaluating prompt variations...",
            "step": "evaluation"
        }
    }
    
    gen0_results = {}
    all_trials = []
    
    # Process variations one by one but with immediate streaming
    for i, (name, prompt) in enumerate(base_mutations):
        # Check for stop signal
        if stop_event and stop_event.is_set():
            logger.info("Stop signal received, breaking optimization loop")
            return
            
        # Send evaluation start
        yield {
            "type": "evaluation_start",
            "data": {
                "name": name,
                "index": i,
                "total": len(base_mutations),
                "message": f"Evaluating variation {i+1}/{len(base_mutations)}: {name}"
            }
        }
        await asyncio.sleep(0)
        
        try:
            # Generate output
            from llm import ask_llm
            output = await ask_llm(prompt, user_input)
            
            # Send LLM response immediately
            yield {
                "type": "llm_response",
                "data": {
                    "name": name,
                    "prompt": prompt,
                    "output": output,
                    "message": f"Generated response for '{name}'"
                }
            }
            await asyncio.sleep(0)
            
            # Evaluate the prompt
            score = await optimizer.evaluate_prompt(prompt, user_input, expected_output, keywords, exclude_keywords_filtered, custom_mutators, evaluation_weights)
            gen0_results[name] = score
            
            trial_result = {
                "name": name,
                "prompt": prompt,
                "score": score,
                "output": output
            }
            all_trials.append(trial_result)
            
            # Send evaluation result immediately
            yield {
                "type": "evaluation_result",
                "data": {
                    "trial": trial_result,
                    "message": f"Variation '{name}' scored {score:.3f}"
                }
            }
            await asyncio.sleep(0)
            
        except Exception as e:
            logger.error(f"Error processing variation {name}: {e}")
            continue
    
    # 최고 점수 선택 (안전 체크)
    if not gen0_results:
        logger.error("No results generated - all variations failed")
        return
        
    best_gen0 = max(gen0_results.items(), key=lambda x: x[1])
    current_best_score = best_gen0[1]
    
    # 최고 점수에 해당하는 프롬프트 찾기
    best_prompt = base_mutations[0][1]  # 기본값
    for name, prompt in base_mutations:
        if name == best_gen0[0]:
            best_prompt = prompt
            break
    
    initial_score = gen0_results.get("base", 0.5)
    improvement = current_best_score - initial_score
    
    # Send final results
    yield {
        "type": "final_results",
        "data": {
            "best_prompt": best_prompt,
            "best_output": await ask_llm(best_prompt, user_input),
            "best_score": round(current_best_score, 3),
            "all_trials": all_trials,
            "total_evaluations": len(gen0_results),
            "generations_completed": 1,
            "best_variant": best_gen0[0],
            "improvement_achieved": improvement > 0,
            "score_improvement": round(improvement, 3),
            "initial_score": round(initial_score, 3),
            "message": f"Optimization complete! Best score: {current_best_score:.3f} (improvement: {improvement:.3f})"
        }
    }
