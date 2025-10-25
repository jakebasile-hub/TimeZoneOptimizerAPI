# RapidAPI Listing for TimeZone Optimizer API

## API Information
- **Name**: TimeZone Optimizer
- **Description**: Find optimal meeting times across timezones for global teams, gaming sessions, and video calls
- **Category**: Productivity, Business, Utilities
- **Pricing**: Free tier (100 requests/day), Paid plans available

## API Endpoints

### 1. POST /optimize
**Find optimal meeting time for participants across timezones**

**Request Body:**
```json
{
  "participants": [
    {"name": "Alice", "location": "New York, USA"},
    {"name": "Bob", "location": "London, UK"},
    {"name": "Cara", "location": "Tokyo, Japan"}
  ],
  "duration_minutes": 60,
  "num_alternatives": 3
}
```

**Response:**
```json
{
  "best_meeting_time_utc": "2025-01-25T14:00:00Z",
  "local_times": [
    {"name": "Alice", "local_time": "2025-01-25T10:00:00-04:00"},
    {"name": "Bob", "local_time": "2025-01-25T15:00:00+01:00"},
    {"name": "Cara", "local_time": "2025-01-25T23:00:00+09:00"}
  ],
  "alternatives": [
    {"utc_time": "2025-01-25T13:00:00Z", "fairness_score": 0.88},
    {"utc_time": "2025-01-25T15:00:00Z", "fairness_score": 0.85}
  ]
}
```

### 2. GET /health
**Health check endpoint**

**Response:**
```json
{
  "status": "ok",
  "uptime": 123.45
}
```

### 3. POST /create-key
**Create a new API key for testing**

**Request:**
```
user_id=test_user
```

**Response:**
```json
{
  "api_key": "tz_opt_abc123def456",
  "message": "API key created successfully"
}
```

### 4. GET /usage
**Get usage statistics for the API key**

**Headers:**
```
X-API-Key: your-api-key-here
```

**Response:**
```json
{
  "message": "Usage stats endpoint - implement as needed"
}
```

## Authentication
- **Type**: API Key
- **Header**: `X-API-Key`
- **Rate Limit**: 100 requests/day (free tier)

## Supported Locations
- **North America**: New York, Los Angeles, Chicago, Toronto, Vancouver
- **Europe**: London, Paris, Berlin, Madrid, Amsterdam, Zurich
- **Asia**: Tokyo, Beijing, Mumbai, Singapore, Hong Kong, Seoul
- **Australia**: Sydney, Melbourne, Perth, Auckland
- **South America**: São Paulo, Buenos Aires, Lima, Bogotá
- **Africa**: Cairo, Johannesburg, Lagos, Nairobi

## Use Cases
- Business meetings across timezones
- Online gaming sessions
- Video conferences with global participants
- Family reunions across countries
- Phone calls with friends overseas

## Pricing Plans
- **Free**: 100 requests/day
- **Pro**: Custom limits and features
- **Enterprise**: Unlimited usage and priority support

## API Documentation
- **Base URL**: Your Render deployment URL
- **Content-Type**: application/json
- **CORS**: Enabled for web applications
