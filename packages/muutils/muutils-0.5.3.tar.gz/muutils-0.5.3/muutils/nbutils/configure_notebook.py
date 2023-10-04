import os
import typing
import warnings

import matplotlib.pyplot as plt  # type: ignore[import]

PLOTLY_IMPORTED: bool
try:
    import plotly.io as pio  # type: ignore[import]
except ImportError:
    warnings.warn("Plotly not installed. Plotly plots will not be available.")
    PLOTLY_IMPORTED = False
else:
    PLOTLY_IMPORTED = True


IN_JUPYTER: bool = not "_" in os.environ

if IN_JUPYTER:
    from IPython import get_ipython  # type: ignore[import]

from muutils.mlutils import get_device, set_reproducibility


def configure_notebook(
    *args,
    seed: int = 42,
    device: typing.Any = None,  # this can be a string, torch.device, or None
    dark_mode: bool = True,
):
    """Shared Jupyter notebook setup steps:
    - Set random seeds and library reproducibility settings
    - Set device based on availability
    - Set module reloading before code execution
    - Set plot rendering and formatting
    """

    # Set seeds and other reproducibility-related library options
    set_reproducibility(seed)

    # Reload modules before executing user code
    if IN_JUPYTER:
        ipython = get_ipython()
        if "IPython.extensions.autoreload" not in ipython.extension_manager.loaded:
            ipython.magic("load_ext autoreload")
            ipython.magic("autoreload 2")

        # Specify plotly renderer for vscode
        if PLOTLY_IMPORTED:
            pio.renderers.default = "notebook_connected"

            if dark_mode:
                pio.templates.default = "plotly_dark"
                plt.style.use("dark_background")

    return get_device(device)
