from fastapi import FastAPI
from routes import router
from config import logger

# 22-07-2026 - For allowing a Vue frontend in another domain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI with JWT Authentication and a LangChain AI Agent for Simply.com Public MCP",
    description="28-10-2026 - FastAPI with JWT authentication and a Groq-powered LangChain agent using Simply.com's public MCP tools and Wikipedia for domain checks, documentation search, and factual answers",
    version="0.0.3", 
    contact={
        "name": "Per Olsen",
        "url": "https://persteenolsen.netlify.app",
    },
)


# 22-07-2026 - For allowing a Vue frontend in another domain
# Set up CORS middleware
origins = [

    # Not sure if this is needed, but adding just in case
    "https://fastapi-jwt-auth-ai-agent-five.vercel.app",

    # The domain name of the Vue 3 SPA Client
    "https://vue.fastapi.jwt.auth.ai.agent.five.persteenolsen.com",
     
    # Allow my local Vue SPA
    "http://localhost:3000"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include API routes
app.include_router(router)