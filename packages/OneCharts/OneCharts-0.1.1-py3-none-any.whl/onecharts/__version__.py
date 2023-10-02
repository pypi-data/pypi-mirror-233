VERSION = (0, 1, 1)
PRERELEASE = None  # "alpha", "beta" or "rc"
REVISION = None


def generate_version():
    version_parts = [".".join(map(str, VERSION))]
    if PRERELEASE is not None:
        version_parts.append("-{}".format(PRERELEASE))
    if REVISION is not None:
        version_parts.append(".{}".format(REVISION))
    return "".join(version_parts)


__title__ = "OneCharts"
__description__ = "Create and Manage Charts with Ease"
__url__ = "https://github.com/onechartsio/onecharts-py"
__version__ = generate_version()
__license__ = "Apache License 2.0"
