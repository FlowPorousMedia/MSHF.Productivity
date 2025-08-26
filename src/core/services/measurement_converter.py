class MeasurementConverter:
    @staticmethod
    def convert_from_cP_to_PaSec(val: float) -> float:
        return val * 0.001

    @staticmethod
    def convert_cm_to_m(val: float) -> float:
        return val * 0.01

    @staticmethod
    def convert_mm_to_m(val: float) -> float:
        if val is None:
            return None
        return val * 0.001

    @staticmethod
    def convert_D_to_m2(val: float) -> float:
        if val is None:
            return None
        return val * 9.869233e-13

    @staticmethod
    def convert_atm_to_Pa(val: float) -> float:
        return val * 101325
