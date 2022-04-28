import io_helper
import helper

class kNN_CLASSIFIER(helper.CLASSIFIER):
    def __init__(self):
        super().__init__()

    def read_input(self) -> list:
        assert helper.CONSTANTS.ATTR_CT == -1
        assert helper.CONSTANTS.TRAIN is not None and helper.CONSTANTS.TEST is not None
        assert type(helper.CONSTANTS.TRAIN) == list and type(helper.CONSTANTS.TEST) == list

        helper.CONSTANTS.ATTR_CT = len(helper.CONSTANTS.TRAIN[0]) - 1
        io_helper.print_func(f"predictive attribute count: {helper.CONSTANTS.ATTR_CT}")