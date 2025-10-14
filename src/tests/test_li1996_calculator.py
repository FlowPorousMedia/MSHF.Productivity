import unittest
from src.core.models.calculator_settings import CalculatorSettings
from src.core.models.init_data.fluid_initial_data import FluidInitialData
from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.initial_data import InitialData
from src.core.models.init_data.reservoir_initial_data import ReservoirInitialData
from src.core.models.init_data.well_initial_data import WellInitialData
from src.core.services.analyt_models.li1996_calculator import Li1996Calculator


class TestLi1996Calculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Li1996Calculator()
        self.setts = CalculatorSettings()
        self.setts.Li96_account_rc = False

    def create_init_data(
        self,
        N: int = 1,
        L: float = 200,
        xf: float = 30,
        R: float = 120,
        kf: float = 1,
        H: float = 10,
        pr: float = 1e7,
        pw: float = 8e6,
        kr: float = 1e-13,
        rw: float = 0.08,
        mu: float = 1e-3,
        wf: float = 0.01,
        Ld: float = 0.0,
        is_well_perf: bool = False,
    ):
        result = InitialData()
        kr = kr
        kf = kf
        if N == 1:
            d = 0  # Only one fracture, so no spacing needed
        else:
            d = L / (2.0 * (N - 1))
        for i in range(int(N)):
            fract = FractInitialData()
            fract.len_p = xf
            fract.len_m = xf
            fract.width = wf
            fract.perm = kf
            fract.well_cross_coord = i * 2 * d if N > 1 else L / 2.0
            result.fractures.append(fract)
        reservoir = ReservoirInitialData()
        reservoir.rc = R
        reservoir.H = H
        reservoir.perm = kr
        reservoir.pr = pr
        result.reservoir = reservoir
        well = WellInitialData()
        well.L = L
        well.rw = rw
        well.pw = pw
        well.is_perforated = is_well_perf
        well.Ld = Ld
        result.well = well
        fluid = FluidInitialData()
        fluid.mu = mu
        result.fluid = fluid
        return result

    def test_calc_q_basic(self):
        init_data = self.create_init_data()
        q = self.calculator.calc_q(init_data, self.setts)
        self.assertIsInstance(q, float)
        self.assertGreater(q, 0)

    def test_calc_q_zero_pressure_diff(self):
        init_data = self.create_init_data()
        init_data.reservoir.pr = 1e7
        init_data.well.pw = 1e7
        q = self.calculator.calc_q(init_data, self.setts)
        self.assertEqual(q, 0.0)

    def test_calc_q_known_case1(self):
        init_data = self.create_init_data(
            N=1,
            L=200,
            xf=30,
            R=200,
            kf=1e-1,
            H=20.0,
            pr=2e6,
            pw=1e6,
            kr=1e-13,
            rw=0.1,
            mu=1e-3,
            wf=0.005,
            Ld=1.0,
            is_well_perf=False,
        )

        q = self.calculator.calc_q(init_data, self.setts)
        print(f"q = {q}")
        self.assertAlmostEqual(q, 0.0015894, 6)

    def test_calc_q_known_case2(self):
        init_data = self.create_init_data(
            N=1,
            L=200,
            xf=30,
            R=200,
            kf=1e-1,
            H=20.0,
            pr=2e6,
            pw=1e6,
            kr=1e-13,
            rw=0.1,
            mu=1e-3,
            wf=0.005,
            Ld=0.0,
            is_well_perf=True,
        )

        q = self.calculator.calc_q(init_data, self.setts)
        print(f"q = {q}")
        self.assertAlmostEqual(q, 0.0015894, 6)

    def test_calc_q_known_case3(self):
        init_data = self.create_init_data(
            N=1,
            L=200,
            xf=30,
            R=200,
            kf=1e-1,
            H=20.0,
            pr=2e6,
            pw=1e6,
            kr=1e-13,
            rw=0.1,
            mu=1e-3,
            wf=0.005,
            Ld=1.0,
            is_well_perf=True,
        )
        q = self.calculator.calc_q(init_data, self.setts)
        print(f"q = {q}")
        self.assertAlmostEqual(q, 0.00375655, 6)


if __name__ == "__main__":
    unittest.main()
