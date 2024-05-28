__all__ = [
        'AUTHORS',
        'RELEASE_MAP',
        'URLS',
        'VERSION',
        'PROG_DESC',
        'PROG_NAME'

        ]


PROG_DESC = 'A tool for scanning (and managing) images for NSFW content.'
"""The description of the program."""


PROG_NAME = 'IS-NSFW-Scanner'
"""The name of the program."""


URLS = dict(
    developer_url='https://inspyre.tech',
    docs_url='https://IS-NSFW-Scanner.readthedocs.io/en/latest',
    github_url='https://github.com/tayjaybabee/Inspyre-Toolbox',
    pypi_url='https://pypi.org/pypi/IS-NSFW-Scanner',
)
"""The URLs used in the project."""


AUTHORS = [
    ('Inspyre-Softworks', URLS['developer_url']),
    ('Taylor-Jayde Blackstone', '<t.blackstone@inspyre.tech>')
]
"""The authors of the project."""


RELEASE_MAP = {
    'dev': 'Development Build',
    'alpha': 'Alpha Build',
    'beta': 'Beta Build',
    'rc': 'Release Candidate Build',
    'final': 'Final Release Build'
}
"""The release map for the project."""


VERSION = {
    'major': 1,
    'minor': 0,
    'patch': 0,
    'release': 'dev',
    'release_num': 1
}
"""The version information for the project."""
