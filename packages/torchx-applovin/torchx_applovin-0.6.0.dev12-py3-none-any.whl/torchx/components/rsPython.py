import os

import torchx
import torchx.specs as specs

from typing import Dict, List, Optional

def rsPython(
    script: Optional[str] = None,
    image: str = torchx.IMAGE,
    num_replicas: int = 1,
    cpu: int = 1,
    gpu: int = 0,
    memMB: int = 1024,
    h: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    max_retries: int = 0,
    mounts: Optional[List[str]] = None,
) -> specs.AppDef:
    """
    Args:
        args: bash arguments
        image: image to use
        num_replicas: number of replicas to run
        cpu: number of cpus per replica
        gpu: number of gpus per replica
        memMB: cpu memory in MB per replica
        h: a registered named resource (if specified takes precedence over cpu, gpu, memMB)
        env: environment varibles to be passed to the run (e.g. ENV1=v1,ENV2=v2,ENV3=v3)
        max_retries: the number of scheduler retries allowed
        mounts: mounts to mount into the worker environment/container (ex. type=<bind/volume>,src=/host,dst=/job[,readonly]).
                See scheduler documentation for more info.
    """

    if env is None:
        env = {}
    env.setdefault("LOGLEVEL", os.getenv("LOGLEVEL", "WARNING"))

    return specs.AppDef(
        name="rsPython",
        roles=[
            specs.Role(
                name="rsPython",
                image=image,
                entrypoint="sh",
                args=[
                    "source", "env/bin/activate",
                    "&&", "python3.11", script
                ],
                num_replicas=num_replicas,
                resource=specs.resource(cpu=cpu, gpu=gpu, memMB=memMB, h=h),
                env=env,
                max_retries=max_retries,
                mounts=specs.parse_mounts(mounts) if mounts else [],
            )
        ],
    )
