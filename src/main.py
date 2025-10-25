from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os
from typing import Optional

from models import OptimizeRequest, OptimizeResponse, HealthResponse, ErrorResponse
from timezone_optimizer import TimezoneOptimizer
from auth import auth_manager

# Initialize FastAPI app
app = FastAPI(
    title="TimeZone Optimizer API",
    description="Find optimal meeting times across timezones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize optimizer
optimizer = TimezoneOptimizer()

# Track startup time for uptime calculation
start_time = time.time()


def get_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency to extract and validate API key"""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Include 'X-API-Key' header."
        )
    
    if not auth_manager.validate_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return x_api_key


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    return HealthResponse(status="ok", uptime=uptime)


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_meeting_time(
    request: OptimizeRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Find optimal meeting time for participants across timezones.
    
    - **participants**: List of meeting participants with names and locations
    - **duration_minutes**: Meeting duration (15-480 minutes)
    - **num_alternatives**: Number of alternative times to return (1-10)
    """
    try:
        # Check rate limit
        if not auth_manager.check_rate_limit(api_key):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Free tier allows 100 requests per day."
            )
        
        # Log usage
        auth_manager.log_usage(api_key, "/optimize")
        
        # Convert request to optimizer format
        participants = [
            {"name": p.name, "location": p.location}
            for p in request.participants
        ]
        
        # Find optimal meeting time
        result = optimizer.find_optimal_meeting_time(
            participants=participants,
            duration_minutes=request.duration_minutes,
            num_alternatives=request.num_alternatives
        )
        
        return OptimizeResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error optimizing meeting time: {str(e)}"
        )


@app.get("/usage")
async def get_usage_stats(api_key: str = Depends(get_api_key)):
    """Get usage statistics for the API key"""
    # This would typically return usage stats
    return {"message": "Usage stats endpoint - implement as needed"}


@app.post("/create-key")
async def create_api_key(user_id: str):
    """Create a new API key (for testing purposes)"""
    try:
        new_key = auth_manager.create_api_key(user_id)
        return {"api_key": new_key, "message": "API key created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating API key: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for consistent error responses"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
