from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class MethodCalculationMethod(Enum):
    """
    Configuration for metric calculation method.

    """
    AVERAGE = "AVERAGE"

    def __str__(self):
        return self.value


@dataclass
class MetricCalculatorConfig:
    """
    Configuration for metric calculation.
    """
    method: MethodCalculationMethod

    def asdict(self) -> Dict[str, Any]:
        return {"method": str(self.method)}


class MatchingTechnique(Enum):
    FUZZY_MATCH = "fuzzy_match"
    JSON_VALIDATOR = "json_validator"
    INCLUDES = "includes"
    MATCH = "match"

    def __str__(self):
        return self.value


class EvaluatorType(Enum):
    INDIVIDUAL = "individual"
    COMPARISON = "comparison"
    ALL = "all"

    def __str__(self):
        return self.value


@dataclass
class BaseEvaluatorConfig:
    """
    Base configuration for evaluators.
    """
    name: str
    evaluator_type: EvaluatorType

    def asdict(self) -> Dict[str, Any]:
        return {"name": self.name, "evaluator_type": str(self.evaluator_type)}


@dataclass
class EvaluatorConfig(BaseEvaluatorConfig):
    """
    Configuration for custom evaluator.
    """
    metric_calculators: List[MetricCalculatorConfig] = field(
        default_factory=list
    )
    evaluator_type = EvaluatorType.INDIVIDUAL

    def asdict(self) -> Dict[str, Any]:
        base_dict = super().asdict()
        base_dict["metric_calculators"] = [
            mc.asdict() for mc in self.metric_calculators
        ]
        return base_dict


@dataclass
class ComparisonEvaluatorConfig(BaseEvaluatorConfig):
    """
    Configuration for evaluators that compare different outputs.
    """
    metric_calculators: List[MetricCalculatorConfig] = field(
        default_factory=list
    )
    evaluator_type = EvaluatorType.COMPARISON


@dataclass
class GlobalEvaluatorConfig(BaseEvaluatorConfig):
    """
    Configuration for evaluators that compare based on all outputs.
    """
    metric_calculators: List[MetricCalculatorConfig] = field(
        default_factory=list
    )
    evaluator_type = EvaluatorType.ALL


@dataclass
class ExpectedResultEvaluatorConfig(EvaluatorConfig):
    matching_technique: MatchingTechnique = MatchingTechnique.MATCH


@dataclass
class OpenAIEloEvaluatorConfig(GlobalEvaluatorConfig):
    openai_model_name: str = "gpt-4"
    input_description: str = "This is a description."


@dataclass
class EvaluatorOutput:
    """
    Result of an evaluator.
    """

    name: str
    result: Any
    metric_calculators: List[MetricCalculatorConfig] = field(
        default_factory=list
    )

    def asdict(self) -> Dict[str, Any]:
        return {
            "name":
            self.name,
            "result":
            self.result,
            "metric_calculators": [
                mc.asdict() if hasattr(mc, 'asdict') else mc
                for mc in self.metric_calculators
            ]
        }