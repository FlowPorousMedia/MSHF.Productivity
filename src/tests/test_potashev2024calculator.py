import os
import sys
from pathlib import Path


# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SRC_DIR))

import csv
import unittest
import numpy as np

from src.core.models.init_data.fluid_initial_data import FluidInitialData
from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.initial_data import InitialData
from src.core.models.init_data.reservoir_initial_data import ReservoirInitialData
from src.core.models.init_data.well_initial_data import WellInitialData
from src.core.services.measurement_converter import MeasurementConverter
from src.core.services.semianalytical_models.potashev2024_calculator import (
    Potashev2024Calculator,
)


class TestPotashev2024Calculator(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(1 + 1, 2)

    def setUp(self):
        """Initialize test data and calculator before each test"""
        self.inner_calculator = Potashev2024Calculator.InnerSectorCalculator()
        self.outer_calculator = Potashev2024Calculator.OuterSectorCalculator()
        self.initial_data = self.__create_simple_initial_data()
        self.output_dir = self.__define_output_dir()

    def test_inner_sector_qf_r_to_file(self) -> None:
        xf = 100
        rcs = [115, 130, 150, 180, 200, 250, 300]  # np.arange(115, 301, 15)
        qfs = [0] * len(rcs)

        self.initial_data.fractures[0].len_p = xf
        self.initial_data.fractures[0].len_m = xf

        for i, rc in enumerate(rcs):
            self.initial_data.reservoir.rc = rc
            qf_quarter = self.inner_calculator.calc_rate(
                self.initial_data, 0, False, False
            )
            qfs[i] = qf_quarter

        # Save results to CSV
        filename = self.output_dir / "rc_qf_inner.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["rc", "qf"])
            for rc, qf in zip(rcs, qfs):
                formatted_qf = f"{qf:.3f}"
                writer.writerow([rc, formatted_qf])

        # Verify file creation
        assert os.path.exists(filename), f"Output file {filename} was not created"
        print(f"Saved {len(rcs)} records to {os.path.abspath(filename)}")

    def test_outer_sector_qf_r_to_file(self) -> None:
        xf = 100
        rcs = [115, 130, 150, 180, 200, 250, 300, 500, 1000]  # np.arange(115, 301, 15)
        qfs = [0] * len(rcs)

        self.initial_data.fractures[0].len_p = xf
        self.initial_data.fractures[0].len_m = xf

        for i, rc in enumerate(rcs):
            self.initial_data.reservoir.rc = rc
            qf_quarter = self.outer_calculator.calc_rate(
                self.initial_data, 0, False, False
            )
            qfs[i] = qf_quarter

        # Save results to CSV
        filename = self.output_dir / "rc_qf_outer.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["rc", "qf"])
            for rc, qf in zip(rcs, qfs):
                formatted_qf = f"{qf:.3f}"
                writer.writerow([rc, formatted_qf])

        # Verify file creation
        assert os.path.exists(filename), f"Output file {filename} was not created"
        print(f"Saved {len(rcs)} records to {os.path.abspath(filename)}")

    def test_outer_sector_lambda(self) -> None:
        exact = 0.565303  # real part from Wolfram Mathematica
        real = self.outer_calculator._OuterSectorCalculator__lam(0.1, 1.15)
        self.assertAlmostEqual(real, exact, 2, "Lambda error")

    def test_outer_sector_omega(self) -> None:
        exact = 1.00148  # real part from Wolfram Mathematica
        real = self.outer_calculator._OuterSectorCalculator__omega(0.1, 0.1, 1.15)
        self.assertAlmostEqual(real, exact, 5, "Lambda error")

    def test_outer_sector_J(self) -> None:
        exact = 1.85741  # real part from Wolfram Mathematica
        real = self.outer_calculator._OuterSectorCalculator__J(0.1, 1.15)
        self.assertAlmostEqual(real, exact, 2, "Lambda error")

    def test_outer_Q(self) -> None:
        exact = 2.87685  # real part from Wolfram Mathematica
        real = self.outer_calculator._OuterSectorCalculator__Q(1.15)
        self.assertAlmostEqual(real, exact, 2, "Q error")

    def test_inner_Q(self) -> None:
        test_cases = [
            # (r, l, expected_result)
            (1.15, 0.2, 0.826975),
            (1.5, 0.2, 0.353202),
            (3.0, 0.2, 0.10975),
            (1.5, 0.5, 0.663436)
        ]

        for r, l, expected in test_cases:
            with self.subTest(r=r, l=l):
                real = self.inner_calculator._InnerSectorCalculator__Q(r, l)
                self.assertAlmostEqual(real, expected, 2, f"Q error for r={r}, l={l}")

    def __create_simple_initial_data(self) -> InitialData:
        mc = MeasurementConverter()

        result = InitialData()

        # fracture
        fract = FractInitialData()
        fract.len_p = 100
        fract.len_m = 100
        fract.width = 0.01
        fract.perm = 1e-8
        fract.well_cross_coord = 20  # 100 m distance between fracts
        result.fractures.append(fract)

        # resevoir
        reservoir = ReservoirInitialData()
        reservoir.rc = 150
        reservoir.H = 10
        reservoir.perm = 1e-13
        reservoir.pr = mc.convert_atm_to_Pa(100)
        result.reservoir = reservoir

        # well
        well = WellInitialData()
        well.L = fract.well_cross_coord * 2.0
        well.rw = 0.08
        well.pw = mc.convert_atm_to_Pa(80)
        well.is_perforated = False
        result.well = well

        # fluid
        fluid = FluidInitialData()
        fluid.mu = 1e-3
        result.fluid = fluid

        return result

    def __define_output_dir(self) -> Path:
        # Get current test file's directory
        current_dir = Path(__file__).resolve().parent

        # Navigate to project root
        project_root = current_dir.parent.parent

        # Create 'out' directory if it doesn't exist
        output_dir = project_root / "out"
        output_dir.mkdir(exist_ok=True, parents=True)

        return output_dir
