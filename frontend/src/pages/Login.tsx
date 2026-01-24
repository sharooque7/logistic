import { useState } from "react";
import { mockLogin } from "../data/auth";

interface LoginPageProps {
  onLoginSuccess: (user: string) => void;
}

export default function LoginPage({ onLoginSuccess }: LoginPageProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (mockLogin(username, password)) {
      onLoginSuccess(username);
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-950 text-gray-100">
      <form
        onSubmit={handleSubmit}
        className="w-96 bg-gray-900 border border-gray-800 rounded-lg p-6 flex flex-col gap-4"
      >
        <h1 className="text-xl font-semibold text-center">Login</h1>

        <input
          className="bg-gray-800 border border-gray-700 rounded px-3 py-2"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          className="bg-gray-800 border border-gray-700 rounded px-3 py-2"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 rounded py-2"
        >
          Login
        </button>
        <p className="text-xs text-gray-500 text-center">
          Hint: <b>admin / admin123</b>
        </p>
      </form>
    </div>
  );
}
