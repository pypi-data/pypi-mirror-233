from __future__ import annotations
from typing import Any, Callable, Iterable


class Options:
    """# `tdbear.sampler.Options`"""

    title: str = "TDSampler"
    """Title of the application"""

    attribute_list_path: str = "./attribute.txt"
    """file path to attribute list (attribute.txt)"""

    attributes: Iterable[str] | str | None = None
    """instead of attribute.txt, this can be used"""

    assessor_name: str = "unknown"
    """assessor name"""

    product_name: str | list[str] = "unknown"
    """product name(s)"""

    trial_count: int | None = None
    """count of trial"""

    trial_count_increment: bool = False
    """auto increment trial count if this is True"""

    custom_metadata: dict[str, Iterable] = {}
    """custom metadata"""

    comments: str | Iterable[str] | None = None
    """comments"""

    button_shuffle: bool = True
    """attribute buttons will be shuffled if this is True"""

    button_text_color: str = "#ffffff"
    """text color of buttons"""

    button_color_on: str = "#008800"
    """background color of buttons (on)"""

    button_color_off: str = "#082567"
    """background color of buttons (off)"""

    button_color_disabled: str = "#666666"
    """background color of buttons (disabled)"""

    button_color_start: str = "#bb0000"
    """background color of start button"""

    button_color_stop: str = "#bb0000"
    """background color of stop button"""

    button_justification: str = "center"
    """button justification (center, right, left)"""

    button_margin: int = 20
    """button margin"""

    button_size: int | None = None
    """button size"""

    output_folder: str | list[str] = "output"
    """output folder name"""

    output_file_prefix: str = "out"
    """output file prefix"""

    output_file_joint: str = "-"
    """output file joint"""

    output_file_number: int | str | list[str] | None = 0
    """output file number"""

    output_file_increment: bool = True
    """auto increment file number if this is True"""

    output_file_suffix: str = ""
    """output file suffix"""

    output_file_extension: str = ".yml"
    """output file extension"""

    after_task_scoring: tuple[int, int] | None = None
    """range of scoring"""

    max_column: int = 3
    """maximum count of button columns"""

    font_family: str = "Meiryo UI"
    """font family for gui components"""

    font_size: int = 14
    """font size for gui components"""

    title_font_size: int = 25
    """font size of title"""

    theme: str = "SystemDefault"
    """PySimpleGUI theme"""

    text_top: str = ""
    "text shown on the top"

    text_bottom: str = ""
    "text shown on the bottom"

    text_left: str = ""
    "text shown on the left"

    text_right: str = ""
    "text shown on the right"

    @classmethod
    def set(cls, key: str, value: Any) -> Callable:
        setattr(cls, key, value)

        return cls.set
