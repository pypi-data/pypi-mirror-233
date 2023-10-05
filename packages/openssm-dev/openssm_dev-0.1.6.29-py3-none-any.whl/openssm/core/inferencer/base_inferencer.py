"""Base inferencer."""


from openssm.core.inferencer.abstract_inferencer import AbstractInferencer


class BaseInferencer(AbstractInferencer):
    """Base inferencer."""

    def predict(self, input_data: dict) -> dict:
        """
        The BaseInferencer always returns a prediction of True.
        """
        assert input_data is not None
        return {"prediction": True}

    def load(self, path: str):
        """
        The BaseInferencer does not need to load anything.
        """
        pass
