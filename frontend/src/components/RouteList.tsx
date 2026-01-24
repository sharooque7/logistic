import type { Route } from "../data/mockRoutes";
import RouteListItem from "./RouteListItem";

interface RouteListProps {
  routes: Route[]; // Routes for current page
  selectedRouteId: string | null;
  onSelect: (id: string) => void;
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  loading: boolean;
}

export default function RouteList({
  routes,
  selectedRouteId,
  onSelect,
  page,
  totalPages,
  onPageChange,
  loading,
}: RouteListProps) {
  // Pagination handlers
  const handlePrev = () => {
    if (page === 0) return;
    onPageChange(page - 1);
  };

  const handleNext = () => {
    if (page + 1 >= totalPages) return;
    onPageChange(page + 1);
  };

  return (
    <div className="flex flex-col gap-2">
      {/* Routes List */}
      {loading ? (
        <div className="text-gray-400 text-center p-4">Loading...</div>
      ) : routes.length > 0 ? (
        routes.map((r) => (
          <RouteListItem
            key={r.route_id}
            route={r}
            selected={r.route_id === selectedRouteId}
            onClick={() => onSelect(r.route_id)}
          />
        ))
      ) : (
        <div className="text-gray-500 text-center p-4">No routes available</div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-between items-center mt-2 text-sm text-gray-400 gap-2">
          <button
            disabled={page === 0 || loading}
            onClick={handlePrev}
            className={`px-2 py-1 rounded hover:bg-gray-700 transition ${
              page === 0 || loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            Prev
          </button>

          <span>
            Page {page + 1} of {totalPages}
          </span>

          <button
            disabled={page + 1 === totalPages || loading}
            onClick={handleNext}
            className={`px-2 py-1 rounded hover:bg-gray-700 transition ${
              page + 1 === totalPages || loading
                ? "opacity-50 cursor-not-allowed"
                : ""
            }`}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
