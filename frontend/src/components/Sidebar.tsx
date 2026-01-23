const Sidebar = () => {
  return (
    <div className="w-64 h-screen bg-gray-800 text-white flex flex-col p-4">
      <h1 className="text-2xl font-bold mb-6">Logistics App</h1>
      <nav className="flex flex-col gap-3">
        <a href="#" className="hover:bg-gray-700 px-3 py-2 rounded">Dashboard</a>
        <a href="#" className="hover:bg-gray-700 px-3 py-2 rounded">Routes</a>
        <a href="#" className="hover:bg-gray-700 px-3 py-2 rounded">Metrics</a>
        <a href="#" className="hover:bg-gray-700 px-3 py-2 rounded">Logout</a>
      </nav>
    </div>
  );
};

export default Sidebar;
