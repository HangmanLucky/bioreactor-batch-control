# I/O List — Bioreactor Environmental Control Unit

**Project:** Automated Bioreactor Environmental Control for Pharmaceutical Batch Processing
**Author:** Sipho Lucky Sibanda
**Target platform:** Siemens S7-1500 (TIA Portal / SCL) — portable to a CODESYS-based
pharmaceutical process controller

## Recipe Parameters (downloaded from SCADA/MES recipe management)

| Field                          | Description                              | Typical Value |
|-------------------------------------|---------------------------------------------|------------------|
| `SIP_Temp_Setpoint_C`                  | Sterilise-in-place temperature target           | 121.1 &deg;C         |
| `SIP_Target_F0_min`                      | Minimum accumulated sterilisation lethality         | 15.0 min               |
| `Cooldown_Temp_C`                          | Safe temperature before inoculation                    | 37.0 &deg;C                |
| `Incubation_Temp_Setpoint_C`                  | Culture temperature during incubation                     | 37.0 &deg;C                    |
| `Incubation_DO_Setpoint_Pct`                     | Dissolved oxygen target                                       | 40.0 %                          |
| `Incubation_pH_Setpoint`                            | Culture pH target                                                | 7.00                              |
| `Incubation_Duration_hr`                               | Planned incubation length                                          | 72.0 hr                            |
| `Harvest_OD_Threshold`                                    | Optical density that triggers early harvest                          | 8.0 OD                                |

## Inputs

| Tag Name                    | Description                                | Signal Type      | Range / Units       |
|---------------------------------|------------------------------------------------|--------------------|-------------------------|
| `AI_VesselTemp_C`                 | Bulk vessel temperature (RTD)                     | 4-20mA               | 0-140 &deg;C               |
| `AI_JacketTemp_C`                    | Heating/cooling jacket temperature                   | 4-20mA                 | 0-140 &deg;C                 |
| `AI_DO_Pct`                             | Dissolved oxygen probe                                  | 4-20mA                   | 0-100 %                       |
| `AI_pH`                                   | pH probe                                                  | 4-20mA                     | 0-14                            |
| `AI_OpticalDensity`                          | Cell density probe (OD600 or equivalent)                    | 4-20mA                       | 0-20 OD                           |
| `AI_AgitatorSpeed_RPM`                          | Agitator speed feedback                                       | 4-20mA                         | 0-500 RPM                           |
| `DI_CIP_Complete`                                  | Clean-in-place skid reports its sequence complete                | Digital (24VDC)                   | 0/1                                    |
| `DI_StartBatch`                                       | Operator/SCADA batch start command                                  | Digital (24VDC)                     | 0/1                                      |
| `DI_AbortBatch`                                          | Batch abort command                                                    | Digital (24VDC)                       | 0/1                                        |
| `DI_System_Enable`                                          | Master enable                                                            | Digital (24VDC)                         | 0/1                                          |

## Outputs

| Tag Name                       | Description                              | Signal Type      |
|-------------------------------------|------------------------------------------------|--------------------|
| `AO_JacketTempSetpoint_C`             | Cascade outer loop output (inner loop's setpoint)   | Internal / trend tag |
| `AO_HeatingValve_Pct` / `AO_CoolingValve_Pct` | Jacket heating/cooling valve position   | 4-20mA x2 |
| `AO_AgitatorSpeed_RPM`                   | Agitator speed command (split-range primary)          | 4-20mA |
| `AO_O2SpargeValve_Pct`                      | Oxygen sparge valve (split-range secondary)              | 4-20mA |
| `DO_AcidPump` / `DO_BasePump`                  | pH dosing pumps                                             | Digital x2 |
| `BatchPhase`                                       | Current ISA-88 style phase (enumeration)                       | Internal / HMI tag |
| `Current_F0_min`                                      | Accumulated sterilisation lethality                               | REAL, HMI trend |
| `BatchElapsed_hr`                                        | Elapsed incubation time                                              | REAL, HMI trend |
| `Alarm_SIP_Failed` / `Alarm_DO_Low` / `Alarm_pH_Excursion` / `Alarm_TempDeviation` | Process alarms | Digital x4 |
| `SystemStatus`                                                 | Human-readable status text                                              | STRING |

## Notes for reviewers

- **F0 accumulation** only runs during the SIP phase and resets to zero when a new batch's
  CIP phase begins — it is a per-batch sterilisation record, consistent with how a real
  batch record would need to document sterilisation lethality for that specific run.
- **Split-range DO control** intentionally exhausts agitation authority (0-70% of
  controller output) before opening the oxygen sparge valve at all — see the project
  manual, Chapter 5, for why that specific order (not the reverse) matters both for cost
  and for shear-sensitive cell cultures.
- The **inoculation phase** in this simplified model advances on a settle timer rather
  than a fully sequenced transfer step — a real recipe would sequence valve alignments,
  a transfer pump, and a confirmed volume addition here. See the project manual's
  limitations chapter.
