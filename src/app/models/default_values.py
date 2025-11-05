DEFAULT_VALUES = {
    "fracture": [
        {
            "fracture_id": i + 1,
            "length_plus": 100,
            "length_minus": 100,
            "width": 40,
            "permeability": 10000,
            "well_cross": i * 400,
        }
        for i in range(3)
    ],
    "well": {
        "length": 800,
        "radius": 8,
        "pressure": 80,
        "perforated": True,
    },
    "reservoir": {
        "radius": 200,
        "height": 10,
        "permeability": 0.1,
        "pressure": 100,
    },
    "fluid": {
        "viscosity": 1.0,
        "compressibility": 1e-5,
        "density": 800,
        "fvf": 1.2,  # Formation volume factor
    },
}
