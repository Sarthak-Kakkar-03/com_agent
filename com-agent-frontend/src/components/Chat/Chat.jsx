// src/components/Chat/Chat.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, Button, HStack, Input, Stack, Text } from "@chakra-ui/react";

const API_BASE = import.meta.env?.VITE_API_URL ?? "/api";

function loadJSON(key) {
  try { return JSON.parse(sessionStorage.getItem(key) || "null"); }
  catch { return null; }
}
function saveJSON(key, val) {
  try { sessionStorage.setItem(key, JSON.stringify(val)); } catch {}
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
    <div className="min-h-screen grid place-items-center px-4">
      <Box w="100%" maxW="720px" p="6" borderWidth="1px" borderRadius="md">
        <Stack spacing="3" mb="4">
          <Text fontWeight="semibold">
            Chatting as {conv.name} ({conv.email})
          </Text>
          <Box borderWidth="1px" borderRadius="md" p="3" maxH="50vh" overflowY="auto">
            {messages.length === 0 ? (
              <Text color="white" fontSize="sm">Hi! I’m Sarthak Kakkar’s Communication Assistant. Ask about him or request that he contact you.</Text>
            ) : (
              messages.map((m, i) => {
                const str = typeof m === "string" ? m : String(m ?? "");
                const isBot = str.startsWith("Bot_Message");
                const text = isBot ? str.replace(/^Bot_Message[:\-\s]?\s*/, "") : str;
                return (
                  <HStack key={i} w="100%" justify={isBot ? "flex-start" : "flex-end"} my="2">
                    <Box
                      px="3"
                      py="2"
                      maxW="80%"
                      borderRadius="lg"
                      boxShadow="sm"
                      bg={isBot ? "gray.100" : "blue.500"}
                      color={isBot ? "black" : "white"}
                    >
                      <Text whiteSpace="pre-wrap">{text}</Text>
                    </Box>
                  </HStack>
                );
              })
            )}
            <div ref={endRef} />
          </Box>
        </Stack>

        <form onSubmit={send}>
          <HStack>
            <Input
              placeholder="Type a message…"
              value={msg}
              onChange={(e) => setMsg(e.target.value)}
              disabled={busy}
              p={2}
            />
            <Button type="submit" colorScheme="blue" isLoading={busy}>
              Send
            </Button>
          </HStack>
        </form>
      </Box>
    </div>
  );
}
