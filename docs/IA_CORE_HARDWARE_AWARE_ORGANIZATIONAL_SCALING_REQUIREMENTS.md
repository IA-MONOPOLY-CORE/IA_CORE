# IA_CORE - Hardware-Aware Organizational Scaling Requirements

## Gate

`ROADMAP_3_0_A_N3_HARDWARE_ORGANIZATIONAL_SCALING_PASSED`

## Strategic shift

IA_CORE must evolve from model compatibility toward **organizational capacity
recommendation**. The question is not only “what model runs on this machine?”
but also “what organization can this machine sustain with acceptable quality?”

The future output is:

`HARDWARE_CAPACITY_PROFILE -> MAX_CONCURRENT_AGENT_CLASSES ->
RECOMMENDED_MODEL_TIERS -> RECOMMENDED_TEAM_SCALE -> IDEAL_BUSINESS_ORGANIZATION
-> RUNNABLE_BUSINESS_ORGANIZATION -> CONSTRAINTS -> UPGRADE/CLOUD_OPTIONS`.

## Three organization views

Every future recommendation must distinguish:

1. `IDEAL_ORGANIZATION`: the professional composition required by business
   complexity, workload, risk and objectives without current machine limits.
2. `MINIMUM_FUNCTIONAL_ORGANIZATION`: the smallest safe/useful composition that
   covers required functions without pretending to cover missing capability.
3. `HARDWARE_FITTED_ORGANIZATION`: the composition and execution schedule that
   current hardware, providers, privacy, budget and latency can sustain.

The system must never claim that a constrained computer can run an ideal
organization concurrently when the measured resources do not support it.

## Future capacity inputs

- RAM and available RAM;
- VRAM and available VRAM;
- CPU and GPU;
- storage and operating system;
- model size and quantization;
- context and reasoning need;
- agent count and team count;
- workload, frequency, latency and concurrency;
- provider/cloud availability;
- privacy, budget and local-only constraints.

The current `config/hardware_profile.json` and model recommendation code provide
model-level inputs and a limited local profile. They do not constitute this
organizational capacity engine.

## Scaling without silent quality loss

When hardware cannot run the ideal organization concurrently, quality should
not be silently reduced. Future strategies are lower concurrency, serialized
functions, safe blueprint/model reuse across turns, staged teams, on-demand role
activation, a minimum sufficient organization, or approved cloud/hybrid routing.

The user must see the difference between `ORGANIZATION_IDEAL` and
`ORGANIZATION_CURRENTLY_RUNNABLE`. A small machine may preserve all professional
functions by running fewer of them at a time; that is a capacity schedule, not
automatic loss of professional quality.

## Hierarchy and model tiers

Future recommendations may distinguish micro/execution agents, specialists,
supervisors, managers/directors and executive/strategic roles. Parameter counts
must not become a universal contract. Hardware, benchmarks, task and quality
criteria decide the smallest sufficient model without sacrificing required
quality.

No scheduler, runtime, concurrency engine, hardware detector, provider fallback
or organizational recommender is implemented by Roadmap 3.0.A.

