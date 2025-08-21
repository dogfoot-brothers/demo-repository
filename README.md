# AutoPromptix Demo Repository

This repository demonstrates how to integrate and utilize the AutoPromptix platform for AI-powered prompt optimization.

## 🚀 Key Features

- **AI-Powered Prompt Optimization**: Automatically optimize prompts using AutoPromptix
- **Smart Mutation Generation**: Generate tailored prompt variations based on user input
- **Real-time Evaluation**: Measure prompt quality using various metrics
- **Custom Requirements**: Fine-tune prompts with additional requirements
- **Keyword Exclusion**: Ensure unwanted content is excluded

## 🏗️ Project Structure

```
demo-repository/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server
│   ├── autopromptix_efficient.py  # Prompt optimization engine
│   ├── scorer_simple.py    # Scoring system
│   └── llm.py              # LLM integration service
├── frontend/               # React frontend
│   └── src/
│       └── pages/
│           └── PromptOptimizationPage.jsx  # Main UI
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **AutoPromptix**: Integrated for prompt optimization
- **OpenAI API**: GPT model integration
- **rapidfuzz**: Text similarity calculation
- **rouge-score**: ROUGE metric calculation

### Frontend
- **React**: User interface
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Lucide React**: Icons

## 📦 Installation and Execution

### 1. Backend Setup

```bash
pip install -r requirements.txt
```

Set environment variables:
```bash
# Create .env file
OPENAI_API_KEY=your_api_key_here
```

### 2. Backend Execution

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Frontend Execution

```bash
npm run dev
```

## 🔧 Usage

1. **User Input**: Enter the prompt you want to optimize
2. **Expected Output**: Describe the desired output format and content
3. **Product Name**: Enter the related product/service name
4. **Exclude Keywords**: Enter keywords to exclude
5. **Additional Requirements**: Enter specific writing style or requirements
6. **Start Optimization**: AI automatically optimizes the prompt

## 📊 Optimization Process

1. **Input Analysis**: AI analyzes the request to determine the best approach
2. **Smart Mutation Generation**: Generates tailored prompt variations based on analysis
3. **Evaluation**: Executes each variation with LLM and calculates scores
4. **Best Result Selection**: Selects the highest-scoring prompt
5. **Result Output**: Provides the optimized prompt and generated output

## 🎯 Evaluation Metrics

- **Cosine Similarity**: Semantic similarity between texts
- **ROUGE-L**: Longest sequence matching accuracy
- **Keyword Coverage**: Inclusion of essential keywords
- **Structural Quality**: Document structure and readability
- **Exclusion Penalty**: Deduction for forbidden keywords

## 🔒 Environment Variables

| Variable Name | Description | Required |
|---------------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | ✅ Required |

## 📝 License

This project is licensed under the Apache 2.0 License.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

For inquiries about the project, please create an issue.
