#!/usr/bin/env python3
"""
NACA 4-digit Airfoil Generator
Generates airfoil coordinates from NACA 4-digit designation and exports to DXF format.
"""

import numpy as np
import math
import argparse
import sys

try:
    import ezdxf
except ImportError:
    print("Error: ezdxf library not found. Install it with: pip install ezdxf")
    sys.exit(1)


def parse_naca_4digit(naca_string):
    """
    Parse NACA 4-digit designation.
    
    Args:
        naca_string (str): 4-digit NACA designation (e.g., "2412")
    
    Returns:
        tuple: (max_camber_percent, max_camber_position, thickness_percent)
    """
    if len(naca_string) != 4 or not naca_string.isdigit():
        raise ValueError("NACA designation must be exactly 4 digits")
    
    max_camber_percent = int(naca_string[0])  # Maximum camber as percentage of chord
    max_camber_position = int(naca_string[1])  # Position of maximum camber in tens of percent
    thickness_percent = int(naca_string[2:])  # Maximum thickness as percentage of chord
    
    return max_camber_percent, max_camber_position, thickness_percent


def naca_4digit_coordinates(naca_designation, chord_length_mm, num_points=100):
    """
    Generate NACA 4-digit airfoil coordinates.
    
    Args:
        naca_designation (str): 4-digit NACA designation
        chord_length_mm (float): Chord length in millimeters
        num_points (int): Number of points along the chord
    
    Returns:
        tuple: (upper_surface_x, upper_surface_y, lower_surface_x, lower_surface_y)
    """
    m, p, t = parse_naca_4digit(naca_designation)
    
    # Convert to decimal values
    m = m / 100.0  # Maximum camber
    p = p / 10.0   # Position of maximum camber
    t = t / 100.0  # Maximum thickness
    
    # Generate x coordinates (cosine spacing for better leading/trailing edge resolution)
    beta = np.linspace(0, np.pi, num_points)
    x = (1 - np.cos(beta)) / 2
    
    # Calculate thickness distribution
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    
    # Calculate camber line
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    
    if m > 0 and p > 0:  # Cambered airfoil
        # Forward of maximum camber
        mask1 = x <= p
        yc[mask1] = (m / p**2) * (2 * p * x[mask1] - x[mask1]**2)
        dyc_dx[mask1] = (2 * m / p**2) * (p - x[mask1])
        
        # Aft of maximum camber
        mask2 = x > p
        yc[mask2] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * x[mask2] - x[mask2]**2)
        dyc_dx[mask2] = (2 * m / (1 - p)**2) * (p - x[mask2])
    
    # Calculate surface coordinates
    theta = np.arctan(dyc_dx)
    
    # Upper surface
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    
    # Lower surface
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    # Scale by chord length and convert to mm
    xu *= chord_length_mm
    yu *= chord_length_mm
    xl *= chord_length_mm
    yl *= chord_length_mm
    
    return xu, yu, xl, yl


def create_dxf_airfoil(naca_designation, chord_length_mm, output_filename, num_points=100):
    """
    Create DXF file with NACA airfoil.
    
    Args:
        naca_designation (str): 4-digit NACA designation
        chord_length_mm (float): Chord length in millimeters
        output_filename (str): Output DXF filename
        num_points (int): Number of points along the chord
    """
    # Generate airfoil coordinates
    xu, yu, xl, yl = naca_4digit_coordinates(naca_designation, chord_length_mm, num_points)
    
    # Create new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Create upper surface polyline
    upper_points = [(x, y) for x, y in zip(xu, yu)]
    msp.add_lwpolyline(upper_points, close=False)
    
    # Create lower surface polyline (reverse order for proper direction)
    lower_points = [(x, y) for x, y in zip(reversed(xl), reversed(yl))]
    msp.add_lwpolyline(lower_points, close=False)
    
    # Add connecting lines at leading and trailing edges if needed
    # Leading edge connection
    if abs(xu[0] - xl[0]) > 0.001 or abs(yu[0] - yl[0]) > 0.001:
        msp.add_line((xu[0], yu[0]), (xl[0], yl[0]))
    
    # Trailing edge connection
    if abs(xu[-1] - xl[-1]) > 0.001 or abs(yu[-1] - yl[-1]) > 0.001:
        msp.add_line((xu[-1], yu[-1]), (xl[-1], yl[-1]))
    
    # Add text annotation
    msp.add_text(
        f'NACA {naca_designation}\nChord: {chord_length_mm:.1f}mm',
        dxfattribs={
            'height': chord_length_mm * 0.05,
            'insert': (chord_length_mm * 0.1, chord_length_mm * 0.2)
        }
    )
    
    # Save DXF file
    doc.saveas(output_filename)
    print(f"Airfoil saved as: {output_filename}")
    
    # Print some statistics
    m, p, t = parse_naca_4digit(naca_designation)
    print(f"NACA {naca_designation} specifications:")
    print(f"  Maximum camber: {m}% at {p*10}% chord")
    print(f"  Maximum thickness: {t}%")
    print(f"  Chord length: {chord_length_mm:.1f} mm")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate NACA 4-digit airfoil and export to DXF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python naca_airfoil_generator.py 2412 100.0 -o airfoil_2412.dxf
  python naca_airfoil_generator.py 0012 50.5 -o symmetric_airfoil.dxf -n 200
        """
    )
    
    parser.add_argument('naca', type=str, 
                       help='4-digit NACA designation (e.g., 2412, 0012)')
    parser.add_argument('chord', type=float,
                       help='Chord length in millimeters')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output DXF filename (default: naca_XXXX_XXXmm.dxf)')
    parser.add_argument('-n', '--num-points', type=int, default=100,
                       help='Number of points along chord (default: 100)')
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        if args.chord <= 0:
            raise ValueError("Chord length must be positive")
        
        if args.num_points < 10:
            raise ValueError("Number of points must be at least 10")
        
        # Generate default filename if not provided
        if args.output is None:
            args.output = f"naca_{args.naca}_{args.chord:.0f}mm.dxf"
        
        # Create airfoil DXF
        create_dxf_airfoil(args.naca, args.chord, args.output, args.num_points)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
