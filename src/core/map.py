import os
import random
import osmnx as ox

class Map:
    def __init__(self, filename: str = "map_data.graphml"):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        self.data_dir = os.path.join(project_root, "data")
        os.makedirs(self.data_dir, exist_ok=True)

        self.filename = os.path.join(self.data_dir, filename)

        self.graph = None
        self.node_keys = []
        self.node_coords = {}

    def load_map(self, location: str, force_download: bool = False):

        try:
            if os.path.exists(self.filename) and not force_download:
                print(f"📂 Loading cached map from: {self.filename}")
                self.graph = ox.load_graphml(self.filename)
                status = f"Loaded cached map data from {os.path.basename(self.filename)}"
            else:
                print(f"🌍 Downloading map data for: {location}")
                self.graph = ox.graph_from_place(location, network_type="drive")

                print(f"💾 Saving to: {self.filename}")
                ox.save_graphml(self.graph, self.filename)
                status = f"Downloaded and cached map data to data/{os.path.basename(self.filename)}"

            self.node_keys = list(self.graph.nodes)
            self.node_coords = {
                n: (data["y"], data["x"]) for n, data in self.graph.nodes(data=True)
            }

            print(f"✅ Map loaded: {len(self.node_keys)} nodes, {self.graph.number_of_edges()} edges")

            return True, status

        except Exception as e:
            error_msg = f"Error loading map: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def get_random_endpoints(self):

        start = random.choice(self.node_keys)
        end = random.choice(self.node_keys)

        while end == start:
            end = random.choice(self.node_keys)

        return start, end

    def get_node_coords(self, node_id: int):
        return self.node_coords[node_id]

    def get_path_length(self, path: list[int]):
        total_length = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge_data = self.graph.get_edge_data(u, v)[0]
            total_length += edge_data.get("length", 0)
        return total_length

    def get_path_coords(self, path: list[int]):
        if not path:
            return []

        coords = [self.node_coords[path[0]]]

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge_data = self.graph.get_edge_data(u, v)
            if edge_data is None:
                coords.append(self.node_coords[v])
                continue

            edge_data = edge_data[0]

            if "geometry" in edge_data:
                curve_points = [(lat, lon) for lon, lat in edge_data["geometry"].coords]
                coords.extend(curve_points[1:])  # Skip first point (already added)
            else:
                coords.append(self.node_coords[v])
        return coords
