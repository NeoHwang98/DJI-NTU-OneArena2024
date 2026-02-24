# Contributing

## Workflow

1. Create a feature branch from `main`.
2. Keep changes small and scoped (firmware, route script, docs).
3. Open a pull request with:
   - what changed
   - why it changed
   - how it was tested

## Code Guidelines

- Keep calibration constants explicit and easy to tune.
- Add short comments only where route logic is non-obvious.
- Avoid hard-coding behavior without documenting marker ID assumptions.

## Testing Checklist

- Python (RoboMaster): validate route transitions, marker detection behavior, pickup/drop flow.
- Arduino: validate IR trigger, motor direction, and ultrasonic stopping thresholds.
- Safety: test at reduced speed before full-speed runs.
