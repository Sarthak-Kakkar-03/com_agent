// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login/Login.jsx";
import Chat from "./components/Chat/Chat.jsx";

export default function App() {
  return (
    <div className="min-h-screen">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/login/chat" element={<Chat />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
