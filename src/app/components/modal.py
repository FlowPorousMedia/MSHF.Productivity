import dash_bootstrap_components as dbc

def create_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Model Details")),
            dbc.ModalBody(id="model-info-modal-body"),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
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