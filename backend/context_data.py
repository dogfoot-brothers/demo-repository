"""
Predefined context data for the customer support LLM
This contains information about products, services, policies, and common issues
"""

PRODUCT_CATALOG = {
    "products": [
        {
            "name": "AutoPromtix AI Assistant",
            "category": "AI Software",
            "price": "$299/month",
            "description": "Advanced AI-powered virtual assistant for business automation and customer support",
            "features": [
                "Natural Language Processing",
                "Multi-platform Integration",
                "Custom Workflow Automation",
                "Real-time Analytics",
                "24/7 Availability",
                "Multi-language Support",
                "API Integration"
            ],
            "warranty": "30-day money-back guarantee",
            "availability": "Available"
        },
        {
            "name": "AutoPromtix Workflow Engine",
            "category": "Automation",
            "price": "$199/month",
            "description": "Powerful workflow automation platform for business process optimization",
            "features": [
                "Drag-and-drop Interface",
                "Conditional Logic",
                "Integration Connectors",
                "Performance Monitoring",
                "Custom Templates",
                "Team Collaboration",
                "Scalable Architecture"
            ],
            "warranty": "30-day money-back guarantee",
            "availability": "Available"
        },
        {
            "name": "AutoPromtix Analytics Suite",
            "category": "Analytics",
            "price": "$149/month",
            "description": "Comprehensive analytics and reporting platform for business intelligence",
            "features": [
                "Real-time Dashboards",
                "Custom Reports",
                "Data Visualization",
                "Predictive Analytics",
                "Export Capabilities",
                "Mobile Access",
                "API Access"
            ],
            "warranty": "30-day money-back guarantee",
            "availability": "Available"
        }
    ]
}

SERVICE_POLICIES = {
    "return_policy": {
        "timeframe": "30 days",
        "conditions": [
            "Service must be in original condition",
            "No usage beyond trial period",
            "Valid subscription required",
            "No refunds for custom development"
        ],
        "exceptions": [
            "Enterprise contracts (non-refundable)",
            "Custom integrations",
            "Training services"
        ]
    },
    "warranty_policy": {
        "standard_warranty": "30-day money-back guarantee for all services",
        "extended_support": "Available for enterprise customers",
        "coverage": [
            "Service availability",
            "Technical support",
            "Bug fixes and updates"
        ],
        "exclusions": [
            "Third-party integrations",
            "Custom modifications",
            "Data migration services"
        ]
    },
    "support_policy": {
        "standard_support": "Email and chat support during business hours",
        "priority_support": "24/7 phone and email support for enterprise customers",
        "response_time": "Within 4 hours for critical issues, 24 hours for standard issues"
    }
}

COMMON_ISSUES = {
    "technical_support": {
        "login_issues": {
            "steps": [
                "Clear browser cache and cookies",
                "Try incognito/private browsing mode",
                "Check internet connection",
                "Contact support if issues persist"
            ],
            "contact": "support@autopromtix.com"
        },
        "integration_setup": {
            "steps": [
                "Review integration documentation",
                "Verify API credentials",
                "Test connection in sandbox mode",
                "Contact technical support for assistance"
            ],
            "troubleshooting": [
                "Check API key permissions",
                "Verify endpoint URLs",
                "Review error logs",
                "Contact support if issues persist"
            ]
        },
        "performance_issues": {
            "slow_loading": [
                "Check internet connection speed",
                "Clear browser cache",
                "Try different browser",
                "Contact support for optimization"
            ],
            "data_sync_issues": [
                "Check integration status",
                "Verify data source connectivity",
                "Review sync schedules",
                "Contact technical support"
            ]
        }
    }
}

COMPANY_INFO = {
    "name": "Autopromtix",
    "founded": "2020",
    "headquarters": "San Francisco, CA",
    "mission": "To revolutionize business operations through intelligent AI-powered automation and analytics solutions",
    "contact": {
        "phone": "1-800-AUTO-PRO",
        "email": "support@autopromtix.com",
        "hours": "Monday-Friday 9AM-6PM PST",
        "emergency": "24/7 for enterprise customers"
    },
    "social_media": {
        "twitter": "@autopromtix",
        "facebook": "Autopromtix",
        "linkedin": "Autopromtix"
    }
}

FAQ_DATA = {
    "general": [
        {
            "question": "What is Autopromtix?",
            "answer": "Autopromtix is a leading technology company specializing in AI-powered automation solutions, analytics, and business intelligence tools. We help businesses streamline operations and improve efficiency through intelligent automation."
        },
        {
            "question": "How do I get started with Autopromtix services?",
            "answer": "You can start with our 30-day free trial. Simply visit our website, choose the service you're interested in, and sign up. Our team will guide you through the setup process and provide training if needed."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and wire transfers for enterprise customers. We also offer annual billing with discounts."
        }
    ],
    "technical": [
        {
            "question": "How do I integrate Autopromtix with my existing systems?",
            "answer": "Autopromtix offers extensive API documentation and pre-built connectors for popular platforms. Our technical team can assist with custom integrations and provide implementation support."
        },
        {
            "question": "Is my data secure with Autopromtix?",
            "answer": "Yes, we take data security seriously. We use enterprise-grade encryption, comply with industry standards, and offer on-premise solutions for customers with strict security requirements."
        }
    ]
}

def get_context_for_query(query: str) -> str:
    """
    Return relevant context based on the user's query
    """
    query_lower = query.lower()
    context_parts = []
    
    # Add company info
    context_parts.append(f"Company: {COMPANY_INFO['name']}")
    context_parts.append(f"Contact: {COMPANY_INFO['contact']['phone']} or {COMPANY_INFO['contact']['email']}")
    
    # Check for product-related queries
    if any(word in query_lower for word in ['product', 'service', 'ai', 'automation', 'analytics']):
        context_parts.append("Available Products:")
        for product in PRODUCT_CATALOG['products']:
            context_parts.append(f"- {product['name']}: {product['description']} (${product['price']})")
    
    # Check for policy-related queries
    if any(word in query_lower for word in ['return', 'refund', 'warranty', 'policy', 'support']):
        context_parts.append("Return Policy: " + str(SERVICE_POLICIES['return_policy']['timeframe']))
        context_parts.append("Warranty: " + str(SERVICE_POLICIES['warranty_policy']['standard_warranty']))
        context_parts.append("Support: " + str(SERVICE_POLICIES['support_policy']['standard_support']))
    
    # Check for technical support queries
    if any(word in query_lower for word in ['help', 'support', 'issue', 'problem', 'broken', 'not working']):
        context_parts.append("Technical Support: Available at " + COMPANY_INFO['contact']['phone'])
        context_parts.append("Support Hours: " + COMPANY_INFO['contact']['hours'])
    
    # Check for integration queries
    if any(word in query_lower for word in ['integration', 'api', 'connect', 'setup']):
        context_parts.append("Integration Support: Available through our technical team")
        context_parts.append("API Documentation: Available in our developer portal")
    
    return "\n".join(context_parts)
