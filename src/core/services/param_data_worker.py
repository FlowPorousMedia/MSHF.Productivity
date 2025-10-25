import copy
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.initial_data import InitialData


class ParamDataWorker:
    def __init__(self):
        self.__original_init_data: InitialData = None
        self.__value: float = None

    def create_initial_data(
        self, original: InitialData, value_in_si: float, param_type: CalcParamTypeEnum
    ) -> InitialData:
        """
        Создаёт новую InitialData с изменённым параметром.

        Args:
            original: Исходные данные.
            value_in_si: Значение параметра **в системе СИ** (м, м² и т.д.).
            param_type: Тип изменяемого параметра.

        Returns:
            Новая копия InitialData с обновлённым параметром.
        """
        self.__original_init_data = original
        self.__value = value_in_si
        match param_type:
            case CalcParamTypeEnum.FRACT_COUNT:
                return self.__fract_count()
            case CalcParamTypeEnum.RES_RAD:
                return self.__res_rad()
            case CalcParamTypeEnum.RES_HEIGTH:
                return self.__res_heigth()
            case CalcParamTypeEnum.WELL_LEN:
                return self.__well_len()
            case CalcParamTypeEnum.FRACT_LEN:
                return self.__fract_len()
            case CalcParamTypeEnum.FRACT_PERM:
                return self.__fract_perm()
            case CalcParamTypeEnum.FRACT_WIDTH:
                return self.__fract_width()
            case _:
                raise Exception("aaa")

    def __fract_count(self) -> InitialData:
        original_fract = copy.deepcopy(self.__original_init_data.fractures[0])
        result = copy.deepcopy(self.__original_init_data)
        result.fractures.clear()

        N = int(self.__value)
        L = result.well.L
        d = L / (N - 1)

        for i in range(N):
            fract = copy.deepcopy(original_fract)
            fract.well_cross_coord = i * d
            result.fractures.append(fract)

        return result

    def __res_rad(self):
        result = copy.deepcopy(self.__original_init_data)
        R = float(self.__value)
        result.reservoir.rc = R

        return result

    def __res_heigth(self):
        result = copy.deepcopy(self.__original_init_data)
        H = float(self.__value)
        result.reservoir.H = H

        return result

    def __well_len(self):
        result = copy.deepcopy(self.__original_init_data)
        L = float(self.__value)
        result.well.L = L

        return result

    def __fract_len(self):
        result = copy.deepcopy(self.__original_init_data)
        xf = float(self.__value)

        for fract in result.fractures:
            fract: FractInitialData
            fract.len_m = xf
            fract.len_p = xf

        return result

    def __fract_perm(self):
        result = copy.deepcopy(self.__original_init_data)
        kf = float(self.__value)

        for fract in result.fractures:
            fract: FractInitialData
            fract.perm = kf

        return result

    def __fract_width(self):
        result = copy.deepcopy(self.__original_init_data)
        wf = float(self.__value)

        for fract in result.fractures:
            fract: FractInitialData
            fract.width = wf

        return result
