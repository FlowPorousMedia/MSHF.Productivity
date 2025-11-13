import dash_bootstrap_components as dbc

from src.app.i18n import _


def create_model_details_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(_("Model Details"))),
            dbc.ModalBody(id="model-info-modal-body"),
            dbc.ModalFooter(
                dbc.Button(
                    _("Close"),
                    id="close-model-info-modal",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="model-info-modal",
        is_open=False,
        size="lg",
    )
