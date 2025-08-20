import { useState, useEffect, useRef } from 'react'
import { Bot, Zap, TrendingUp, Settings, Play, Copy, Check, Loader } from 'lucide-react'

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
  const [streamingData, setStreamingData] = useState({
    status: null,
    analysis: null,
    mutations: [],
    evaluations: [],
    currentEvaluation: null,
    finalResults: null,
    lastCompletedIndex: -1
  })
  const [optimizationSessionId, setOptimizationSessionId] = useState(null)
  const [renderKey, setRenderKey] = useState(0)
  const [forceUpdate, setForceUpdate] = useState(0)
  const wsRef = useRef(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  // WebSocket connection management
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])
  
  // Force re-render when results change
  useEffect(() => {
    if (results) {
      setRenderKey(prev => prev + 1)
      setForceUpdate(prev => prev + 1)
    }
  }, [results])

  const connectWebSocket = (sessionId) => {
    // Use Vite proxy to ensure same-origin WS and avoid CORS/proxy issues
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/optimization/${sessionId}`
    console.log('Creating WebSocket with URL:', wsUrl)
    const ws = new WebSocket(wsUrl)
    // Store immediately so all subsequent code uses the same reference
    wsRef.current = ws
    
    ws.onopen = () => {
      console.log('WebSocket opened successfully')
      setIsOptimizing(true)
    }
    
        ws.onmessage = (event) => {
      console.log('Raw WebSocket message received:', event.data)
      try {
        const data = JSON.parse(event.data)
        console.log(`[${new Date().toISOString()}] Parsed message:`, data)
        
        switch (data.type) {
        case 'status':
          console.log('Status received:', data.data)
          setStreamingData(prev => {
            const newData = {
              ...prev,
              status: data.data
            }
            // Force immediate re-render
            setTimeout(() => setForceUpdate(v => v + 1), 0)
            return newData
          })
          break
          
        case 'analysis':
          setStreamingData(prev => ({
            ...prev,
            analysis: data.data
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          break
          
        case 'mutations':
          setStreamingData(prev => ({
            ...prev,
            mutations: data.data.mutations
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          break
          
        case 'evaluation_start':
          setStreamingData(prev => ({
            ...prev,
            currentEvaluation: data.data
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          break
          
        case 'llm_response':
          // Update status to show current progress
          setStreamingData(prev => ({
            ...prev,
            status: {
              message: `${data.data.name} 변이에 대한 응답 생성 완료`,
              step: 'llm_response'
            }
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          
          // LLM 응답이 오면 바로 화면에 보여주기 (점수 없이)
          setResults(prev => {
            const newTrial = {
              name: data.data.name,
              prompt: data.data.prompt,
              output: data.data.output,
              score: null // 아직 평가되지 않음
            }
            
            if (!prev) {
              const newResults = {
                best_prompt: data.data.prompt,
                best_output: data.data.output,
                best_score: null,
                all_trials: [newTrial],
                total_evaluations: 0,
                generations_completed: 1,
                best_variant: data.data.name,
                improvement_achieved: false,
                score_improvement: 0,
                initial_score: 0
              }
              return newResults
            } else {
              // 기존 결과에 새로운 응답 추가 (점수 없이)
              const existingTrialIndex = prev.all_trials.findIndex(trial => trial.name === data.data.name)
              let newTrials
              
              if (existingTrialIndex >= 0) {
                // 기존 결과 업데이트
                newTrials = [...prev.all_trials]
                newTrials[existingTrialIndex] = newTrial
              } else {
                // 새로운 결과 추가
                newTrials = [...prev.all_trials, newTrial]
              }
              
              const updatedResults = {
                ...prev,
                all_trials: newTrials,
                total_evaluations: newTrials.length
              }
              return updatedResults
            }
          })
          // 즉시 강제 업데이트
          setTimeout(() => {
            setForceUpdate(prev => prev + 1)
            setRenderKey(prev => prev + 1)
            // DOM 강제 업데이트
            document.body.style.display = 'none'
            document.body.offsetHeight // 강제 리플로우
            document.body.style.display = ''
          }, 0)
          break
          
        case 'evaluation_result':
          setStreamingData(prev => ({
            ...prev,
            evaluations: [...prev.evaluations, data.data.trial],
            currentEvaluation: null,
            lastCompletedIndex: prev.evaluations.length,
            status: {
              message: `${data.data.trial.name} 변이 평가 완료 (점수: ${data.data.trial.score.toFixed(3)})`,
              step: 'evaluation_complete'
            }
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          // 평가 완료되면 점수 업데이트
          setResults(prev => {
            if (!prev) return null
            
            const updatedTrials = prev.all_trials.map(trial => 
              trial.name === data.data.trial.name 
                ? { ...trial, score: data.data.trial.score }
                : trial
            )
            
            // 점수가 있는 결과들 중에서 최고 점수 찾기
            const scoredTrials = updatedTrials.filter(trial => trial.score !== null)
            const bestTrial = scoredTrials.length > 0 
              ? scoredTrials.reduce((best, current) => 
                  current.score > best.score ? current : best
                )
              : null
            
            return {
              ...prev,
              all_trials: updatedTrials,
              best_prompt: bestTrial?.prompt || prev.best_prompt,
              best_output: bestTrial?.output || prev.best_output,
              best_score: bestTrial?.score || prev.best_score,
              best_variant: bestTrial?.name || prev.best_variant,
              score_improvement: bestTrial ? bestTrial.score - (prev.initial_score || 0) : prev.score_improvement
            }
          })
          break
          
        case 'final_results':
          setStreamingData(prev => ({
            ...prev,
            finalResults: data.data,
            status: {
              message: `최적화 완료! 최고 점수: ${data.data.best_score} (개선: ${data.data.score_improvement})`,
              step: 'complete'
            }
          }))
          // Force immediate re-render
          setTimeout(() => setForceUpdate(v => v + 1), 0)
          
          // Merge final results with existing trials instead of replacing
          setResults(prev => {
            if (!prev) return data.data
            
            // Keep the existing trials that were built up during streaming
            return {
              ...data.data,
              all_trials: prev.all_trials.length > 0 ? prev.all_trials : data.data.all_trials
            }
          })
          setIsOptimizing(false)
          break
          
        case 'optimization_stopped':
          setIsOptimizing(false)
          break
          
        case 'complete':
          setIsOptimizing(false)
          break
          
        case 'error':
          console.error('Optimization error:', data.message)
          alert(`최적화 오류: ${data.message}`)
          setIsOptimizing(false)
          break
      }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
        console.error('Raw message:', event.data)
      }
    }
    
    ws.onclose = () => {
      console.log('WebSocket closed')
      setIsOptimizing(false)
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      console.error('WebSocket error details:', error)
      console.error('WebSocket readyState:', ws.readyState)
      setIsOptimizing(false)
    }
    
    return ws
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log('handleSubmit called')
    setIsOptimizing(true)
    
    // Reset streaming data
    setStreamingData({
      status: null,
      analysis: null,
      mutations: [],
      evaluations: [],
      currentEvaluation: null,
      finalResults: null,
      lastCompletedIndex: -1
    })
    setResults(null)
    
    try {
      // Generate session ID
      const sessionId = `optimization_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      setOptimizationSessionId(sessionId)
      
      // Connect WebSocket and wait for it to be ready
      console.log('About to connect WebSocket')
      const ws = connectWebSocket(sessionId)
      
      // Simple connection check - if already open, proceed immediately
      if (ws.readyState === WebSocket.OPEN) {
      } else {
        // Wait for connection with a simple timeout
        await new Promise((resolve, reject) => {
          const timeout = setTimeout(() => {
            reject(new Error('WebSocket connection timeout'))
          }, 5000)
          
          const checkConnection = () => {
            if (ws.readyState === WebSocket.OPEN) {
              clearTimeout(timeout)
              resolve()
            } else if (ws.readyState === WebSocket.CLOSED || ws.readyState === WebSocket.CLOSING) {
              clearTimeout(timeout)
              reject(new Error('WebSocket connection failed'))
            } else {
              // Still connecting, check again in 100ms
              setTimeout(checkConnection, 100)
            }
          }
          
          checkConnection()
        })
      }
      
      // Send optimization request
      const requestData = {
        type: "optimization_request",
        user_input: formData.user_input,
        expected_output: formData.expected_output,
        product_name: formData.product_name,
        exclude_keywords: formData.exclude_keywords.split(',').map(w => w.trim()).filter(w => w),
        custom_mutators: formData.custom_mutators.split('\n').map(m => m.trim()).filter(m => m)
      }
      ws.send(JSON.stringify(requestData))
    } catch (error) {
      console.error('Error starting optimization:', error)
      alert('최적화 시작 중 오류가 발생했습니다. 다시 시도해주세요.')
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
          <p className="text-xl text-gray-600">
            AI 기반 자동프롬프트 최적화를 통해 원하는 결과를 얻어보세요
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
                
                {isOptimizing && (
                  <button
                    type="button"
                    onClick={() => {
                      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                        // 백엔드에 중단 시그널 전송
                        wsRef.current.send(JSON.stringify({
                          type: "stop_optimization"
                        }))
                      }
                      setIsOptimizing(false)
                      setStreamingData({
                        status: null,
                        analysis: null,
                        mutations: [],
                        evaluations: [],
                        currentEvaluation: null,
                        finalResults: null,
                        lastCompletedIndex: -1
                      })
                    }}
                    className="w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 flex items-center justify-center mt-2"
                  >
                    최적화 중단
                  </button>
                )}
                

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
            {/* Streaming Progress - Always show when optimizing */}
            {isOptimizing && (
              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-2xl font-semibold mb-4 flex items-center">
                  <Loader className="w-6 h-6 mr-2 text-blue-600 animate-spin" />
                  최적화 진행 중...
                </h2>
                
                {/* Status */}
                {streamingData.status && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
                      <span className="text-blue-800">{streamingData.status.message}</span>
                    </div>
                  </div>
                )}
                

                
                {/* Analysis */}
                {streamingData.analysis && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <h3 className="font-medium text-green-800 mb-2">분석 완료</h3>
                    <p className="text-green-700">{streamingData.analysis.message}</p>
                    <div className="mt-2 text-sm text-green-600">
                      방향: {streamingData.analysis.analysis?.direction || 'Unknown'}
                    </div>
                  </div>
                )}
                
                {/* Mutations */}
                {streamingData.mutations.length > 0 && (
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
                    <h3 className="font-medium text-purple-800 mb-2">프롬프트 변이 생성</h3>
                    <p className="text-purple-700">{streamingData.mutations.length}개의 변이가 생성되었습니다.</p>
                    <div className="mt-2 space-y-1">
                      {streamingData.mutations.map((mutation, index) => (
                        <div key={index} className="text-sm text-purple-600">
                          • {mutation.name}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Current Evaluation */}
                {streamingData.currentEvaluation && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-yellow-600 mr-3"></div>
                      <span className="text-yellow-800">
                        {streamingData.currentEvaluation.message}
                      </span>
                    </div>
                    <div className="mt-2 text-sm text-yellow-600">
                      진행률: {streamingData.currentEvaluation.index + 1}/{streamingData.currentEvaluation.total}
                    </div>
                    {/* Progress bar */}
                    <div className="mt-2 w-full bg-yellow-200 rounded-full h-2">
                      <div 
                        className="bg-yellow-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${((streamingData.currentEvaluation.index + 1) / streamingData.currentEvaluation.total) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                )}
                
                {/* Overall Progress */}
                {streamingData.mutations.length > 0 && (
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">전체 진행률</span>
                      <span className="text-sm text-gray-600">
                        {streamingData.evaluations.length}/{streamingData.mutations.length} 완료
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${(streamingData.evaluations.length / streamingData.mutations.length) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                )}
                
                {/* Completed Evaluations - Show in real-time */}
                {streamingData.evaluations.length > 0 && (
                  <div className="space-y-2">
                    <h3 className="font-medium text-gray-800">완료된 평가 ({streamingData.evaluations.length})</h3>
                    {streamingData.evaluations.map((evaluation, index) => (
                      <div key={index} className={`bg-gray-50 border rounded-lg p-3 transition-all duration-300 ${
                        index === streamingData.lastCompletedIndex ? 'border-green-300 bg-green-50' : 'border-gray-200'
                      }`}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center">
                            <span className="font-medium text-gray-900">{evaluation.name}</span>
                            {index === streamingData.lastCompletedIndex && (
                              <span className="ml-2 px-2 py-1 text-xs bg-green-500 text-white rounded-full animate-pulse">
                                New
                              </span>
                            )}
                          </div>
                          <span className="text-sm font-medium text-gray-600">
                            {(evaluation.score * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          <strong>프롬프트:</strong> 
                          <div className="mt-1 p-2 bg-white border rounded text-gray-700 whitespace-pre-wrap max-h-20 overflow-y-auto">
                            {evaluation.prompt}
                          </div>
                        </div>
                        <div className="text-sm text-gray-700">
                          <strong>출력:</strong>
                          <div className="mt-1 p-2 bg-white border rounded text-gray-800 whitespace-pre-wrap max-h-32 overflow-y-auto">
                            {evaluation.output}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Completion Message */}
                {streamingData.finalResults && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center">
                      <div className="w-4 h-4 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-green-800 font-medium">최적화 완료!</span>
                    </div>
                    <p className="text-green-700 mt-1">{streamingData.finalResults.message}</p>
                  </div>
                )}
              </div>
            )}
            
            {/* Results - Show only after optimization is complete */}
            {results && !isOptimizing ? (
              <div key={`${renderKey}-${forceUpdate}`} className="space-y-6">
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
                        {results.best_score !== null ? `${(results.best_score * 100).toFixed(1)}%` : '평가 중...'}
                      </span>
                    </div>
                    <div className="text-sm text-green-700">
                      {results.best_variant} 변이 사용
                      {results.score_improvement > 0 && (
                        <span className="ml-2 text-green-600">
                          (+{(results.score_improvement * 100).toFixed(1)}% 개선)
                        </span>
                      )}
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
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap min-h-[8rem] max-h-[20rem] overflow-y-auto">
                          {results.best_output}
                        </div>
                        <button
                          onClick={() => copyToClipboard(results.best_output, 'output')}
                          className="absolute top-2 right-2 p-2 text-gray-500 hover:text-gray-700 bg-white rounded shadow-sm"
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
                        key={`${trial.name}-${trial.score}-${forceUpdate}-${index}`}
                        className={`p-4 rounded-lg border ${
                          trial.name === results.best_variant
                            ? 'border-green-200 bg-green-50'
                            : 'border-gray-200 bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-gray-900">
                            {trial.name} {trial.name === results.best_variant && trial.score !== null && '⭐'}
                          </span>
                          <span className="text-sm font-medium text-gray-600">
                            {trial.score !== null ? `${(trial.score * 100).toFixed(1)}%` : '평가 중...'}
                          </span>
                        </div>
                        <div className="text-sm text-gray-600 mb-2">
                          <strong>프롬프트:</strong> {trial.prompt}
                        </div>
                        <div className="text-sm text-gray-700">
                          <strong>출력:</strong>
                          <div className="mt-1 p-2 bg-white border rounded text-gray-800 whitespace-pre-wrap">
                            {trial.output}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : !isOptimizing ? (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-900 mb-2">
                  프롬프트 최적화 준비 완료
                </h3>
                <p className="text-gray-600">
                  왼쪽에서 프롬프트 설정을 입력하고 최적화를 시작해보세요.
                </p>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PromptOptimizationPage
