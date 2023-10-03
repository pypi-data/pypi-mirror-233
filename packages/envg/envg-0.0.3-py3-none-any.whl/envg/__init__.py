"""envg environment package."""
from envg import default, env, main, misc, osrelease, secrets, system
from envg.default import *  # noqa: F403
from envg.env import *  # noqa: F403
from envg.main import *  # noqa: F403
from envg.misc import *  # noqa: F403
from envg.osrelease import *  # noqa: F403
from envg.secrets import *  # noqa: F403
from envg.system import *  # noqa: F403

__all__ = (
    default.__all__
    + env.__all__
    + main.__all__
    + misc.__all__
    + osrelease.__all__
    + secrets.__all__
    + system.__all__
)

# TODO: parcheo esto con el python-decouple que lea antes el .env
