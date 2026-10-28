
# 🚀 FastAPI JWT LangChain AI Agent with Simply.com MCP

A full-stack AI agent application built with **FastAPI**, **Vue 3**, **Pinia**, **LangChain**, **Groq LLMs**, **JWT authentication**, and the **Model Context Protocol (MCP)**.

The backend uses LangChain's native tool-calling architecture to retrieve general information from Wikipedia and interact with Simply.com's public MCP server for documentation searches and domain availability checks.

The agent dynamically discovers MCP tools, enables only explicitly approved tools, and returns a structured response containing the final answer and intermediate tool calls.

The companion Vue 3 Single Page Application (SPA) provides an authenticated chat interface for interacting with the agent and visualizing its workflow.

**Vue Frontend:** https://github.com/persteenolsen/vue-fastapi-jwt-auth-ai-agent-five

---

## 📌 Project Information

- Version: 0.0.3
- Last Updated: 28-10-2026
- Python: 3.12
- Backend: FastAPI
- Frontend: Vue 3 and Pinia
- Authentication: JWT (HS256)
- AI Framework: LangChain
- LLM Provider: Groq
- Model: `openai/gpt-oss-20b`
- External Integration: Simply.com public MCP server
- Agent Architecture: LangChain tool-calling agent
- API: REST

## ✨ Features

### 🔐 Authentication

The backend provides JWT-based authentication for protected endpoints.

- JWT authentication using HS256
- OAuth2-compatible token endpoint
- Dedicated SPA login endpoint
- Bearer token authorization
- Environment-based secret configuration
- Protected chat endpoint

Authentication endpoints:

- `POST /login-spa` — Authenticate the Vue SPA.
- `POST /token` — Obtain an OAuth2-compatible token.

**Security note:** The application uses demo credentials. Replace these with database-backed users, secure password hashing, and production-grade identity management before deployment.

### 🤖 LangChain AI Agent

The agent uses LangChain's native structured tool-calling architecture. The LLM determines which available tools are appropriate for each request.

Key capabilities:

- Dynamic MCP tool discovery
- Explicit tool allowlisting
- Wikipedia and MCP tool integration
- Multiple tool calls per request
- Structured intermediate-step reporting
- Configurable execution limits
- Centralized error handling and logging

### 🔌 Simply.com MCP Integration

The application connects to Simply.com's public MCP server through `MultiServerMCPClient` from `langchain-mcp-adapters`.

| Setting | Value |
|---|---|
| Endpoint | `https://mcp.simply.com/public` |
| Transport | `streamable_http` |
| Client | `MultiServerMCPClient` |

The public endpoint is used without the browser-based OAuth flow associated with Simply.com's authenticated `/v2` endpoint.

#### Approved MCP tools

| Tool | Purpose |
|---|---|
| `search-docs` | Search Simply.com support documentation |
| `check-domain-availability` | Check domain availability for registration or transfer |

The backend discovers the tools exposed by the server and enables only names included in the application's allowlist.

The discovery process:

1. Connects to the public MCP endpoint.
2. Retrieves the available tools.
3. Filters them against the allowlist.
4. Logs discovered, enabled, and missing tools.
5. Passes approved tools to the LangChain agent.

The MCP client configuration uses Python's `lru_cache` to avoid repeatedly constructing the client configuration.

If an approved tool is unavailable on the public server, it is logged as missing and is not passed to the agent.

**Important:** The configured integration is intentionally limited to documentation search and domain availability checks. It does not expose domain registration, purchasing, or account modification tools. Checking availability does not register or reserve a domain.

### 🌐 Wikipedia Tool

The agent includes a custom Wikipedia retrieval tool implemented in `tools/wikipedia.py` and exposed to LangChain as a structured tool named `Wikipedia`.

It supports:

- General factual information retrieval
- Wikipedia-based research
- Integration with the agent's tool-calling workflow
- Error handling and logging

The agent prompt directs general knowledge questions to Wikipedia rather than Simply.com tools. If retrieval fails, the tool returns an error message instead of propagating the exception directly.

### 🧠 Groq LLM Integration

