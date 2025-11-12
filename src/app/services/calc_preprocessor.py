from src.app.models.default_values import DEFAULT_VALUES
from src.core.models.logcategory import LogCategory
from src.core.models.message_level import MessageLevel
from src.core.services.log_worker import make_log


class CalcPreprocessor:
    @staticmethod
    def is_default_params(well_data, reservoir_data, fluid_data, fracture_data, logs):
        """
        Проверяет, совпадают ли все введённые пользователем параметры
        с дефолтными значениями из DEFAULT_VALUES.
        Возвращает True, если ВСЁ совпадает, иначе False.
        """
        defaults = DEFAULT_VALUES

        if not CalcPreprocessor.compare_dicts(
            defaults["well"], well_data, logs, "well"
        ):
            print("well is not default")
            return False

        if not CalcPreprocessor.compare_dicts(
            defaults["reservoir"], reservoir_data, logs, "reservoir"
        ):
            print("reservoir is not default")
            return False

        if not CalcPreprocessor.compare_dicts(
            defaults["fluid"], fluid_data, logs, "fluid"
        ):
            print("fluid is not default")
            return False

        default_fractures = defaults["fractures"]
        if len(fracture_data) != len(default_fractures):
            print("fractures count is not default")
            return False

        for f_default, f_user in zip(default_fractures, fracture_data):
            for key in f_default:
                if key == "fracture_id":
                    continue
                if not CalcPreprocessor.is_equal(f_default[key], f_user.get(key)):
                    print("fract is not default")
                    return False

        return True

    @staticmethod
    def is_equal(v1, v2, tol=1e-9):
        # 🔹 Вспомогательная функция для сравнения чисел и bool
        if isinstance(v2, list) and len(v2) == 1:
            v2 = v2[0]
        if isinstance(v1, list) and len(v1) == 1:
            v1 = v1[0]

        # Числа с допуском
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return abs(v1 - v2) < tol

        # Всё остальное — обычное сравнение
        return v1 == v2

    @staticmethod
    def compare_dicts(d1, d2, logs, label=""):
        for key, val in d1.items():
            if key not in d2:
                logs.append(
                    make_log(
                        f"[{label}] ❌ Ключ '{key}' отсутствует во втором словаре",
                        MessageLevel.DEBUG,
                        LogCategory.CHECK_DATA,
                        False,
                    )
                )
                print()
                return False

            val2 = d2[key]

            if not CalcPreprocessor.is_equal(val, val2):
                logs.append(
                    make_log(
                        f"[{label}] ❌ Несовпадение по ключу '{key}': "
                        f"default={val!r} ({type(val).__name__}), "
                        f"user={val2!r} ({type(val2).__name__})",
                        MessageLevel.DEBUG,
                        LogCategory.CHECK_DATA,
                        False,
                    )
                )
                return False
            else:
                logs.append(
                    make_log(
                        f"[{label}] ✅ Совпадает '{key}': {val!r}",
                        MessageLevel.DEBUG,
                        LogCategory.CHECK_DATA,
                        False,
                    )
                )

        return True
