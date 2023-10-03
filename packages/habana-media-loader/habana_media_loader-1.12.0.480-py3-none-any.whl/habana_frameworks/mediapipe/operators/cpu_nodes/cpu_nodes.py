from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
from habana_frameworks.mediapipe.operators.media_nodes import MediaConstantNode
from habana_frameworks.mediapipe.operators.media_nodes import MediaFuncDataNode
from habana_frameworks.mediapipe.operators.media_nodes import MediaDummyNode
from habana_frameworks.mediapipe.operators.media_nodes import MediaCPUNode
from habana_frameworks.mediapipe.backend.utils import get_str_dtype
from habana_frameworks.mediapipe.media_types import dtype as dt
from abc import ABC, abstractmethod
import numpy as np
import inspect
import copy


class media_dummy(MediaDummyNode):
    """
    Class defining media dummy node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(name, None, device, inputs,
                         params, cparams, node_attr)

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        pass

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        return opnode_tensor_info(dt.NDT,
                                  np.array([0], dtype=np.uint32),
                                  "")

    def __call__(self):
        """
        Callable class method.

        """
        return None


class media_constants(MediaConstantNode):
    """
    Class defining media constant node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(name, None, device, inputs,
                         params, cparams, node_attr)
        self.params = copy.deepcopy(params)
        self.out_tensor_info = []
        for i in range(len(node_attr)):
            dtype = get_str_dtype(node_attr[i]['outputType'])
            o = opnode_tensor_info(dtype,
                                   np.array(self.params['shape'],
                                            dtype=np.uint32),
                                   "")
            self.out_tensor_info.append(o)

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        pass

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        return self.out_tensor_info

    def __call__(self):
        """
        Callable class method.

        """
        return self.params['data']


class media_func_data(MediaFuncDataNode):
    """
    Class defining media function node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(name, None, device, inputs,
                         params, cparams, node_attr)
        self.params = copy.deepcopy(params)
        self.dtype = get_str_dtype(node_attr[0]['outputType'])
        self.params['dtype'] = self.dtype
        self.params['unique_number'] = self.counter
        spec = inspect.getargspec(self.params['func'])
        if(len(spec.args) != 2):
            msg = "{} constructor must take two arguments".format(
                str(self.params['func']))
            raise RuntimeError(msg)
        self.func_obj = self.params['func'](self.params)
        if(not isinstance(self.func_obj, media_function)):
            print(isinstance(self.func_obj, media_function))
            raise ValueError(
                "Tensor node function must be of type TensorFunctionNode")
        spec = inspect.getargspec(self.func_obj)
        if((len(spec.args) - 1) != len(inputs)):
            msg = "{} callable entity must take {} arguments".format(
                str(self.params['func']), len(inputs)+1)
            raise RuntimeError(msg)

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        pass

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        return opnode_tensor_info(self.dtype, np.array(
            self.params['shape'], dtype=np.uint32), "")

    def __call__(self, *argv):
        """
        Callable class method.

        :params *argv: list of inputs to this node.
        """
        return self.func_obj(*argv)


class media_function(ABC):
    """
    Abstract class representing media function node.

    """
    @abstractmethod
    def __init__(self, params):
        """
        Abstract constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        pass

    @abstractmethod
    def __call__(self, *argv):
        """
        Callable class method.

        """
        pass


class media_ext_cpu_op(MediaCPUNode):
    """
    Class representing media external cpu node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(name, None, device, inputs,
                         params, cparams, node_attr)
        self.params = copy.deepcopy(params)
        self.params['unique_number'] = self.counter
        spec = inspect.getargspec(self.params['impl'])
        if(len(spec.args) != 2):
            msg = "{} constructor must take two arguments".format(
                str(self.params['impl']))
            raise RuntimeError(msg)
        self.impl_obj = self.params['impl'](self.params)
        if(not isinstance(self.impl_obj, media_ext_cpu_op_impl)):
            print(isinstance(self.impl_obj, media_ext_cpu_op_impl))
            raise ValueError(
                "Tensor node function must be of type TensorFunctionNode")
        spec = inspect.getargspec(self.impl_obj)
        if((len(spec.args) - 1) != len(inputs)):
            msg = "{} callable entity must take {} arguments".format(
                str(self.params['impl']), len(inputs)+1)
            raise RuntimeError(msg)

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        p = media_ext_cpu_op_params(params.batch_size)
        self.impl_obj.set_params(p)

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        out_tensor_info = self.impl_obj.gen_output_info()
        if(out_tensor_info == None):
            raise ValueError(
                "out tensor info of node {} is None".format(self.opname))
        if(not isinstance(out_tensor_info, list)):
            out_tensor_info = [out_tensor_info]
        if(len(out_tensor_info) != len(self.output_tensors)):
            raise ValueError(
                "out info incomplete for node {}".format(self.opname))
        output_info = []
        for o in out_tensor_info:
            if(not isinstance(o, media_ext_cpu_op_tensor_info)):
                raise ValueError(
                    "operator {}  return output info is not opnode_tensor_info type".format(self.opname))
            oti = opnode_tensor_info(o.dtype, o.shape, o.layout)
            output_info.append(oti)
        return output_info

    def __call__(self, *argv):
        """
        Callable class method.

        :params *argv: list of inputs to this node.
        """
        return self.impl_obj(*argv)


class media_ext_cpu_op_impl(ABC):
    """
    Abstract class representing external cpu node.

    """
    @abstractmethod
    def __init__(self, params):
        """
        Abstract constructor method.

        :params params: private params of this node
        """
        pass

    @abstractmethod
    def __call__(self, *argv):
        """
        Abstract callable class method.

        :params *argv: list of inputs to this node.
        """
        pass

    @abstractmethod
    def set_params(self, params):
        """
        Abstract setter method to set mediapipe specific params.

        :params params: mediapipe params of type "media_ext_cpu_op_params".
        """
        pass

    @abstractmethod
    def gen_output_info(self):
        """
        Abstract method to generate output type information.

        :returns : output tensor information of type "media_ext_cpu_op_tensor_info".
        """

        pass


class media_ext_cpu_op_params(object):
    """
    Class defining param information sent to external cpu op class.

    """

    def __init__(self, batch_size):
        """
        Constructor method.

        :params batch_size: Batch size.
        """
        self.batch_size = batch_size


class media_ext_cpu_op_tensor_info(object):
    """
    Class defining return numpy tensor information of external cpu op class.

    """

    def __init__(self, dtype, shape, layout):
        """
        Constructor method.

        :params dtype: output data type.
        :params shape: output shape.
        :params layout: output layout.
        """
        self.dtype = dtype
        self.shape = shape
        self.layout = layout