The application uses LangChain's `ChatGroq` integration.

| Setting | Value |
|---|---|
| Model | `openai/gpt-oss-20b` |
| Temperature | `0` |
| Streaming | Disabled |
| API key | Loaded from configuration |

The LLM interprets questions, selects tools, generates arguments, evaluates tool observations, and produces the final answer.

External facts such as domain availability must be obtained from the relevant tool rather than invented by the model.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login-spa` | Authenticate the Vue SPA |
| POST | `/token` | Obtain an OAuth2-compatible token |
| POST | `/chat` | Submit a question to the agent |
| GET | `/health` | Check service health |
| GET | `/test-groq` | Test the Groq integration |
| GET | `/test-wikipedia` | Test the Wikipedia integration |

These endpoints describe the documented application interface. Exact request and response schemas depend on the corresponding FastAPI route implementations.

## 📦 Chat Request and Response

A chat request uses a message containing the user's question.

Example request:

```json
{
  "message": "How do I configure DNS records?"
}
```

The response contains the final answer and any intermediate tool calls.

```json
{
  "response": {
    "actions": [
      {
        "action": "search-docs",
        "action_input": {
          "query": "How do I configure DNS records?"
        },
        "observation": "Retrieved Simply.com documentation..."
      }
    ],
    "final_answer": "Here is how to configure your DNS settings..."
  }
}
```

### Response fields

| Field | Description |
|---|---|
| `response` | Agent result |
| `response.actions` | List of intermediate tool calls |
| `actions[].action` | Tool name |
| `actions[].action_input` | Input supplied to the tool |
| `actions[].observation` | Tool output |
| `response.final_answer` | Final answer generated by the agent |

If no tool is required, the actions list is empty:

```json
{
  "response": {
    "actions": [],
    "final_answer": "Here is the answer to your question."
  }
}
```

The current implementation returns a generic error response if agent execution fails:

```json
{
  "response": {
    "actions": [],
    "final_answer": "The agent encountered an error. Check the server logs for details."
  }
}
```

An empty actions list can indicate either a normal response without tool use or an error. Check the final answer to distinguish the two cases.

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.12
- pip
- A Groq API key
- Network access to the Simply.com public MCP endpoint
- The companion Vue frontend, if using the graphical interface

### 1. Clone the repository

Replace the example URL with your actual backend repository URL.

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository/backend
```

Adjust the directory path to match your repository structure.

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure your dependencies include the packages used by the application, such as:

- `fastapi`
- `uvicorn`
- `langchain`
- `langchain-core`
- `langchain-groq`
- `langchain-mcp-adapters`
- Dependencies required by the Wikipedia and authentication implementations

Use the project's pinned dependency versions where available.

## 🔑 Environment Variables

Create a `.env` file in the directory from which the application loads its configuration.

```dotenv
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key
FAKE_USERNAME=admin
FAKE_PASSWORD=replace_with_a_secure_password
```

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Secret used to sign JWTs |
| `GROQ_API_KEY` | Groq API key |
| `FAKE_USERNAME` | Demo username |
| `FAKE_PASSWORD` | Demo password |

The application imports `GROQ_API_KEY` from `config.py`. Ensure that environment variables are loaded before initializing the LLM.

The MCP endpoint and approved tools are configured in the agent code:

```python
SIMPLY_MCP_URL = "https://mcp.simply.com/public"

ALLOWED_SIMPLY_TOOLS = {
    "search-docs",
    "check-domain-availability",
}
```

The supplied public MCP client configuration does not require a separate Simply.com API key.

Generate a random JWT signing secret with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Security recommendations

- Never commit `.env` files or expose secrets in frontend code.
- Add `.env` and virtual environment directories to `.gitignore`.
- Use a strong, unique JWT signing secret.
- Replace demo credentials before deployment.
- Configure CORS for trusted frontend origins only.
- Avoid logging tokens, secrets, or sensitive user information.

## ▶️ Run the Backend

Start the application from the directory containing `main.py`:

```bash
uvicorn main:app --reload
```

Development endpoints:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

The `--reload` option is intended for development and should generally be disabled in production.


