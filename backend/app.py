from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal, Dict, Any
from agent_graph import build_graph, settings

NextStep = Literal["MAIL","INFO","MESSAGE","supervisor"]

class ConversationState(BaseModel):
    name: str
    email: str
    visible_messages: List[str] = Field(default_factory=list)
    summary: str = ""
    latest_info: str = "No info collected yet"
    next: NextStep = "supervisor"
    events: List[Dict[str, Any]] = Field(default_factory=list)
    pending_tools: List[Dict[str, Any]] = Field(default_factory=list)
    last_mail_ai_text: str = ""
    supervisor_instruction: str = ""
    intermediate_note: str = ""

class StepInput(BaseModel):
    state: ConversationState
    user_text: Optional[str] = ""

class StepOutput(BaseModel):
    state: ConversationState
    display_message: str
    next: NextStep

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
GRAPH = build_graph()

@app.post("/chat", response_model=StepOutput)
def step(request: StepInput):
    st: Dict[str, Any] = request.state.dict() 
    if request.user_text:
        st.setdefault("visible_messages", []).append(request.user_text)
    result: Dict[str, Any] = GRAPH.invoke(st)
    vm = result.get("visible_messages", [])
    display = vm[-1] if vm else ""
    return StepOutput(
        state=ConversationState.parse_obj(result),
        display_message=display,
        next=result.get("next","supervisor"),
    )
    
@app.get("/debug/env")
def debug_env():
    return {
        "DEEPSEEK_API_KEY": bool(settings.DEEPSEEK_API_KEY),
        "LANGCHAIN_API_KEY": bool(settings.LANGCHAIN_API_KEY),
        "BOT_MAIL_ID": settings.BOT_MAIL_ID,
        "BOT_MAIL_PASSWORD": "*****" if settings.BOT_MAIL_PASSWORD else None,
    }
    
@app.get("/health")
def health():
    return {"ok": True}


