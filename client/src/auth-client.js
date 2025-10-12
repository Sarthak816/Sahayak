// src/lib/auth-client.js
import { createAuthClient } from "better-auth/vue";

export const authClient = createAuthClient({
  baseURL: "http://localhost:8000/api/v1/auth"
});

export const {
  signIn,
  signOut,
  useSession,
} = authClient;
