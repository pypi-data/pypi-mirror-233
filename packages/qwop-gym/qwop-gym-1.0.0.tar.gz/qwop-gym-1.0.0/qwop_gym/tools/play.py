# =============================================================================
# Copyright 2023 Simeon Manolov <s.manolloff@gmail.com>.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import os
import time
import gymnasium as gym
import gymnasium.utils.play

from . import common


def play(seed, run_id, fps):
    env = gym.make("local/QWOP-v1", seed=seed)
    rec_file = None

    try:
        # Unfortunately, this will immediately reset on termination
        # (gym.utils.play() does not allow control over this)
        gym.utils.play.play(env, fps=fps)
    finally:
        env.close()
