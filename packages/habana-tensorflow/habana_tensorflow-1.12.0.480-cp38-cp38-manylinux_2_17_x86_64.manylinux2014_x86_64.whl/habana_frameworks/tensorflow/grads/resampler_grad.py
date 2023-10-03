###############################################################################
# Copyright (C) 2022 Habana Labs, Ltd. an Intel Company
###############################################################################
from tensorflow.python.framework import ops


def _register_grad(habana_ops):
    @ops.RegisterGradient("HabanaResampler")
    def _HabanaResamplerGrad(op, *grads):
        return habana_ops.habana_resampler_grad(
            data=op.inputs[0],
            warp=op.inputs[1],
            grad_output=grads[0])
