export const STATE_KEY = "conv_state";
export const saveState = (s) => sessionStorage.setItem(STATE_KEY, JSON.stringify(s));
export const loadState = () => {
  try { return JSON.parse(sessionStorage.getItem(STATE_KEY) || "null"); } catch { return null; }
};
export const clearState = () => sessionStorage.removeItem(STATE_KEY);
