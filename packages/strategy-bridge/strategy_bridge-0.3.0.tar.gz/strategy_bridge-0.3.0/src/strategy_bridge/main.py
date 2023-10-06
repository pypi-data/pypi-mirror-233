from strategy_bridge.common import config
from strategy_bridge.processors import VisionDetectionsCollector, RobotCommandsSender
from strategy_bridge.processors.python_controller_template import PythonControllerTemplate
from strategy_bridge.processors.referee_commands_collector import RefereeCommandsCollector
from strategy_bridge.processors.vision_combiner import VisionCombiner
from strategy_bridge.runner import Runner


if __name__ == '__main__':

    config.init_logging()

    # TODO: Move list of processors to config
    processors = [
        VisionDetectionsCollector(processing_pause=0.01),
        # VisionCombiner(processing_pause=1)
        RefereeCommandsCollector(processing_pause=0.01),
        PythonControllerTemplate(processing_pause=0.2, reduce_pause_on_process_time=True),
        RobotCommandsSender(processing_pause=0.01)
    ]

    runner = Runner(processors=processors)
    runner.run()
