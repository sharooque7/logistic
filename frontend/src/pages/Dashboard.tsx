import React from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import RouteCard from "../components/RouteCard";

const dummyRoutes = [
  { route_id: "Route_001", station_code: "DLA3", stop_count: 10 },
  { route_id: "Route_002", station_code: "DLA7", stop_count: 7 },
  { route_id: "Route_003", station_code: "DLA1", stop_count: 12 },
];

const Dashboard = () => {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="p-6 bg-gray-100 flex-1 overflow-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {dummyRoutes.map((route) => (
            <RouteCard key={route.route_id} {...route} />
          ))}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
