AZURE_01_MINI = "o1-mini"
AZURE_03_MINI = "o3-mini"
AZURE_04_MINI = "o4-mini"
AZURE_03_PRO = "o3-pro"
AZURE_O3_DEEP_RESEARCH = "o3-deep-research"

PROVIDER_AZURE = {
    AZURE_03_PRO: {
        "version": "2025-04-01-preview",
        "deployment_name": AZURE_03_PRO
    },
    AZURE_03_MINI: {
        "version": "2025-04-01-preview",
        "deployment_name": AZURE_03_MINI
    },
    AZURE_04_MINI: {
        "version": "2025-04-01-preview",
        "deployment_name": AZURE_04_MINI
    },
    AZURE_01_MINI: {
        "version": "2025-04-01-preview",
        "deployment_name": AZURE_04_MINI

    }
}

OPENAI_03 = "o3-deep-research"
OPENAI_04_MINI = "o4-mini-deep-research-2025-06-26"

PROVIDER_OPENAI = {
    OPENAI_03: {
        "deployment_name": OPENAI_03
    },
    OPENAI_04_MINI: {
        "deployment_name": OPENAI_04_MINI
    }
}
