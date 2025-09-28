import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { Provider } from "@/components/ui/provider";
import "./index.css"

createRoot(document.getElementById("root")).render(
  <Provider>
    <App />
  </Provider>
);
