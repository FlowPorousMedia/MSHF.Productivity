from src.core.models.characteristic_data import CharacteristicData


class DimlessConverter:
    def __init__(self, char_data: CharacteristicData):
        self.__char_data: CharacteristicData = char_data

    def make_dimless_geom(self, val: float) -> float:
        return val / self.__char_data.x0

    def make_dim_geom(self, val: float) -> float:
        return val * self.__char_data.x0

    def make_dimless_perm(self, val: float) -> float:
        return val / self.__char_data.perm

    def make_dim_perm(self, val: float) -> float:
        return val * self.__char_data.perm

    def make_dimless_mu(self, val: float) -> float:
        return val / self.__char_data.mu

    def make_dim_mu(self, val: float) -> float:
        return val * self.__char_data.mu

    def make_dimless_press(self, val: float) -> float:
        return (val - self.__char_data.pw) / (self.__char_data.pr - self.__char_data.pw)

    def make_dim_press(self, val: float) -> float:
        return val * (self.__char_data.pr - self.__char_data.pw) + self.__char_data.pw

    def make_dim_q(self, val: float) -> float:
        q0 = self.__char_data.get_q0()
        return val * q0
