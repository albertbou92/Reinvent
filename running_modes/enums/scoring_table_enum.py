from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringTableEnum:

    AGENTS = "agent_priors"
    SCORES = "scores"
    SCORING_FUNCTIONS = "scoring_functions"
    COMPONENT_NAMES = "component_names"
