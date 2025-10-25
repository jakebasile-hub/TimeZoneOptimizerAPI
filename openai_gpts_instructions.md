# TimeZone Optimizer GPT Configuration

## Overview
This configuration file is designed for creating an OpenAI GPT that integrates with your TimeZone Optimizer API.

## How to Use

### 1. Create a New GPT
1. Go to ChatGPT and click "Create a GPT"
2. Use the configuration from `openai_gpts_config.json`

### 2. Key Features
- **Smart Timezone Optimization**: Finds optimal meeting times across timezones
- **Global Coverage**: Supports 100+ locations worldwide
- **Business Hours Optimization**: Minimizes sleep-hour conflicts
- **Alternative Suggestions**: Multiple meeting time options with fairness scores

### 3. API Integration
The GPT will call your TimeZone Optimizer API endpoints:
- `POST /optimize` - Main optimization endpoint
- `GET /health` - Health check
- `POST /create-key` - Create API keys
- `GET /usage` - Usage statistics

### 4. Example Use Cases
- "Help me schedule a meeting between Alice in New York and Bob in Tokyo"
- "Find the best time for a gaming session with players in London, Sydney, and Los Angeles"
- "Plan a video call between team members in Paris, Mumbai, and São Paulo"

### 5. Supported Locations
- **North America**: New York, Los Angeles, Chicago, Toronto, Vancouver
- **Europe**: London, Paris, Berlin, Madrid, Amsterdam, Zurich
- **Asia**: Tokyo, Beijing, Mumbai, Singapore, Hong Kong, Seoul
- **Australia**: Sydney, Melbourne, Perth, Auckland
- **South America**: São Paulo, Buenos Aires, Lima, Bogotá
- **Africa**: Cairo, Johannesburg, Lagos, Nairobi

### 6. Configuration Notes
- Set the API base URL to your Render deployment URL
- Include API key authentication in requests
- Handle rate limiting (100 requests/day for free tier)
- Provide clear, actionable meeting time recommendations

## Benefits
- **One-step solution** for global meeting scheduling
- **Eliminates manual timezone calculations**
- **Perfect for business, gaming, family, and international calls**
- **Production-ready API** deployed on Render
