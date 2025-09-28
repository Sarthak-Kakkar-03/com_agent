// src/components/Login/Login.jsx
import React, { useState } from "react";
import { Box, Text, Input, Button, Stack } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [name, setName]   = useState("");
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
    <div className="min-h-screen flex items-center justify-center px-4">
      <Box
        as="form"
        onSubmit={handleSubmit}
        w="100%"
        maxW="420px"
        p="6"
        borderWidth="1px"
        borderRadius="md"
      >
        <Text fontSize="lg" fontWeight="semibold">Welcome</Text>
        <Text fontSize="sm" color="gray.600" mb="4">
          Please enter your name and email to continue.
        </Text>

        <Stack spacing="3">
          <Box>
            <Text mb="1">Name</Text>
            <Input
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </Box>

          <Box>
            <Text mb="1">Email</Text>
            <Input
              type="email"
              placeholder="me@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </Box>

          <Button
            type="submit"
            isDisabled={!name.trim() || !email.trim()}
            className="border-2 !border-white hover:!border-blue-500 transition-colors"
          >
            Submit
          </Button>
        </Stack>
      </Box>
    </div>
  );
}
