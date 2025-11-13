from typing import List

from src.app.i18n import _
from src.core.models.init_data.models_enum import ModelsEnum


def get_semianalytic_models() -> List:
    """Create semi-analytical model selection table"""
    # Define available models

    models_data = {
        ModelsEnum.POTASHEV_2024: {
            "name": ModelsEnum.POTASHEV_2024.label,
            "citation": {
                "entry_type": "article",
                "author": "Potashev, K., Mazo, A., Mukhina, M. Maklakov, D., Uraimov, A., Khamidullin, M.",
                "title": " High-speed algorithm for computing the inflow to multiple-fractured horizontal wells using stream tubes",
                "journal": "Computational Geosciences",
                "volume": "29",
                "year": "2024",
                "pages": "1389-1411",
                "doi": "10.1007/s10596-024-10322-w",
            },
            "description": "",
            "abstract": _(
                "The scope of the work is to develop high-speed and fairly accurate methods for calculating the "
                "productivity of wells with multi-stage hydraulic fracturing"
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
                    _("Infinite conductivity fractures"),
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
