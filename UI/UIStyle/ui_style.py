from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from typing import TextIO, Union
import json

LOGGING_STREAM: Union[TextIO, None] = None

PALETTE_KEYS = {"Active": 0,
                "All": 5,
                "AlternateBase": 16,
                "Background": 10,
                "Base": 9,
                "BrightText": 7,
                "Button": 1,
                "ButtonText": 8,
                "Current": 4,
                "Dark": 4,
                "Disabled": 1,
                "Foreground": 0,
                "Highlight": 12,
                "HighlightedText": 13,
                "Inactive": 2,
                "Light": 2,
                "Link": 14,
                "LinkVisited": 15,
                "Mid": 5,
                "Midlight": 3,
                "NColorGroups": 3,
                "NColorRoles": 21,
                "Normal": 0,
                "NoRole": 17,
                "PlaceholderText": 20,
                "Shadow": 11,
                "Text": 6,
                "ToolTipBase": 18,
                "ToolTipText": 19,
                "Window": 10,
                "WindowText": 0}

FONT_KEYS = {'selector', 'font-family', 'font-size', 'font-units'}


def _load_palette(src: dict) -> QPalette():
    if 'Palette' not in src:
        return QPalette()
    palette = src['Palette']
    q_palette = QPalette()
    for key, val in palette.items():
        if key not in PALETTE_KEYS:
            continue
        try:
            q_palette.setColor(PALETTE_KEYS[key], QColor(*tuple(int(v) for v in val.values())))
        except ValueError as err:
            print(f"load pallet:  {err}", file=LOGGING_STREAM)
            q_palette.setColor(PALETTE_KEYS[key], QColor(120, 130, 140))
        except RuntimeError as err:
            print(f"load pallet:  {err}", file=LOGGING_STREAM)
            q_palette.setColor(PALETTE_KEYS[key], QColor(120, 130, 140))
    return q_palette


def _font_setup(*value: str) -> str:
    return f"{value[0]}{{font-family: {value[1]}; font-size: {value[2]}{value[3]};}}" if len(value) == 4 else ""


def load_style(style_src: str, application: QApplication) -> None:
    try:
        with open(style_src, 'rt') as input_file:
            json_file = json.load(input_file)
            application.setPalette(_load_palette(json_file))
            if 'WidgetsFontStyles' in json_file:
                widgets_styles = json_file['WidgetsFontStyles']
                application.setStyleSheet(
                    '\n'.join(_font_setup(*tuple(v[key] for key in FONT_KEYS if key in v)) for v in widgets_styles))
                print('\n'.join(_font_setup(*tuple(v[key] for key in FONT_KEYS if key in v)) for v in widgets_styles))
            if 'ApplicationStyles' in json_file:
                app_font = json_file['ApplicationStyles']
                font = application.font()
                font.setFamily(app_font["font-family"] if "font-family" in app_font else "Consolas")
                if "font-units" not in app_font:
                    font.setPointSize(int(app_font["font-size"]) if "font-size" in app_font else 12)
                else:
                    font_units = app_font["font-units"]
                    try:
                        if font_units == "pt":
                            font.setPointSize(int(app_font["font-size"]) if "font-size" in app_font else 12)
                        elif font_units == "px":
                            font.setPixelSize(int(app_font["font-size"]) if "font-size" in app_font else 12)
                        else:
                            font.setPointSize(int(app_font["font-size"]) if "font-size" in app_font else 12)
                    except ValueError as err:
                        print(f"load_style: font_units : {err}", file=LOGGING_STREAM)
                application.setFont(font)
    except FileNotFoundError:
        print(f"No such file or directory: \"{style_src}\"")

