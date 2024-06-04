from pic_scanner.models.of_interest import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('presets')


def make_all_exposed_genitalia_concerning(factory):
    """
    Make all exposed genitalia concerning.

    Parameters:
        factory (LabelFactory):
            The label factory.

    Returns:
        None
    """
    _name = 'make_all_exposed_genitalia_concerning'
    if not MOD_LOGGER.find_child_by_name(_name):
        log = MOD_LOGGER.get_child(_name)
    else:
        log = MOD_LOGGER.find_child_by_name(_name)

    _checked = []
    _found = []

    for name in factory.points_of_interest:
        log.debug(f'Checking {name}')

        if 'GENITALIA_EXPOSED' in name:
            log.debug(f'Making {name} concerning')
            factory.make_concerning(name)
            log.debug(f'{factory.concerns}')
            _found.append(name)

        _checked.append(name)
        log.debug(f'Checked {_checked}')
        log.debug(f'Found {_found}')

    return factory


def make_all_armpit_non_interesting(factory):
    """
    Make all armpit non-interesting.

    Parameters:
        factory (LabelFactory):
            The label factory.

    Returns:
        None
    """
    _name = 'make_all_armpit_non_interesting'
    if not MOD_LOGGER.find_child_by_name(_name):
        log = MOD_LOGGER.get_child(_name)
    else:
        log = MOD_LOGGER.find_child_by_name(_name)
    
    for name in factory.points_of_interest:
        if 'ARMPIT' in name:
            factory.make_non_interesting(name)

    return factory


def make_all_belly_non_interesting(factory):
    """
    Make all belly non-interesting.

    Parameters:
        factory (LabelFactory):
            The label factory.

    Returns:
        None
    """
    for name in factory.points_of_interest:
        if 'BELLY' in name:
            factory.make_non_interesting(name)

    return factory


def make_all_covered_non_interesting(factory):
    """
    Make all covered non-interesting.

    Parameters:
        factory (LabelFactory):
            The label factory.

    Returns:
        None
    """
    for name in factory.points_of_interest:
        if 'COVERED' in name:
            factory.make_non_interesting(name)

    return factory
