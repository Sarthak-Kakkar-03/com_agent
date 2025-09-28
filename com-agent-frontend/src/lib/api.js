const API = import.meta.env.VITE_API_URL ?? "/api";
export async function stepChat(state, user_text = "") {
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state, user_text }),
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}