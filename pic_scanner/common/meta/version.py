from . import VERSION, RELEASE_MAP


def get_full_version_name() -> str:
    """
    Gets the full version name.

    Returns:
        str: The full version name.

    Since:
        v1.3.2
    """
    ver = parse_version()
    ver = ver.split('-')[0]

    release_type = RELEASE_MAP[VERSION["release"]]
    release_num = VERSION["release_num"]
    release_str = f" {release_type} {'' if VERSION['release'].lower() == 'final' else f'({release_num})'}"
    return f'v{ver}{release_str}'


def parse_version() -> str:
    """
    Parses the version information into a string.

    Returns:
        str: The version information.

    Since:
        v1.3.2
    """
    version = f'{VERSION["major"]}.{VERSION["minor"]}.{VERSION["patch"]}'

    if VERSION['release'] != 'final':
        version += f'-{VERSION["release"]}.{VERSION["release_num"]}'

    return version
