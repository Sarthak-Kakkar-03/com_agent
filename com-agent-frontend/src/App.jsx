import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Login/Login.jsx";

function Chat() {
  return <div>Chat</div>; // your real component here
}

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/login/:id" element={<Chat />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
