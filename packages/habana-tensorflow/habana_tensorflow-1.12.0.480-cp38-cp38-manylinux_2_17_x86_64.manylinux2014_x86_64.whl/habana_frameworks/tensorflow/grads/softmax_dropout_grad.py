###############################################################################
# Copyright (C) 2022 Habana Labs, Ltd. an Intel Company
###############################################################################
import tensorflow as tf
from tensorflow.python.framework import ops

def _register_grad(habana_ops):
    @ops.RegisterGradient("HabanaSoftmaxDropout")
    def _HabanaSoftmaxDropoutGrad(op, *grads):
        grad = habana_ops.habana_dropout_grad(x=grads[0], mask=op.outputs[1], ratio=tf.make_tensor_proto(op.get_attr('rate')))
        return habana_ops.habana_softmax_grad(y=op.outputs[2], dzdy=grad, axis=tf.make_tensor_proto(op.get_attr('axis')))