## 🔐 Authentication Flow

### Vue SPA

1. The user submits credentials through the login interface.
2. The frontend sends them to `POST /login-spa`.
3. The backend validates the credentials and returns a JWT.
4. The frontend stores the token according to its authentication implementation.
5. Subsequent protected requests include:

   ```http
   Authorization: Bearer <token>
   ```

6. The authenticated user submits questions to `POST /chat`.

### Swagger UI

1. Open http://127.0.0.1:8000/docs.
2. Use `/token` to obtain a token.
3. Click **Authorize** in Swagger UI.
4. Enter the credentials or token details required by the configured OAuth2 flow.
5. Call the protected endpoints.

Exact authentication fields depend on the FastAPI security dependencies.

---

## 🧠 Agent Workflow

The application combines the Vue frontend, FastAPI, LangChain, Groq, Wikipedia, and Simply.com's public MCP server.

```text
User Question
     |
     v
Vue 3 Frontend
     |
     v
FastAPI + JWT Authentication
     |
     v
LangChain Agent <----> Groq LLM
     |
     +----> Wikipedia
     |
     +----> Simply.com MCP
                  |
                  +----> search-docs
                  |
                  +----> check-domain-availability
     |
     v
Tool Observations
     |
     v
Final Answer + Intermediate Steps
     |
     v
Structured API Response
     |
     v
Vue Frontend
```

The LLM determines whether external tools are needed. Not every request invokes a tool.

## 🏗️ Architecture

### Backend

FastAPI handles authentication, REST endpoints, agent execution, MCP integration, Wikipedia retrieval, intermediate-step collection, error handling, and logging.

### Frontend

The companion Vue 3 SPA handles login, authentication state, JWT usage, API requests, Pinia state management, chat interactions, and visualization of tool calls and observations.

### AI agent

LangChain orchestrates tool selection and execution. Groq generates responses, while Wikipedia and Simply.com MCP provide external information.

### External services

| Service | Responsibility |
|---|---|
| Groq | LLM inference and tool selection |
| Wikipedia | General factual information |
| Simply.com public MCP | Documentation search and domain availability |

## 💬 Example Use Cases

The following examples illustrate intended behavior. Actual responses depend on model output and external tool results.

### 1. General question

**Request:**

```json
{
  "message": "Tell me a joke"
}
```

The agent can answer directly without invoking a tool.

### 2. Wikipedia lookup

**Request:**

```json
{
  "message": "Who is the CEO of Apple?"
}
```

The agent can use Wikipedia to retrieve relevant information before generating its answer. The result should reflect the information actually retrieved, which may change over time.

### 3. Simply.com documentation

**Request:**

```json
{
  "message": "How do I configure DNS records for my domain at Simply.com?"
}
```

Expected workflow:

1. The agent identifies a Simply.com support question.
2. It can invoke `search-docs`.
3. The MCP server returns relevant documentation.
4. The agent summarizes the retrieved information.
5. The API returns the answer and intermediate tool observations.

### 4. Domain availability

**Request:**

```json
{
  "message": "Is example-domain.dk available for registration?"
}
```

Expected workflow:

1. The agent identifies a domain availability request.
2. It can invoke `check-domain-availability`.
3. The MCP server checks the requested domain.
4. The agent communicates the actual result.

Availability must be verified by the tool. Results can change, and a positive result does not reserve the domain.

---

## 🖥️ Vue Frontend

The companion Vue 3 application provides the graphical interface.

Repository: https://github.com/persteenolsen/vue-fastapi-jwt-auth-ai-agent-five

Capabilities include:

- Vue 3 Single Page Application
- JWT authentication
- Pinia state management
- AI chat interface
- FastAPI integration
- Final-answer display
- Tool-call, input, and observation visualization

The frontend and backend must agree on the chat request and response schemas. The agent returns `response.actions` as a list and `response.final_answer` as a string.

## ⚙️ Agent Configuration

