// src/components/Login/Login.jsx
import React, { useState } from "react";
import { Box, Text, Input, Button, Stack } from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

export default function Login() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    const user = { name, email };
    sessionStorage.setItem("user", JSON.stringify(user));
    navigate("/login/me", { state: { user } });
  }

  return (
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
          />
        </Box>

        <Box>
          <Text mb="1">Email</Text>
          <Input
            type="email"
            placeholder="me@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Box>

       <Button
            type="submit"
            className="border-2 !border-white hover:!border-blue-500 transition-colors"
        >
            Submit
       </Button>


      </Stack>
    </Box>
  );
}
