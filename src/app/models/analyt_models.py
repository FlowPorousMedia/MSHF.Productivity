from typing import List

from src.app.i18n import _
from src.core.models.init_data.models_enum import ModelsEnum


def get_analytic_models() -> List:
    """Create analytical model selection table"""
    # Define available models

    models_data = {
        ModelsEnum.LI_1996: {
            "name": ModelsEnum.LI_1996.label,
            "citation": {
                "entry_type": "inproceedings",
                "author": "Li, Hujun, Jia, Zhengqi, and Zhaosheng Wei",
                "title": "A New Method to Predict Performance of Fractured Horizontal Wells.",
                "conference": "Paper presented at the International Conference on Horizontal Well Technology",
                "city": "Calgary, Alberta, Canada",
                "date": "November 1996",
                "doi": "10.2118/37051-MS",
            },
            "description": "",
            "abstract": _(
                "A practical method to predict performance of a horizontal well which is hydraulically fractured and "
                "partially perforated has been proposed in this paper. Using the mathematical model presented in this "
                "paper, factors affecting performance of a hydraulically fractured horizontal well have been analyzed"
            ),
            "parameters": {
                "applicability": [
                    _(
                        "Prediction of performance for hydraulically fractured horizontal wells"
                    ),
                    _("Wells with partial perforation"),
                ],
                "limitations": [
                    _(
                        "Fracture half-length is equal in both directions from the wellbore"
                    ),
                    _("Fracture height is equal to the reservoir height"),
                ],
            },
        },
        ModelsEnum.GUO_1997: {
            "name": ModelsEnum.GUO_1997.label,
            "citation": {
                "entry_type": "inproceedings",
                "author": "Guo, B., and D.S. Schechter",
                "title": "A Simple and Rigorous Mathematical Model for Estimating Inflow Performance of Wells Intersecting Long Fractures",
                "conference": "Paper presented at the SPE Asia Pacific Oil and Gas Conference and Exhibition",
                "city": "Kuala Lumpur, Malaysia",
                "date": "April 1997",
                "doi": "10.2118/38104-MS",
            },
            "description": "",
            "abstract": _(
                "This paper presents a simple and more rigorous mathematical model for predicting performance of vertical and "
                "horizontal wells intersecting fractures fully penetrating reservoir sections. An important feature of the new model is that "
                "it allows rigorous coupling of flow in the matrix and flow in the fracture"
            ),
            "parameters": {
                "applicability": [
                    _(
                        "Prediction of performance for hydraulically fractured horizontal wells"
                    ),
                ],
                "limitations": [
                    _(
                        "Fracture half-length is equal in both directions from the wellbore"
                    ),
                    _("Fracture height is equal to the reservoir height"),
                    _("Well perforation does not take into account"),
                ],
            },
        },
        ModelsEnum.GUO_2009: {
            "name": ModelsEnum.GUO_2009.label,
            "citation": {
                "entry_type": "article",
                "author": "Guo, Boyun, Yu, Xiance, and Mohammad Khoshgahdam",
                "title": "Simple Analytical Model for Predicting Productivity of Multifractured Horizontal Wells",
                "journal": "SPE Res Eval & Eng",
                "volume": "12",
                "year": "2009",
                "pages": "879–885",
                "doi": "10.2118/114452-PA",
            },
            "description": "",
            "abstract": _("Formulated a simple analytical model that describes the productivity of multifractured horizontal wells better. "
            "The new model couples the radial flow in the nonfractured region of reservoir, the linear flow toward the fractures in the "
            "fractured region, the linear flow in the fracture, and the radial flow in the fracture toward the horizontal wellbore. "
            "It can model pseudosteady-state flow of reservoir fluids in reservoir sections of any shape, with the fractured region being "
            "located at any area in the reservoir"),
            "parameters": {
                "applicability": [
                    _("Prediction of performance for hydraulically fractured horizontal wells"),
                ],
                "limitations": [
                    _("Fracture half-length is equal in both directions from the wellbore"),
                    _("Fracture height is equal to the reservoir height"),
                    _("Well perforation does not take into account"),
                ],
            },
        },
        ModelsEnum.ELKIN_2016_12: {
            "name": ModelsEnum.ELKIN_2016_12.label,
            "citation": {
                "entry_type": "article",
                "author": "С.В. Елкин, А.А. Алероев, Н.А. Веремко, М.В. Чертенков",
                "title": "Учет влияния безразмерной проводимости на экспресс-расчет дебита жидкости после многозонного гидроразрыва пласта",
                "journal": "Нефт. хоз-во",
                "volume": "12",
                "year": "2016",
                "pages": "110-113",
                "url": "https://www.oil-industry.net/Journal/author/recens.php?ID=11007&art=230007&PAGEN_1=7&forgot_password=yes&backurl=%2FJournal%2Fauthor%2Frecens.php%3FID%3D11007%26art%3D230007%26PAGEN_1%3D7",
            },
            "description": "",
            "abstract": "",
            "parameters": {
                "applicability": [
                    _("Prediction of performance for hydraulically fractured horizontal wells"),
                ],
                "limitations": [
                    _("Fracture half-length is equal in both directions from the wellbore"),
                    _("Fracture height is equal to the reservoir height"),
                    _("Well perforation does not take into account"),
                ],
            },
        },
    }

    return [
        {
            "id": model.value,
            "name": data["name"],
            "info": "?",  # this is just button Name in table
            "metadata": data,  # Все остальные данные здесь!
        }
        for model, data in models_data.items()
    ]
