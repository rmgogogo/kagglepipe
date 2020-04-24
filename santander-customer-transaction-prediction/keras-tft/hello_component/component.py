from typing import Optional, Text
from hello_component import executor
from tfx import types
from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.types import channel_utils
from tfx.types import standard_artifacts
from tfx.types import artifact_utils
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter

class HelloComponentSpec(types.ComponentSpec):
  """ComponentSpec for Custom TFX Hello World Component."""

  PARAMETERS = {
  }

  INPUTS = {
      # This will be a dictionary with input artifacts, including URIs
      'input_data': ChannelParameter(type=standard_artifacts.Examples),
  }
  OUTPUTS = {
      # This will be a dictionary which this component will populate
      'output_data': ChannelParameter(type=standard_artifacts.Examples),
  }


class HelloComponent(base_component.BaseComponent):
  """Custom TFX Hello World Component.
  This custom component class consists of only a constructor.
  """

  SPEC_CLASS = HelloComponentSpec
  EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(executor.Executor)

  def __init__(self,
               input_data: types.Channel = None,
               output_data: Optional[types.Channel] = None,
               instance_name: Optional[Text] = None):
    """Construct a HelloComponent.
    Args:
      input_data: A Channel of type `standard_artifacts.Examples`. This will
        often contain two splits: 'train', and 'eval'.
      output_data: A Channel of type `standard_artifacts.Examples`. This will
        usually contain the same splits as input_data.
      instance_name: Optional unique name. Necessary if multiple Hello components are
        declared in the same pipeline.
    """
    # output_data will contain a list of Channels for each split of the data,
    # by default a 'train' split and an 'eval' split. Since HelloComponent
    # passes the input data through to output, the splits in output_data will
    # be the same as the splits in input_data, which were generated by the
    # upstream component.
    if not output_data:
      examples_artifact = standard_artifacts.Examples()
      examples_artifact.split_names = artifact_utils.get_single_instance(
          list(input_data.get())).split_names
      output_data = channel_utils.as_channel([examples_artifact])

    spec = HelloComponentSpec(input_data=input_data,
                              output_data=output_data)
    super(HelloComponent, self).__init__(spec=spec, instance_name=instance_name)