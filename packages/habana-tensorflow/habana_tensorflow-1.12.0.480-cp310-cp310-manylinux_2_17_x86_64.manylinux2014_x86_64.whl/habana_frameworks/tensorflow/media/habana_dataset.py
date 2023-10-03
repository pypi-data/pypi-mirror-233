###############################################################################
# Copyright (C) 2023 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################
from packaging import version
import tensorflow as tf

if version.parse(tf.__version__) < version.parse("2.13.0"):
    from habana_frameworks.tensorflow.media.tf_ver.v2_12_0.habana_dataset import HabanaDataset
else:
    from habana_frameworks.tensorflow.media.tf_ver.v2_13_0.habana_dataset import HabanaDataset
