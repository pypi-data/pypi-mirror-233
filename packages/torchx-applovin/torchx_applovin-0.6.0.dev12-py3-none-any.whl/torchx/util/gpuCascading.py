#!/usr/bin/env python3

from typing import Dict, List, Any, Optional

from kubernetes.client.models import (
    V1Affinity,
    V1Toleration,
    V1NodeAffinity,
    V1PreferredSchedulingTerm,
    V1NodeSelectorTerm,
    V1NodeSelectorRequirement,
)

def generateCascadingAffinityAndTolerationsGPU(gpu_settings: Dict[str, Dict[str, Any]]):
    tolerations = [
        V1Toleration(
            operator='Equal',
            value='true',
            effect='NoSchedule',
            key=gpu_values["label"],
        )
        for _, gpu_values in gpu_settings.items()
    ]

    tolerations.append(
        V1Toleration(
            operator='Equal',
            value='present',
            effect='NoSchedule',
            key='nvidia.com/gpu'
        )
    )

    affinity = V1Affinity(
        node_affinity=V1NodeAffinity(
            preferred_during_scheduling_ignored_during_execution=[
                V1PreferredSchedulingTerm(

                    weight=gpu_values["weight"],

                    preference=V1NodeSelectorTerm(
                        match_expressions=[
                            V1NodeSelectorRequirement(
                                key="node_pool",
                                operator="In",
                                values=[gpu_values["label"]],
                            )
                        ]
                    ),

                ) for _, gpu_values in gpu_settings.items()
            ]
        )
    )

    return tolerations, affinity
