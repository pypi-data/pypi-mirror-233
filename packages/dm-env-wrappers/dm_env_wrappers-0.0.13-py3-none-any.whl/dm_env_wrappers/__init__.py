"""dm_env_wrappers: A collection of wrappers for dm_env environments."""

from dm_env_wrappers._src.action_repeat import ActionRepeatWrapper
from dm_env_wrappers._src.base import EnvironmentWrapper, wrap_all
from dm_env_wrappers._src.canonical_spec import CanonicalSpecWrapper
from dm_env_wrappers._src.concatenate_observations import ConcatObservationWrapper
from dm_env_wrappers._src.episode_statistics import EpisodeStatisticsWrapper
from dm_env_wrappers._src.expand_scalar_observation_shapes import (
    ExpandScalarObservationShapesWrapper,
)
from dm_env_wrappers._src.frame_stacking import FrameStackingWrapper
from dm_env_wrappers._src.mujoco.dm_control_video import DmControlVideoWrapper
from dm_env_wrappers._src.mujoco.dm_control import DmControlWrapper
from dm_env_wrappers._src.mujoco.action_noise import ActionNoiseWrapper
from dm_env_wrappers._src.mujoco.action_smoother import ActionSmootherWrapper
from dm_env_wrappers._src.observation_action_reward import (
    ObservationActionRewardWrapper,
)
from dm_env_wrappers._src.single_precision import SinglePrecisionWrapper
from dm_env_wrappers._src.step_limit import StepLimitWrapper
from dm_env_wrappers._src.validate_spec import ValidateActionSpecWrapper
from dm_env_wrappers._src.video import VideoWrapper

from dm_env_wrappers._src import lazy_loader

with lazy_loader.LazyImports(__name__, False):
    from dm_env_wrappers._src.gymnasium_wrapper import GymnasiumWrapper
    from dm_env_wrappers._src.gym_wrapper import GymWrapper

del lazy_loader  # lazy_loader should not be exported

__version__ = "0.0.13"

__all__ = (
    "ActionNoiseWrapper",
    "ActionRepeatWrapper",
    "ActionSmootherWrapper",
    "CanonicalSpecWrapper",
    "ConcatObservationWrapper",
    "DmControlWrapper",
    "DmControlVideoWrapper",
    "EnvironmentWrapper",
    "EpisodeStatisticsWrapper",
    "ExpandScalarObservationShapesWrapper",
    "FrameStackingWrapper",
    "GymnasiumWrapper",
    "GymWrapper",
    "ObservationActionRewardWrapper",
    "SinglePrecisionWrapper",
    "StepLimitWrapper",
    "ValidateActionSpecWrapper",
    "VideoWrapper",
    "wrap_all",
)

#  _________________________________________
# / Please don't use symbols in `_src` they \
# \ are not part of the public API.         /
#  -----------------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||
#
