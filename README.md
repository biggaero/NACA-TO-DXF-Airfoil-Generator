# NACA 4-Digit Airfoil Generator

This Python script generates NACA 4-digit airfoil coordinates and exports them as DXF files suitable for CAD applications, CNC machining, or 3D printing.

## Features

- Generates accurate NACA 4-digit airfoil coordinates
- Exports to DXF format compatible with most CAD software
- Configurable chord length in millimeters
- Adjustable point density for smoother curves
- Command-line interface for easy automation
- Includes airfoil specifications in the output

## Requirements

- Python 3.7+
- numpy >= 1.19.0
- ezdxf >= 1.0.0

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x naca_airfoil_generator.py
```

## Usage

### Command Line Interface

Basic usage:
```bash
python3 naca_airfoil_generator.py [NACA_NUMBER] [CHORD_LENGTH_MM]
```

With options:
```bash
python3 naca_airfoil_generator.py [NACA_NUMBER] [CHORD_LENGTH_MM] -o [OUTPUT_FILE] -n [NUM_POINTS]
```

### Parameters

- `NACA_NUMBER`: 4-digit NACA designation (e.g., 2412, 0012, 4412)
- `CHORD_LENGTH_MM`: Chord length in millimeters (must be positive)
- `-o, --output`: Output DXF filename (optional, default: naca_XXXX_XXXmm.dxf)
- `-n, --num-points`: Number of points along chord (optional, default: 100)

### Examples

1. Generate NACA 2412 with 100mm chord:
```bash
python3 naca_airfoil_generator.py 2412 100.0
```

2. Generate symmetric NACA 0012 with custom filename:
```bash
python3 naca_airfoil_generator.py 0012 50.5 -o wing_profile.dxf
```

3. Generate high-resolution NACA 4412:
```bash
python3 naca_airfoil_generator.py 4412 200.0 -n 200
```

### Python Module Usage

You can also import and use the functions directly in your Python code:

```python
from naca_airfoil_generator import create_dxf_airfoil, naca_4digit_coordinates

# Generate DXF file
create_dxf_airfoil("2412", 100.0, "my_airfoil.dxf")

# Get coordinates only
xu, yu, xl, yl = naca_4digit_coordinates("2412", 100.0, num_points=150)
```

## NACA 4-Digit Nomenclature

NACA 4-digit airfoils are specified by four digits: **MPXX**

- **M**: Maximum camber as percentage of chord (0-9)
- **P**: Position of maximum camber in tenths of chord (0-9)
- **XX**: Maximum thickness as percentage of chord (01-99)

### Examples:
- **NACA 2412**: 2% max camber at 40% chord, 12% thick
- **NACA 0012**: Symmetric (0% camber), 12% thick
- **NACA 4412**: 4% max camber at 40% chord, 12% thick

## Output

The script generates:
- DXF file with airfoil profile as polylines
- Text annotation with NACA designation and chord length
- Console output with airfoil specifications

The DXF file contains:
- Upper surface polyline
- Lower surface polyline
- Leading and trailing edge connections (if needed)
- Text label with specifications

## File Structure

```
├── naca_airfoil_generator.py  # Main script
├── requirements.txt           # Python dependencies
├── example_usage.py          # Example usage script
└── README.md                 # This file
```

## Troubleshooting

### Common Issues:

1. **ImportError**: Install required packages with `pip install -r requirements.txt`
2. **Invalid NACA number**: Must be exactly 4 digits (e.g., 2412, not 242)
3. **Negative chord length**: Chord length must be positive

### Coordinate System:
- Origin (0,0) is at the leading edge
- X-axis: Along the chord (0 to chord_length)
- Y-axis: Perpendicular to chord (positive up for upper surface)

## License

This script is provided as-is for educational and engineering purposes.

## Technical Details

The airfoil generation uses the standard NACA equations:
- Thickness distribution based on the NACA 4-digit series equation
- Mean camber line calculated using parabolic sections
- Surface coordinates computed by offsetting the camber line
- Cosine spacing for better leading/trailing edge definition
