import { MessageCircle, Users, Clock, Shield, Bot, Zap, Brain, Sparkles } from 'lucide-react'

function HomePage({ onPageChange }) {
  const openChatWidget = () => {
    // Dispatch a custom event to open the chat widget
    window.dispatchEvent(new CustomEvent('openChatWidget'));
  }

  const goToPromptOptimization = () => {
    onPageChange('prompt-optimization');
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16 px-4">
        <div className="mb-8">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <MessageCircle className="h-16 w-16 text-primary-600" />
              <Bot className="h-8 w-8 text-green-600 absolute -top-2 -right-2" />
            </div>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            AI 플랫폼
            <span className="text-primary-600"> 통합 솔루션</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            고객 지원 AI 채팅과 프롬프트 최적화를 한 곳에서 경험하세요. 
            고급 언어 모델과 포괄적인 지식 베이스로 즉시 정확한 응답을 받을 수 있습니다.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={openChatWidget}
              className="btn-primary text-lg px-8 py-3"
            >
              AI 채팅 시작
            </button>
            <button 
              onClick={goToPromptOptimization}
              className="btn-secondary text-lg px-8 py-3 flex items-center"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              프롬프트 최적화
            </button>
          </div>
        </div>
      </div>

      {/* AI Features Section */}
      <div className="py-16 px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            고급 AI로 구동
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            우리의 AI 어시스턴트는 컨텍스트를 이해하고, 대화를 기억하며, 지능적인 응답을 제공합니다
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Bot className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI 어시스턴트</h3>
            <p className="text-gray-600">
              OpenAI의 GPT 모델로 구동되는 자연스러운 대화를 위한 지능형 챗봇
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Brain className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">컨텍스트 인식</h3>
            <p className="text-gray-600">
              대화 기록을 기억하고 관련성 있고 맥락적인 응답을 제공
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Zap className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">즉시 응답</h3>
            <p className="text-gray-600">
              타이핑 표시기가 있는 실시간 AI 응답으로 자연스러운 대화 흐름
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Shield className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">지식 베이스</h3>
            <p className="text-gray-600">
              포괄적인 제품 정보, 정책 및 문제 해결 가이드에 대한 액세스
            </p>
          </div>
        </div>
      </div>

      {/* Prompt Optimization Section */}
      <div className="py-16 px-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <Sparkles className="h-12 w-12 text-blue-600" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            AutoPromptix 프롬프트 최적화
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI가 자동으로 프롬프트를 변이하고 평가하여 원하는 결과를 얻는 최적의 방법을 찾아드립니다
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="text-center bg-white p-6 rounded-lg shadow-sm">
            <div className="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              1
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">프롬프트 입력</h3>
            <p className="text-gray-600">
              원하는 입력과 기대하는 출력을 정의하고 제약 조건을 설정하세요
            </p>
          </div>

          <div className="text-center bg-white p-6 rounded-lg shadow-sm">
            <div className="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              2
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">자동 최적화</h3>
            <p className="text-gray-600">
              AI가 다양한 프롬프트 변이를 생성하고 각각을 테스트하여 최적의 것을 찾습니다
            </p>
          </div>

          <div className="text-center bg-white p-6 rounded-lg shadow-sm">
            <div className="bg-blue-100 text-blue-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              3
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">결과 분석</h3>
            <p className="text-gray-600">
              최고 점수의 프롬프트와 모든 시도 결과를 상세히 분석하여 제공합니다
            </p>
          </div>
        </div>

        <div className="text-center mt-8">
          <button 
            onClick={goToPromptOptimization}
            className="bg-blue-600 text-white hover:bg-blue-700 font-medium py-3 px-8 rounded-lg transition-colors duration-200 flex items-center mx-auto"
          >
            <Sparkles className="w-5 h-5 mr-2" />
            프롬프트 최적화 시작하기
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            AI 플랫폼을 선택해야 하는 이유
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            최고의 고객 경험을 제공하기 위해 현대 기술로 구축되었습니다
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <MessageCircle className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">실시간 채팅</h3>
            <p className="text-gray-600">
              AI 기반 응답이 있는 WebSocket 기반 즉시 메시징
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Users className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">다중 세션 지원</h3>
            <p className="text-gray-600">
              AI 지원으로 여러 고객 대화를 동시에 처리
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Clock className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">24/7 가용성</h3>
            <p className="text-gray-600">
              고객을 돕기 위해 하루 24시간 사용 가능한 AI 어시스턴트
            </p>
          </div>

          <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
            <Shield className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">안전하고 신뢰할 수 있음</h3>
            <p className="text-gray-600">
              보안 모범 사례와 신뢰할 수 있는 인프라로 구축
            </p>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="py-16 px-4 bg-white rounded-lg shadow-sm border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            AI 플랫폼 작동 방식
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            몇 가지 간단한 단계로 즉시 AI 지원을 받으세요
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              1
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">채팅 위젯 클릭</h3>
            <p className="text-gray-600">
              오른쪽 하단의 떠있는 채팅 위젯을 클릭하여 대화를 시작하세요
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              2
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI가 즉시 응답</h3>
            <p className="text-gray-600">
              우리의 AI 어시스턴트가 질문을 분석하고 지능적이고 맥락적인 응답을 제공합니다
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 text-primary-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold text-lg">
              3
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">언제든지 도움 받기</h3>
            <p className="text-gray-600">
              지능형 AI 어시스턴트와 함께 24/7 질문에 대한 답변을 받으세요
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 px-4 text-center">
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-12 text-white">
          <h2 className="text-3xl font-bold mb-4">
            AI 플랫폼을 경험할 준비가 되셨나요?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            채팅 위젯을 클릭하고 AI 어시스턴트와 대화를 시작하세요!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={openChatWidget}
              className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors duration-200"
            >
              채팅 시작하기
            </button>
            <button 
              onClick={goToPromptOptimization}
              className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-primary-600 font-medium py-3 px-8 rounded-lg transition-colors duration-200"
            >
              프롬프트 최적화
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
