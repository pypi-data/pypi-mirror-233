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

if version.parse(tf.__version__) <= version.parse("2.12.0"):
    from tensorflow.python.framework.tensor_util import shape_tensor
else:
    from tensorflow.python.ops.shape_util import shape_tensor