| Setting | Value | Purpose |
|---|---|---|
| LLM | `openai/gpt-oss-20b` | Tool selection and response generation |
| Temperature | `0` | More deterministic generation |
| MCP transport | `streamable_http` | MCP communication |
| MCP endpoint | `https://mcp.simply.com/public` | Public Simply.com server |
| Approved MCP tools | `search-docs`, `check-domain-availability` | Restricts available tools |
| Maximum iterations | `4` | Limits agent iterations |
| Maximum execution time | `30` seconds | Configures executor time limit |
| Intermediate steps | Enabled | Collects tool calls and observations |
| Verbose output | Disabled | Disables verbose executor output |
| Parsing error handling | Enabled | Configures parsing error handling |
| Streaming | Disabled | Returns responses after execution |

Actual request duration can also depend on network latency and external services.


## 🚧 Current Limitations

- Only two Simply.com MCP tools are explicitly allowlisted.
- Tool availability depends on the public MCP server.
- The public MCP configuration does not provide authenticated access to private customer resources.
- Domain availability checks do not register or reserve domains.
- Domain purchasing and account modification tools are not exposed.
- Wikipedia is the only configured general knowledge tool.
- Conversation memory and persistent chat history are not implemented in the supplied agent code.
- Streaming responses are disabled.
- Authentication uses demo credentials.
- The application uses a single LangChain agent.
- External service outages can affect requests.
- Intermediate tool observations are returned to clients and should be reviewed before production use.
- Dedicated rate limiting, persistent conversation storage, and production observability are not configured in the supplied agent code.

## 🚀 Future Improvements

Potential enhancements include:

- Conversation memory and persistent chat history
- Streaming responses using server-sent events
- Additional MCP servers and approved tools
- Configurable MCP endpoints
- Production-grade authentication and user management
- Database-backed users and conversations
- Rate limiting and abuse prevention
- Structured error responses and request validation
- Improved retry policies and external-service timeouts
- Monitoring, tracing, and observability
- Automated tests for discovery and execution
- Tool-result sanitization and size limits
- Per-user authorization and usage tracking
- Docker deployment and CI/CD
- Improved frontend visualization of multiple tool calls

Review additional MCP tools before adding them to the allowlist.

## 🔒 Security Considerations

Before deploying to production:

- Replace demo authentication with a secure identity system.
- Hash passwords using an appropriate password-hashing algorithm.
- Protect JWT signing secrets and rotate them when necessary.
- Validate and constrain incoming requests.
- Restrict CORS to trusted frontend origins.
- Apply rate limiting to authentication and chat endpoints.
- Treat external tool results as untrusted input.
- Keep the MCP tool allowlist restrictive.
- Review new tools before exposing them to the agent.
- Limit tool input and observation sizes.
- Avoid returning sensitive internal errors.
- Review which intermediate observations should be exposed to users.
- Apply suitable network, logging, and monitoring controls.
- Verify external-service results before relying on them.

The agent prompt instructs the model to treat tool output as untrusted data. This provides useful defense-in-depth, but prompts are not a security boundary. Enforce validation and access restrictions in application code.

## 💡 Design Philosophy

> Use structured tool-calling workflows and explicit tool permissions instead of fragile prompt parsing and unrestricted external actions.

The project emphasizes:

- **Reliability:** Structured LangChain tool calling.
- **Transparency:** Tool calls, inputs, observations, and final answers.
- **Modularity:** Separate orchestration from integrations.
- **Controlled access:** Explicit MCP tool allowlisting.
- **Extensibility:** Add capabilities through tools and MCP servers.
- **Separation of concerns:** Distinct frontend, API, agent, and external services.
- **Security awareness:** Treat external results as untrusted and constrain available capabilities.

## 🙌 Final Notes

This project demonstrates how FastAPI, Vue 3, JWT authentication, LangChain, Groq, Wikipedia, and MCP can be combined into an extensible AI agent application.

The backend exposes an authenticated REST API, while the Vue SPA provides an interactive chat interface. The agent combines general factual retrieval with selected Simply.com capabilities for documentation search and domain availability checks.

Dynamic MCP discovery adapts to the tools exposed by the external server, while explicit allowlisting limits which tools the agent can invoke.

The result is a modular starting point for building AI applications with controlled and observable tool execution.

## 📄 License

MIT License
