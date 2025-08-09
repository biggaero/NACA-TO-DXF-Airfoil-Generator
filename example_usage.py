#!/usr/bin/env python3
"""
Example usage of the NACA airfoil generator
"""

from naca_airfoil_generator import create_dxf_airfoil

# Example 1: NACA 2412 airfoil with 100mm chord
print("Generating NACA 2412 airfoil with 100mm chord...")
create_dxf_airfoil("2412", 100.0, "naca_2412_100mm.dxf")

# Example 2: Symmetric NACA 0012 airfoil with 50mm chord
print("\nGenerating symmetric NACA 0012 airfoil with 50mm chord...")
create_dxf_airfoil("0012", 50.0, "naca_0012_50mm.dxf", num_points=150)

# Example 3: NACA 4412 airfoil with 200mm chord
print("\nGenerating NACA 4412 airfoil with 200mm chord...")
create_dxf_airfoil("4412", 200.0, "naca_4412_200mm.dxf")

print("\nAll airfoils generated successfully!")
