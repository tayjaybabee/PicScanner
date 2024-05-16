from dataclasses import dataclass


@dataclass
class Unit:
    unit_name: str
    unit_abbrev: str
    base_multiplier: int
    pluralize: str


__all__ = ['UNIT_MAP']


UNIT_MAP = {
    'B': Unit(unit_name='bytes', unit_abbrev='B', base_multiplier=1, pluralize='bytes'),
    'KB': Unit(unit_name='kilobytes', unit_abbrev='KB', base_multiplier=1024, pluralize='kilobytes'),
    'MB': Unit(unit_name='megabytes', unit_abbrev='MB', base_multiplier=1024**2, pluralize='megabytes'),
    'GB': Unit(unit_name='gigabytes', unit_abbrev='GB', base_multiplier=1024**3, pluralize='gigabytes'),
    'TB': Unit(unit_name='terabytes', unit_abbrev='TB', base_multiplier=1024**4, pluralize='terabytes'),
    'PB': Unit(unit_name='petabytes', unit_abbrev='PB', base_multiplier=1024**5, pluralize='petabytes'),
    'EB': Unit(unit_name='exabytes', unit_abbrev='EB', base_multiplier=1024**6, pluralize='exabytes'),
    'ZB': Unit(unit_name='zetabytes', unit_abbrev='ZB', base_multiplier=1024**7, pluralize='zetabytes'),
    'YB': Unit(unit_name='yottabytes', unit_abbrev='YB', base_multiplier=1024**8, pluralize='yottabytes')
}
"""
A dictionary mapping storage units to their respective data classes.
"""
