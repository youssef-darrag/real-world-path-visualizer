"""
Grid-Based Pathfinding Visualizer
Entry point for the Pygame grid visualizer

Run: python src/main_grid.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grid_visualizer.main import PathfindingVisualizer


def main():
    """Launch the grid visualizer application."""
    print("=" * 60)
    print("  🎮  Grid-Based Pathfinding Visualizer")
    print("=" * 60)
    print("\nStarting Pygame visualizer...")
    print("\nControls:")
    print("  • Click algorithm buttons to run visualization")
    print("  • Reset: Clear current visualization")
    print("  • New Grid: Generate new random grid")
    print("\nAlgorithms: A*, BFS, DFS, UCS, DLS")
    print("\nColors:")
    print("  🟢 Green  = Start")
    print("  🔴 Red    = Goal")
    print("  ⬛ Gray   = Obstacles")
    print("  🔵 Blue   = Visited nodes")
    print("  🟡 Yellow = Final path")
    print("=" * 60)
    print()

    # Create and run visualizer
    visualizer = PathfindingVisualizer(
        cell_size=35,
        grid_rows=15,
        grid_cols=20
    )

    visualizer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication closed by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
