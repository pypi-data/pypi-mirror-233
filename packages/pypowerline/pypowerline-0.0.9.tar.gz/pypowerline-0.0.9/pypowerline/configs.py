"""
All configurations for pypowerline
"""
from pytconf import Config, ParamCreator


class ConfigGeneral(Config):
    """
    Parameters for configuring the separator
    """
    icons = ParamCreator.create_bool(
        help_string="Should we show icons?",
        default=True,
    )
    colors = ParamCreator.create_bool(
        help_string="Should we use colors?",
        default=True,
    )
