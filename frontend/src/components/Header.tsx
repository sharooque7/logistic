import { useState } from "react";
import { FaUserCircle } from "react-icons/fa";

interface HeaderProps {
  username: string;
  onLogout: () => void;
}

export default function Header({ username, onLogout }: HeaderProps) {
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    setOpen(false);
    onLogout();
  };

  return (
    <header className="h-16 flex items-center justify-between px-6 bg-gray-950 border-b border-gray-800 shadow-sm">
      {/* Left */}
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
          RI
        </div>
        <div className="flex flex-col">
          <span className="text-lg font-semibold text-white">
            Route Intelligence
          </span>
          <span className="text-xs text-gray-400">
            Delivery Route Comparison
          </span>
        </div>
      </div>

      {/* Right */}
      <div className="relative">
        <button
          onClick={() => setOpen(!open)}
          className="flex items-center space-x-2 bg-gray-800 px-3 py-1 rounded-md hover:bg-gray-700 transition"
        >
          <FaUserCircle className="text-gray-300 w-5 h-5" />
          <span className="text-sm text-gray-300">{username}</span>
          <svg
            className={`w-3 h-3 text-gray-300 transition-transform ${
              open ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {open && (
          <div className="absolute right-0 mt-2 w-32 bg-gray-800 border border-gray-700 rounded-md shadow-lg py-1 z-10">
            <button
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-gray-700 hover:text-red-300 rounded transition"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
