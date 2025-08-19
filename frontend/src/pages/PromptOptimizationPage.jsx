import { useState } from 'react'
import { Bot, Zap, TrendingUp, Settings, Play, Copy, Check } from 'lucide-react'

function PromptOptimizationPage() {
  const [formData, setFormData] = useState({
    user_input: '',
    expected_output: '',
    product_name: '',
    exclude_keywords: '',
    custom_mutators: ''
  })
  
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [results, setResults] = useState(null)
  const [copiedPrompt, setCopiedPrompt] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsOptimizing(true)
    
    // 디버깅: 입력 데이터 확인
    console.log('=== 입력 데이터 디버깅 ===')
    console.log('사용자 요청:', formData.user_input)
    console.log('기대 결과:', formData.expected_output)
    console.log('제품명:', formData.product_name)
    console.log('제외 키워드:', formData.exclude_keywords)
    console.log('추가 요구사항:', formData.custom_mutators)
    
    try {
      const response = await fetch('/api/prompt-optimization/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
        },
        body: JSON.stringify({
          user_input: formData.user_input,
          expected_output: formData.expected_output,
          product_name: formData.product_name,
          exclude_keywords: formData.exclude_keywords.split(',').map(w => w.trim()).filter(w => w),
          custom_mutators: formData.custom_mutators.split('\n').map(m => m.trim()).filter(m => m)
        }),
      })

      if (response.ok) {
        const result = await response.json()
        console.log('=== 응답 데이터 디버깅 ===')
        console.log('응답 결과:', result)
        setResults(result)
      } else {
        throw new Error('최적화 실패')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('프롬프트 최적화 중 오류가 발생했습니다.')
    } finally {
      setIsOptimizing(false)
    }
  }

  const copyToClipboard = async (text, type) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedPrompt(type)
      setTimeout(() => setCopiedPrompt(''), 2000)
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
  }

  const loadExample = (example) => {
    setFormData({
      user_input: example.user_input,
      expected_output: example.expected_output || "",
      product_name: example.product_name,
      exclude_keywords: example.exclude_keywords.join(', '),
      custom_mutators: example.custom_mutators
    })
    setResults(null)
  }

  const examples = [
    {
      title: "고객 사과 메일",
      description: "애매한 요청을 구체적이고 효과적인 프롬프트로 변환",
      data: {
        user_input: "고객에게 사과 메일 써줘",
        expected_output: "정중하고 구체적인 사과 메일로, 사과 이유와 해결책을 포함",
        product_name: "고객서비스",
        exclude_keywords: ["절대", "전혀", "아예"],
        custom_mutators: "데이터 기반 분석, 구체적 일정과 해결책 포함, 재발 방지책 제시"
      }
    },
    {
      title: "회사 소개서 작성",
      description: "간단한 요청을 전문적이고 구조화된 프롬프트로 개선",
      data: {
        user_input: "회사 소개서 작성",
        expected_output: "전문적이고 매력적인 회사 소개서로, 비전, 미션, 핵심 가치를 포함",
        product_name: "회사",
        exclude_keywords: ["거짓", "과장"],
        custom_mutators: "구체적 수치와 성과 포함, 시각적 요소 활용, 투자자 관점에서 작성"
      }
    },
    {
      title: "프로젝트 계획서",
      description: "애매한 요청을 실행 가능한 구체적 지시사항으로 변환",
      data: {
        user_input: "프로젝트 계획서 만들기",
        expected_output: "구체적이고 실행 가능한 프로젝트 계획서로, 목표, 일정, 리소스를 포함",
        product_name: "프로젝트",
        exclude_keywords: ["불가능", "어려움"],
        custom_mutators: "Gantt 차트 형태로 일정 제시, 리스크 분석 포함, 성공 지표 명시"
      }
    },
    {
      title: "마케팅 전략 수립",
      description: "추상적인 요청을 구체적인 실행 계획으로 변환",
      data: {
        user_input: "마케팅 전략 좀 제안해줘",
        expected_output: "데이터 기반의 구체적인 마케팅 전략으로, 타겟 고객, 채널, 예산, KPI를 포함",
        product_name: "마케팅",
        exclude_keywords: ["모든", "무조건"],
        custom_mutators: "ROI 분석 포함, A/B 테스트 계획, 경쟁사 분석, 예산 효율성 최적화"
      }
    },
    {
      title: "기술 문서 작성",
      description: "기술적 요청을 명확하고 체계적인 문서로 변환",
      data: {
        user_input: "API 사용법 문서 써줘",
        expected_output: "개발자가 쉽게 이해할 수 있는 기술 문서로, 인증, 엔드포인트, 예시 코드를 포함",
        product_name: "API",
        exclude_keywords: ["복잡", "어려움"],
        custom_mutators: "단계별 스크린샷 포함, 실제 사용 예시 코드, 트러블슈팅 가이드, FAQ 섹션"
      }
    },
    {
      title: "비즈니스 제안서",
      description: "비즈니스 아이디어를 구체적이고 설득력 있는 제안서로 변환",
      data: {
        user_input: "새로운 서비스 아이디어 제안서 작성",
        expected_output: "투자자와 고객을 설득할 수 있는 제안서로, 시장 기회, 수익 모델, 실행 계획을 포함",
        product_name: "서비스",
        exclude_keywords: ["불확실", "모름"],
        custom_mutators: "시장 규모 수치화, 수익 예측 모델, 경쟁 우위 분석, 투자 수익률 계산"
      }
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Zap className="w-8 h-8 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">AutoPromptix</h1>
          </div>
          <p className="text-xl text-gray-600">
            AI가 자동으로 프롬프트를 최적화하여 원하는 결과를 얻어보세요
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <Settings className="w-6 h-6 mr-2 text-gray-600" />
                프롬프트 설정
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    사용자 입력
                  </label>
                  <textarea
                    name="user_input"
                    value={formData.user_input}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                    placeholder="예: 고객에게 사과 메일 써줘"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    기대 결과 (결과물 형태)
                  </label>
                  <textarea
                    name="expected_output"
                    value={formData.expected_output}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                    placeholder="예: 투자자와 고객을 설득할 수 있는 제안서로, 시장 기회, 수익 모델, 실행 계획을 포함"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    제품/서비스 이름
                  </label>
                  <input
                    type="text"
                    name="product_name"
                    value={formData.product_name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="예: 고객서비스, 제품"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    제외 키워드 (쉼표로 구분)
                  </label>
                  <input
                    type="text"
                    name="exclude_keywords"
                    value={formData.exclude_keywords}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="예: 절대, 전혀, 아예"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    추가 요구사항 (작성 스타일)
                  </label>
                  <textarea
                    name="custom_mutators"
                    value={formData.custom_mutators}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                    placeholder="예: 데이터 기반 분석, 구체적 수치 포함, 실행 가능한 액션 플랜 제시"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isOptimizing}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {isOptimizing ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      최적화 중...
                    </>
                  ) : (
                    <>
                      <Play className="w-5 h-5 mr-2" />
                      프롬프트 최적화 시작
                    </>
                  )}
                </button>
              </form>

              {/* Examples */}
              <div className="mt-6">
                <h3 className="text-lg font-medium text-gray-700 mb-3">예시 템플릿</h3>
                <div className="space-y-2">
                  {examples.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => loadExample(example.data)}
                      className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm text-gray-700 transition-colors"
                    >
                      <div className="font-medium">{example.title}</div>
                      <div className="text-gray-500 text-xs">{example.description}</div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="lg:col-span-2">
            {results ? (
              <div className="space-y-6">
                {/* Best Result */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-2xl font-semibold mb-4 flex items-center">
                    <TrendingUp className="w-6 h-6 mr-2 text-green-600" />
                    최적화 결과
                  </h2>
                  
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-green-800">최고 점수</span>
                      <span className="text-2xl font-bold text-green-600">
                        {(results.best_score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="text-sm text-green-700">
                      {results.optimization_summary?.best_variant} 변이 사용
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        최적화된 프롬프트
                      </label>
                      <div className="relative">
                        <textarea
                          value={results.best_prompt}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                          rows="4"
                        />
                        <button
                          onClick={() => copyToClipboard(results.best_prompt, 'prompt')}
                          className="absolute top-2 right-2 p-2 text-gray-500 hover:text-gray-700"
                        >
                          {copiedPrompt === 'prompt' ? (
                            <Check className="w-4 h-4 text-green-600" />
                          ) : (
                            <Copy className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        생성된 출력
                      </label>
                      <div className="relative">
                        <textarea
                          value={results.best_output}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                          rows="4"
                        />
                        <button
                          onClick={() => copyToClipboard(results.best_output, 'output')}
                          className="absolute top-2 right-2 p-2 text-gray-500 hover:text-gray-700"
                        >
                          {copiedPrompt === 'output' ? (
                            <Check className="w-4 h-4 text-green-600" />
                          ) : (
                            <Copy className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                {/* All Trials */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold mb-4">모든 시도 결과</h3>
                  <div className="space-y-3">
                    {results.all_trials.map((trial, index) => (
                      <div
                        key={index}
                        className={`p-4 rounded-lg border ${
                          trial.name === results.optimization_summary?.best_variant
                            ? 'border-green-200 bg-green-50'
                            : 'border-gray-200 bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-gray-900">
                            {trial.name} {trial.name === results.optimization_summary?.best_variant && '⭐'}
                          </span>
                          <span className="text-sm font-medium text-gray-600">
                            {(trial.score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          <strong>프롬프트:</strong> {trial.prompt}
                        </div>
                        <div className="text-sm text-gray-700">
                          <strong>출력:</strong> {trial.output}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-900 mb-2">
                  프롬프트 최적화 준비 완료
                </h3>
                <p className="text-gray-600">
                  왼쪽에서 프롬프트 설정을 입력하고 최적화를 시작해보세요.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PromptOptimizationPage
