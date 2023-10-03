import os

import torchx
from torchx.util.gpuCascading import generateCascadingAffinityAndTolerationsGPU
import torchx.specs as specs

from typing import Dict, List, Optional

from kubernetes.client.models import (
    V1Affinity,
    V1Toleration,
    V1NodeAffinity,
    V1PreferredSchedulingTerm,
    V1NodeSelectorTerm,
    V1NodeSelectorRequirement,
)

def rsPython(
    script: Optional[str] = None,
    image: str = torchx.IMAGE,
    num_replicas: int = 1,
    cpu: int = 1,
    gpu: int = 0,
    gpu_type: Optional[str] = "cascading",
    memMB: int = 1024,
    h: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    max_retries: int = 0,
    mounts: Optional[List[str]] = None,
) -> specs.AppDef:
    """
    Args:
        script: python script to run
        image: image to use
        num_replicas: number of replicas to run
        cpu: number of cpus per replica
        gpu: number of gpus per replica

        gpu_type: type of gpu to use (a100, t4, l4, cascading)

        memMB: cpu memory in MB per replica
        h: a registered named resource (if specified takes precedence over cpu, gpu, memMB)
        env: environment varibles to be passed to the run (e.g. ENV1=v1,ENV2=v2,ENV3=v3)
        max_retries: the number of scheduler retries allowed
        mounts: mounts to mount into the worker environment/container (ex. type=<bind/volume>,src=/host,dst=/job[,readonly]).
                See scheduler documentation for more info.
    """

    gpu_settings = {
        "t4": {
            "label": "biddermlgpu-t4-node-pool",
            "weight": 1
        },

        "a100": {
            "label": "biddermlgpu-node-pool",
            "weight": 100
        },

        "l4": {
            "label": "biddermlgpu-l4-node-pool",
            "weight": 50
        },
    }

    if gpu_type not in gpu_settings.keys() and gpu_type != "cascading" and gpu_type != "":
        raise ValueError("invalid gpu_type")


    if gpu_type == "cascading":
        tolerations, affinity = generateCascadingAffinityAndTolerationsGPU(gpu_settings)

    elif gpu_type in gpu_settings.keys():
        affinity = {
            "node_selector": {
                "node_pool": gpu_settings[gpu_type]["label"]
            }
        }

        tolerations = [
            V1Toleration(
                effect="NoSchedule",
                key="nvidia.com/gpu",
                operator="Equal",
                value="present"
            ),
        ]

    capabilities = {
        "affinity": affinity,
        "tolerations": tolerations,
    }

    # if h is not None:
    #     h.

    if env is None:
        env = {}

    env.setdefault("LOGLEVEL", os.getenv("LOGLEVEL", "WARNING"))

    return specs.AppDef(
        name="rsPython",
        roles=[
            specs.Role(
                name="rsPython",
                image=image,
                entrypoint="/bin/bash",
                args=[
                    "-c",
                    f'source /app/env/bin/activate && python3.11 {script}'
                ],
                num_replicas=num_replicas,
                resource=specs.resource(cpu=cpu, gpu=gpu, memMB=memMB, h=h),
                env=env,
                max_retries=max_retries,
                mounts=specs.parse_mounts(mounts) if mounts else [],
            )
        ],
    )
