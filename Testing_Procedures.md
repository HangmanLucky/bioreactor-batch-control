# Functional Test Procedure — Bioreactor Batch Control

**Project:** Automated Bioreactor Environmental Control Unit
**Document type:** Factory Acceptance Test (FAT) — simulated / desktop validation
**Author:** Sipho Lucky Sibanda

| # | Test Case | Precondition | Action | Expected Result | Pass/Fail |
|---|------------|----------------|---------|--------------------|-------------|
| 1 | Batch start sequences into CIP | System enabled, phase IDLE | Pulse `DI_StartBatch` | `BatchPhase` &rarr; PH_CIP | |
| 2 | CIP complete advances to SIP | Phase CIP | Force `DI_CIP_Complete = TRUE` | `BatchPhase` &rarr; PH_SIP; `Current_F0_min` resets to 0 at CIP entry | |
| 3 | F0 accumulates correctly at reference temperature | Phase SIP, `AI_VesselTemp_C = 121.1` | Wait 60 simulated seconds | `Current_F0_min` increases by ~1.0 min (10^0 = 1.0 lethality rate at the reference temp) | |
| 4 | F0 accumulates faster above reference temperature | Phase SIP, `AI_VesselTemp_C = 131.1` | Observe accumulation rate | Rate is 10x faster than Test 3 (one z-value, 10&deg;C, above reference) | |
| 5 | SIP completes on F0 target, not on time or temperature alone | Phase SIP | Wait until `Current_F0_min >= Recipe.SIP_Target_F0_min` | `BatchPhase` &rarr; PH_COOLDOWN, regardless of elapsed time | |
| 6 | Cascade temperature control | Phase SIP or Incubation | Step `AI_VesselTemp_C` below setpoint | `AO_JacketTempSetpoint_C` rises; `AO_HeatingValve_Pct` responds once jacket temp lags | |
| 7 | Cooldown confirmation requires a stable hold | Phase COOLDOWN | Let vessel temp settle within 1&deg;C of target, hold 5 minutes | `BatchPhase` &rarr; PH_INOCULATION only after the full confirm timer, not on first touch | |
| 8 | DO split-range: agitation only | Phase INCUBATION, DO controller output &le;70% | Observe | `AO_AgitatorSpeed_RPM` scales with output; `AO_O2SpargeValve_Pct = 0` | |
| 9 | DO split-range: sparge engages | Phase INCUBATION, DO controller output &gt;70% | Observe | `AO_AgitatorSpeed_RPM` pinned at max; `AO_O2SpargeValve_Pct` scales with the remaining output | |
| 10 | pH deadband prevents dosing chatter | Phase INCUBATION, pH within &plusmn;0.10 of setpoint | Observe | Both `DO_AcidPump` and `DO_BasePump` remain FALSE | |
| 11 | pH excursion alarm | Phase INCUBATION | Force `AI_pH` more than 0.5 from setpoint | `Alarm_pH_Excursion = TRUE` | |
| 12 | Early harvest on optical density | Phase INCUBATION | Force `AI_OpticalDensity >= Recipe.Harvest_OD_Threshold` | `BatchPhase` &rarr; PH_HARVEST before the incubation timer expires | |
| 13 | Abort forces a safe state | Any active phase | Force `DI_AbortBatch = TRUE` | `BatchPhase` &rarr; PH_ABORT; cooling valve to 100%, agitator/sparge/dosing all off | |
| 14 | Aborted SIP is flagged, not silently accepted | Phase SIP, F0 below target | Force `DI_AbortBatch = TRUE` | `Alarm_SIP_Failed = TRUE` - the batch record shows sterilisation was never actually achieved | |

## Why Test 14 matters as much as Test 5

Test 5 proves the happy path: SIP genuinely completes once enough lethality has been
accumulated. Test 14 proves the system never lets an aborted, under-sterilised batch look
the same as a properly completed one — `Alarm_SIP_Failed` exists specifically so a batch
record can never ambiguously suggest a vessel was safe to inoculate when it wasn't.

## How to exercise these tests without physical hardware

As with the rest of this portfolio, these cases were run by forcing input tags in a
PLCSIM-style watch table (or an equivalent CODESYS soft-PLC harness), stepping simulated
temperature and time values to exercise the F0 integration and cascade loops across a
realistic range rather than only at single fixed points.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Test performed by | Sipho Lucky Sibanda | |
| Reviewed by | | |
