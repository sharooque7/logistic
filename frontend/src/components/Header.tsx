import React from "react";

const Header = () => {
  return (
    <div className="h-16 bg-white shadow px-6 flex items-center justify-between">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <div className="flex items-center gap-4">
        <span className="text-gray-700">Admin User</span>
        <button className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">
          Profile
        </button>
      </div>
    </div>
  );
};

export default Header;
