// src/components/Login/Login.jsx
import React, { useState } from "react";
import { Box, Text, Input, Button, Stack } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { FiArrowRight, FiDatabase, FiExternalLink, FiGitBranch, FiMail, FiShield, FiUser } from "react-icons/fi";

export default function Login() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim() || !email.trim()) return;
    const user = { name: name.trim(), email: email.trim() };
    sessionStorage.setItem("user", JSON.stringify(user));
    navigate("/login/chat", { state: { user } });
  }

  return (
    <main className="app-shell min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <section className="mx-auto grid min-h-[calc(100vh-3rem)] w-full max-w-6xl items-center gap-8 lg:grid-cols-[1.08fr_0.92fr]">
        <div className="space-y-8">
          <div className="brand-mark">
            <img src="/sk_icon.png" alt="Sarthak Kakkar" />
            <span>Communication Assistant</span>
          </div>

          <div className="max-w-3xl space-y-5">
            <p className="eyebrow">Sarthak Kakkar</p>
            <h1 className="page-title">A focused assistant for reaching Sarthak.</h1>
            <p className="lead-text">
              Ask about Sarthak or request an email follow-up. The assistant uses a supervisor-style flow,
              layered injection security, and information retrieved through RAAS, Sarthak's separate Retrieval
              as a Service project.
            </p>
          </div>

          <div className="system-notes" aria-label="Assistant system details">
            <div className="system-note">
              <FiGitBranch aria-hidden="true" />
              <div>
                <h2>Supervisor flow</h2>
                <p>Routes each message to the right path: answer, outreach, or deny off-topic requests.</p>
              </div>
            </div>
            <div className="system-note">
              <FiDatabase aria-hidden="true" />
              <div>
                <h2>Powered by RAAS</h2>
                <p>RAAS is a separate custom RAG project that provides the information layer for this assistant.</p>
              </div>
            </div>
            <div className="system-note">
              <FiShield aria-hidden="true" />
              <div>
                <h2>Injection security</h2>
                <p>Layered checks keep the conversation scoped to Sarthak and the available data.</p>
              </div>
            </div>
          </div>

          <div className="link-row">
            <a href="https://github.com/Sarthak-Kakkar-03/RAAS" target="_blank" rel="noreferrer">
              RAAS GitHub <FiExternalLink aria-hidden="true" />
            </a>
            <a href="https://skakkar.netlify.app/" target="_blank" rel="noreferrer">
              Sarthak's website <FiExternalLink aria-hidden="true" />
            </a>
          </div>
        </div>

        <Box as="form" onSubmit={handleSubmit} className="entry-panel">
          <div className="panel-kicker">
            <FiShield aria-hidden="true" />
            <span>Identity gate</span>
          </div>
          <Text as="h2" className="panel-title">Start the session</Text>
          <Text className="panel-copy">
            Your name and email let the assistant attach any outreach request to the right person.
          </Text>

          <Stack gap="4" mt="6">
            <Box>
              <label className="field-label" htmlFor="name">Name</label>
              <div className="input-shell">
                <FiUser aria-hidden="true" />
                <Input
                  id="name"
                  placeholder="John Doe"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  variant="unstyled"
                />
              </div>
            </Box>

            <Box>
              <label className="field-label" htmlFor="email">Email</label>
              <div className="input-shell">
                <FiMail aria-hidden="true" />
                <Input
                  id="email"
                  type="email"
                  placeholder="me@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  variant="unstyled"
                />
              </div>
            </Box>

            <Button
              type="submit"
              isDisabled={!name.trim() || !email.trim()}
              className="primary-action"
            >
              Enter chat <FiArrowRight aria-hidden="true" />
            </Button>
          </Stack>
        </Box>
      </section>
    </main>
  );
}
