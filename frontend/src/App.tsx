import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import MainApp from "./pages/MainApp";

export default function App() {
  const [username, setUsername] = useState<string | null>(
    localStorage.getItem("username"),
  );

  const handleLoginSuccess = (user: string) => {
    setUsername(user);
    localStorage.setItem("username", user);
  };

  const handleLogout = () => {
    setUsername(null);
    localStorage.removeItem("username");
  };

  return (
    <Routes>
      {/* ROOT */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* LOGIN */}
      <Route
        path="/login"
        element={
          username ? (
            <Navigate to="/insights" replace />
          ) : (
            <Login onLoginSuccess={handleLoginSuccess} />
          )
        }
      />

      {/* DASHBOARD */}
      <Route
        path="/insights"
        element={
          username ? (
            <MainApp
              username={username}
              onLoginSuccess={handleLoginSuccess}
              onLogout={handleLogout}
            />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
    </Routes>
  );
}
