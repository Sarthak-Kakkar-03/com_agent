// src/components/Chat/Chat.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, Button, HStack, Input, Stack, Text } from "@chakra-ui/react";
import { FiArrowUpRight, FiDatabase, FiExternalLink, FiMail, FiMessageCircle, FiSend, FiSlash, FiUserCheck } from "react-icons/fi";

const API_BASE = import.meta.env?.VITE_API_URL ?? "/api";

function loadJSON(key) {
  try { return JSON.parse(sessionStorage.getItem(key) || "null"); }
  catch { return null; }
}
function saveJSON(key, val) {
  try { sessionStorage.setItem(key, JSON.stringify(val)); } catch { return; }
}

export default function Chat() {
  const navigate = useNavigate();
  const location = useLocation();
  const navUser = location.state?.user || null;

  const [conv, setConv] = useState(() => {
    const saved = loadJSON("conv_state");
    if (saved) return saved;
    const user = loadJSON("user") || navUser;
    if (user?.name && user?.email) return { name: user.name, email: user.email };
    return null;
  });
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    if (!conv?.name || !conv?.email) navigate("/login", { replace: true });
  }, [conv, navigate]);

  useEffect(() => {
    if (conv) saveJSON("conv_state", conv);
  }, [conv]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  });

  const messages = useMemo(() => (conv?.visible_messages ?? []), [conv]);

  async function send(e) {
    e.preventDefault();
    if (!msg.trim() || !conv || busy) return;
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: conv, user_text: msg.trim() }),
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      setConv(data.state);
      setMsg("");
    } catch (err) {
      console.error(err);
      alert("Failed to send message. Check backend URL or CORS.");
    } finally {
      setBusy(false);
    }
  }

  if (!conv) return null;

  return (
    <main className="app-shell min-h-screen px-4 py-5 sm:px-6 lg:px-8">
      <section className="chat-layout mx-auto grid min-h-[calc(100vh-2.5rem)] w-full max-w-7xl gap-5 lg:grid-cols-[320px_minmax(0,1fr)]">
        <aside className="chat-sidebar">
          <div className="brand-mark compact">
            <img src="/sk_icon.png" alt="Sarthak Kakkar" />
            <span>Communication Assistant</span>
          </div>

          <div className="identity-card">
            <div className="avatar">{conv.name?.charAt(0)?.toUpperCase() || "U"}</div>
            <div>
              <p className="identity-label">Chatting as</p>
              <h1>{conv.name}</h1>
              <p>{conv.email}</p>
            </div>
          </div>

          <div className="sidebar-section">
            <p className="sidebar-heading">What this bot can do</p>
            <div className="expectation-list">
              <div><FiMail aria-hidden="true" /><span>Send Sarthak an email to reach out to you if you ask me.</span></div>
              <div><FiDatabase aria-hidden="true" /><span>Tell you available data about Sarthak.</span></div>
              <div><FiSlash aria-hidden="true" /><span>Deny any requests that are not about him.</span></div>
            </div>
          </div>

          <div className="resource-links">
            <a href="https://github.com/Sarthak-Kakkar-03/RAAS" target="_blank" rel="noreferrer">
              RAAS information layer <FiExternalLink aria-hidden="true" />
            </a>
            <a href="https://skakkar.netlify.app/" target="_blank" rel="noreferrer">
              Website <FiExternalLink aria-hidden="true" />
            </a>
          </div>

          <div className="prompt-card">
            <p>Good opening prompts</p>
            <button
              type="button"
              disabled={busy}
              onClick={() => {
                if (busy) return;
                setMsg("What available data do you have about Sarthak?");
              }}
            >
              Available data <FiArrowUpRight aria-hidden="true" />
            </button>
            <button
              type="button"
              disabled={busy}
              onClick={() => {
                if (busy) return;
                setMsg("Please ask Sarthak to reach out to me by email.");
              }}
            >
              Email Sarthak <FiArrowUpRight aria-hidden="true" />
            </button>
          </div>
        </aside>

        <Box className="chat-panel">
          <header className="chat-header">
            <div>
              <div className="panel-kicker">
                <FiMessageCircle aria-hidden="true" />
                <span>Live assistant</span>
              </div>
              <Text as="h2" className="chat-title">Ask, qualify, or request follow-up</Text>
            </div>
            <div className="status-pill">
              <FiUserCheck aria-hidden="true" />
              Ready
            </div>
          </header>

          <Stack gap="0" className="conversation-shell">
            <Box className="message-stream">
              {messages.length === 0 ? (
                <div className="empty-state">
                  <FiMessageCircle aria-hidden="true" />
                  <h3>Start with what you need from Sarthak.</h3>
                  <p>
                    Ask about available data on Sarthak, or ask the assistant to email him so he can reach out.
                  </p>
                </div>
              ) : (
                messages.map((m, i) => {
                  const str = typeof m === "string" ? m : String(m ?? "");
                  const isBot = str.startsWith("Bot_Message");
                  const text = isBot ? str.replace(/^Bot_Message[:\-\s]?\s*/, "") : str;
                  return (
                    <HStack key={i} w="100%" justify={isBot ? "flex-start" : "flex-end"} className="message-row">
                      <Box className={isBot ? "message-bubble bot" : "message-bubble user"}>
                        <span>{isBot ? "Assistant" : "You"}</span>
                        <Text whiteSpace="pre-wrap">{text}</Text>
                      </Box>
                    </HStack>
                  );
                })
              )}
              {busy && (
                <HStack w="100%" justify="flex-start" className="message-row">
                  <Box className="message-bubble bot typing">
                    <span>Assistant</span>
                    <Text>Thinking through the best next step...</Text>
                  </Box>
                </HStack>
              )}
              <div ref={endRef} />
            </Box>

            <form onSubmit={send} className="composer">
              <Input
                placeholder="Ask about Sarthak or request that he contact you..."
                value={msg}
                onChange={(e) => setMsg(e.target.value)}
                disabled={busy}
                variant="unstyled"
                className={busy ? "animate-textFlash" : ""}
              />
              <Button type="submit" isLoading={busy} isDisabled={!msg.trim()} className="send-button">
                <FiSend aria-hidden="true" />
                Send
              </Button>
            </form>
          </Stack>
        </Box>
      </section>
    </main>
  );
}
