from src.app.callbacks import (
    calculate_button_callbacks,
    fracture_table_callbacks,
    model_info_view_callbacks,
    parametric_settings_callbacks,
    well_params_component_callbacks,
    reservoir_params_component_callbacks,
    fluid_params_component_callbacks,
    graph_content_callbacks,
    table_content_callbacks,
    navbar_callbacks,
)


def register_all_callbacks(app):
    fracture_table_callbacks.register(app)
    well_params_component_callbacks.register(app)
    reservoir_params_component_callbacks.register(app)
    fluid_params_component_callbacks.register(app)
    model_info_view_callbacks.register(app)
    parametric_settings_callbacks.register(app)
    calculate_button_callbacks.register(app)
    graph_content_callbacks.register(app)
    table_content_callbacks.register(app)
    navbar_callbacks.register(app)
