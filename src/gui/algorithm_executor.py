import time
from algorithms import ALGORITHMS, run_algorithm


class AlgorithmExecutor:

    def __init__(self, map_controller, root):
        self.map_controller = map_controller
        self.root = root
        self.visited_markers = []
        self.is_running = False
        self.should_stop = False

    def run_single_algorithm(self, algo_name, color="blue", width=5, animate=False, delay=0.0):

        start_time = time.perf_counter()

        self.should_stop = False
        self.is_running = True

        self._clear_visited_markers()

        callback = None
        if animate:
            def animation_callback(current_node, visited_set):
                if self.should_stop:
                    raise StopIteration("Animation stopped by user")

                self._draw_visited_node(current_node)
                self.root.update()  # Update UI
                if delay > 0:
                    self.root.after(int(delay * 1000), lambda: None)
                    time.sleep(delay)
            callback = animation_callback

        try:
            path, visited = run_algorithm(
                algo_name,
                self.map_controller.map.graph,
                self.map_controller.start_node,
                self.map_controller.goal_node,
                self.map_controller.map.node_coords,
                callback=callback,
                delay=0,
            )
        except StopIteration:

            self.is_running = False
            return {
                "name": algo_name,
                "time_ms": 0,
                "visited": 0,
                "length_km": None,
                "path_nodes": 0,
                "color": color,
                "success": False,
                "error": "Cancelled",
            }
        except Exception as e:
            self.is_running = False
            return {
                "name": algo_name,
                "time_ms": 0,
                "visited": 0,
                "length_km": None,
                "path_nodes": 0,
                "color": color,
                "success": False,
                "error": str(e),
            }

        duration = (time.perf_counter() - start_time) * 1000
        self.is_running = False

        result = {
            "name": algo_name,
            "time_ms": duration,
            "visited": visited,
            "length_km": None,
            "path_nodes": 0,
            "color": color,
            "success": False,
        }

        if path and len(path) > 0:
            coords = self.map_controller.map.get_path_coords(path)

            if coords:

                path_obj = self.map_controller.map_widget.set_path(
                    coords, color=color, width=width
                )
                self.map_controller.current_paths.append(path_obj)


                length = self.map_controller.map.get_path_length(path)
                result["length_km"] = length / 1000
                result["path_nodes"] = len(path)
                result["success"] = True


                self.map_controller.fit_bounds_to_path(coords)

        return result

    def run_comparison(self, animate=False, delay=0.0):

        colors = ["blue", "red", "green", "purple", "orange", "brown"]
        results = []

        for i, algo_name in enumerate(ALGORITHMS.keys()):

            self._clear_visited_markers()

            result = self.run_single_algorithm(
                algo_name,
                color=colors[i % len(colors)],
                width=4,
                animate=animate,
                delay=delay
            )
            results.append(result)

            if animate:
                time.sleep(0.5)
                self.root.update()

        return results

    def _draw_visited_node(self, node_id):

        try:
            if len(self.visited_markers) > 1000:
                for _ in range(100):
                    if self.visited_markers:
                        old_marker = self.visited_markers.pop(0)
                        try:
                            old_marker.delete()
                        except:
                            pass

            lat, lon = self.map_controller.map.get_node_coords(node_id)
            marker = self.map_controller.map_widget.set_marker(
                lat, lon,
                text="",
                marker_color_circle="lightblue",
                marker_color_outside="blue",
            )
            self.visited_markers.append(marker)
        except Exception as e:
            pass

    def stop_execution(self):
        """Stop the currently running algorithm."""
        self.should_stop = True
        self.is_running = False

        try:
            self.root.update()
        except:
            pass

    def _clear_visited_markers(self):
        markers_to_delete = self.visited_markers[:]
        self.visited_markers.clear()

        for marker in markers_to_delete:
            try:
                marker.delete()
            except:
                pass

    @staticmethod
    def format_results(results):
        lines = []

        header = f"{'Algorithm':<12} {'Time (ms)':<12} {'Nodes':<12} {'Path':<12} {'Distance (km)':<15} {'Status':<10} {'Color'}"
        lines.append(header)
        lines.append("=" * 95)

        def sort_key(r):
            if not r["success"]:
                return (1, float('inf'))
            return (0, r["time_ms"])

        results_sorted = sorted(results, key=sort_key)

        for r in results_sorted:
            if r["success"]:
                line = (
                    f"{r['name']:<12} "
                    f"{r['time_ms']:<12.2f} "
                    f"{r['visited']:<12} "
                    f"{r['path_nodes']:<12} "
                    f"{r['length_km']:<15.2f} "
                    f"{'✅ Found':<10} "
                    f"{r['color']}"
                )
            else:
                error_msg = r.get('error', 'Failed')
                line = (
                    f"{r['name']:<12} "
                    f"{'N/A':<12} "
                    f"{r['visited']:<12} "
                    f"{'N/A':<12} "
                    f"{'N/A':<15} "
                    f"{'❌ ' + error_msg[:8]:<10} "
                    f"{r['color']}"
                )
            lines.append(line)

        if len(results) > 1:
            lines.append("")
            lines.append("─" * 95)
            lines.append("📈 COMPARISON SUMMARY")
            lines.append("─" * 95)

            successful = [r for r in results if r["success"]]

            if successful:
                fastest = min(successful, key=lambda x: x["time_ms"])
                lines.append(f"⚡ Fastest:        {fastest['name']:<15} ({fastest['time_ms']:.2f} ms)")

                shortest = min(successful, key=lambda x: x["length_km"])
                lines.append(f"🎯 Shortest Path:  {shortest['name']:<15} ({shortest['length_km']:.2f} km)")

                least_nodes = min(successful, key=lambda x: x["visited"])
                lines.append(f"💡 Most Efficient: {least_nodes['name']:<15} ({least_nodes['visited']} nodes)")

                for r in successful:
                    r['efficiency'] = r['path_nodes'] / r['visited'] if r['visited'] > 0 else 0
                most_efficient = max(successful, key=lambda x: x['efficiency'])
                lines.append(f"🏆 Best Ratio:     {most_efficient['name']:<15} ({most_efficient['efficiency']:.3f})")
            else:
                lines.append("❌ No algorithms found a valid path")

        return "\n".join(lines)
