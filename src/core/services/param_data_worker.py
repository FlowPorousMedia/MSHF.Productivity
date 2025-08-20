import copy
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.initial_data import InitialData


class ParamDataWorker:
    def __init__(self):
        self.__original: InitialData = None
        self.__value: float = None

    def create_initial_data(
        self, original: InitialData, value: float, param_type: CalcParamTypeEnum
    ) -> InitialData:
        self.__original = original
        self.__value = value
        match param_type:
            case CalcParamTypeEnum.FRACT_COUNT:
                return self.__fract_count()
            case _:
                raise Exception("aaa")

    def __fract_count(self) -> InitialData:
        original_fract = copy.deepcopy(self.__original.fractures[0])
        result = copy.deepcopy(self.__original)
        result.fractures.clear()

        N = int(self.__value)
        L = result.well.L
        d = L / (N - 1)

        for i in range(N):
            fract = copy.deepcopy(original_fract)
            fract.well_cross_coord = i * d
            result.fractures.append(fract)

        return result
