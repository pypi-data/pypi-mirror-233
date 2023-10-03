from torchx.specs import Resource

from torchx.util.gpuCascading import generateCascadingAffinityAndTolerationsGPU

from kubernetes.client.models import (
    V1Affinity,
    V1Toleration,
    V1NodeAffinity,
    V1PreferredSchedulingTerm,
    V1NodeSelectorTerm,
    V1NodeSelectorRequirement,
)

# t-shirt sizes

def cascadingGPU() -> Resource:
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

    tolerations, affinity = generateCascadingAffinityAndTolerationsGPU(gpu_settings)

    capabilities = {
        "affinity": affinity,
        "tolerations": tolerations,
    }

    return Resource(cpu=2,  gpu=4, memMB=10000, capabilities=capabilities)

def t4() -> Resource:
    capabilities = {
        "node_selector": {
            "node_pool": "biddermlgpu-t4-node-pool"
        },
    }

    return Resource(cpu=2,  gpu=4, memMB=10000, capabilities=capabilities)


def l4() -> Resource:
    capabilities = {
        "node_selector": {
            "node_pool": "biddermlgpu-l4-node-pool"
        },
    }

    return Resource(cpu=2,  gpu=4, memMB=10000, capabilities=capabilities)



def a100() -> Resource:
    capabilities = {
        "node_selector": {
            "node_pool": "biddermlgpu-node-pool"
        },
    }

    return Resource(cpu=2,  gpu=4, memMB=10000, capabilities=capabilities)
