(*
====================================================================================
  PROJECT   : Automated Bioreactor Environmental Control Unit
              for Pharmaceutical Batch Processing
  MODULE    : FB_Bioreactor_BatchControl
  PLATFORM  : IEC 61131-3 Structured Text
              Written against Siemens SCL (TIA Portal, S7-1500) syntax,
              portable to CODESYS-based pharmaceutical process controllers.
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : Producing a biologic drug substance (or vaccine intermediate)
              means holding a living cell culture inside a precise,
              validated environment for days, after first proving the
              vessel itself was sterilised beyond any reasonable doubt.
              This function block sequences a full batch through the
              ISA-88 style phases a real biopharma batch record follows:
              CIP -> SIP (sterilisation) -> Cooldown -> Inoculation ->
              Incubation -> Harvest - and runs the cascade and
              split-range control loops that hold temperature, dissolved
              oxygen, and pH inside spec throughout.

  ENGINEERING BASIS (simulated against, for realism only):
    - ISA-88 (IEC 61512) batch control model: recipes, phases, and
      equipment procedures as the standard structure for batch
      pharmaceutical/biotech manufacturing control.
    - Cascade control: an outer (master) loop's output becomes the
      setpoint for an inner (slave) loop, which reacts to disturbances
      far faster than the outer loop alone ever could.
    - Split-range control: dissolved oxygen is defended first by
      increasing agitation (fast, cheap), and only escalates to
      supplemental oxygen sparging once agitation is maxed out.
    - F0 lethality (a real sterilisation-validation concept): the
      standard formula F0 = sum(10^((T-121.1)/z) * dt), z=10, integrates
      how much sterilising "credit" a batch has actually accumulated,
      because sterilisation is temperature AND time dependent - holding
      110C for an hour is not equivalent to 121C for six minutes, and
      F0 is the industry-standard way of comparing the two on one scale.
====================================================================================
*)

TYPE E_BatchPhase :
(
    PH_IDLE,
    PH_CIP,
    PH_SIP,
    PH_COOLDOWN,
    PH_INOCULATION,
    PH_INCUBATION,
    PH_HARVEST,
    PH_COMPLETE,
    PH_ABORT
);
END_TYPE

TYPE ST_BatchRecipe :
STRUCT
    SIP_Temp_Setpoint_C          : REAL;   // Typically 121.1 C (standard steam reference)
    SIP_Target_F0_min             : REAL;   // Minimum accumulated lethality, e.g. 15.0
    Cooldown_Temp_C                 : REAL;   // Safe inoculation temperature, e.g. 37.0
    Incubation_Temp_Setpoint_C        : REAL;
    Incubation_DO_Setpoint_Pct          : REAL;
    Incubation_pH_Setpoint                : REAL;
    Incubation_Duration_hr                  : REAL;
    Harvest_OD_Threshold                      : REAL;   // Optical density triggering harvest
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Bioreactor_BatchControl
VAR_INPUT
    Recipe                    : ST_BatchRecipe;   // Downloaded from SCADA/MES recipe management
    AI_VesselTemp_C             : REAL;
    AI_JacketTemp_C              : REAL;
    AI_DO_Pct                     : REAL;   // Dissolved oxygen, % of saturation
    AI_pH                          : REAL;
    AI_OpticalDensity                : REAL;   // OD600 or equivalent cell-density proxy
    AI_AgitatorSpeed_RPM               : REAL;   // Feedback
    DI_CIP_Complete                      : BOOL;   // From the CIP skid's own sequence
    DI_StartBatch                          : BOOL;
    DI_AbortBatch                            : BOOL;
    DI_System_Enable                           : BOOL;
END_VAR

VAR_OUTPUT
    AO_JacketTempSetpoint_C  : REAL := 0.0;   // Cascade: outer loop's output
    AO_HeatingValve_Pct       : REAL := 0.0;
    AO_CoolingValve_Pct        : REAL := 0.0;
    AO_AgitatorSpeed_RPM         : REAL := 0.0;   // Split-range primary
    AO_O2SpargeValve_Pct           : REAL := 0.0;   // Split-range secondary
    DO_AcidPump                      : BOOL := FALSE;
    DO_BasePump                        : BOOL := FALSE;
    BatchPhase                           : E_BatchPhase := PH_IDLE;
    Current_F0_min                         : REAL := 0.0;
    BatchElapsed_hr                          : REAL := 0.0;
    Alarm_SIP_Failed                           : BOOL := FALSE;
    Alarm_DO_Low                                 : BOOL := FALSE;
    Alarm_pH_Excursion                             : BOOL := FALSE;
    Alarm_TempDeviation                              : BOOL := FALSE;
    SystemStatus                                       : STRING[28] := 'STANDBY';
END_VAR

VAR
    // --- Cascade temperature control ---
    OuterTemp_PID           : FB_PID;
    InnerJacketTemp_PID      : FB_PID;
    OuterTemp_Kp              : REAL := 3.0;   OuterTemp_Ti : REAL := 300.0;
    InnerJacket_Kp             : REAL := 6.0;   InnerJacket_Ti : REAL := 60.0;

    // --- DO split-range control ---
    DO_PID                       : FB_PID;
    DO_Kp                          : REAL := 4.0;    DO_Ti : REAL := 120.0;
    DO_ControllerOutput_Pct          : REAL;
    Agitator_Min_RPM                   : REAL := 100.0;
    Agitator_Max_RPM                     : REAL := 400.0;

    // --- pH deadband dosing ---
    pH_Deadband                            : REAL := 0.10;

    // --- SIP / F0 tracking ---
    T_ScanTime                               : TON;   T_ScanTime_PT : TIME := T#1S;
    F0_RefTemp_C                               : REAL := 121.1;
    F0_zValue                                    : REAL := 10.0;
    LethalityRate_PerMin                           : REAL;

    // --- Batch timing ---
    T_IncubationTimer                                : TON;
    T_CooldownConfirm                                  : TON;   T_CooldownConfirm_PT : TIME := T#5M;

    TempDeviation_Deg                                    : REAL := 2.0;
END_VAR

// ------------------------------------------------------------------
// 1. CASCADE TEMPERATURE CONTROL
//    Outer loop (vessel temp) sets the target for the inner loop
//    (jacket temp), which reacts to a heat-transfer fluid disturbance
//    far faster than waiting for it to show up in the vessel itself.
// ------------------------------------------------------------------
IF (BatchPhase = PH_SIP) OR (BatchPhase = PH_COOLDOWN)
   OR (BatchPhase = PH_INOCULATION) OR (BatchPhase = PH_INCUBATION) THEN

    CASE BatchPhase OF
        PH_SIP:         OuterTemp_PID(SP := Recipe.SIP_Temp_Setpoint_C, PV := AI_VesselTemp_C,
                                        KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE,
                                        LMN_HLM := 135.0, LMN_LLM := 0.0);
        PH_COOLDOWN:    OuterTemp_PID(SP := Recipe.Cooldown_Temp_C, PV := AI_VesselTemp_C,
                                        KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE,
                                        LMN_HLM := 135.0, LMN_LLM := 0.0);
        PH_INOCULATION, PH_INCUBATION:
                        OuterTemp_PID(SP := Recipe.Incubation_Temp_Setpoint_C, PV := AI_VesselTemp_C,
                                        KP := OuterTemp_Kp, TI := OuterTemp_Ti, MANUAL := FALSE,
                                        LMN_HLM := 135.0, LMN_LLM := 0.0);
        ELSE ;
    END_CASE

    AO_JacketTempSetpoint_C := OuterTemp_PID.LMN;

    InnerJacketTemp_PID(SP := AO_JacketTempSetpoint_C, PV := AI_JacketTemp_C,
                          KP := InnerJacket_Kp, TI := InnerJacket_Ti, MANUAL := FALSE,
                          LMN_HLM := 100.0, LMN_LLM := -100.0);

    IF InnerJacketTemp_PID.LMN >= 0.0 THEN
        AO_HeatingValve_Pct := InnerJacketTemp_PID.LMN;
        AO_CoolingValve_Pct := 0.0;
    ELSE
        AO_HeatingValve_Pct := 0.0;
        AO_CoolingValve_Pct := ABS(InnerJacketTemp_PID.LMN);
    END_IF

    Alarm_TempDeviation := ABS(AI_VesselTemp_C - OuterTemp_PID.SP) > TempDeviation_Deg;
ELSE
    AO_HeatingValve_Pct := 0.0;
    AO_CoolingValve_Pct := 0.0;
    Alarm_TempDeviation := FALSE;
END_IF

// ------------------------------------------------------------------
// 2. F0 LETHALITY ACCUMULATION (active during SIP only)
//    Standard formula: contribution this scan = 10^((T-121.1)/z) * dt(min)
// ------------------------------------------------------------------
T_ScanTime(IN := (BatchPhase = PH_SIP), PT := T_ScanTime_PT);
IF BatchPhase = PH_SIP THEN
    IF T_ScanTime.Q THEN
        T_ScanTime(IN := FALSE);
        LethalityRate_PerMin := EXPT(10.0, (AI_VesselTemp_C - F0_RefTemp_C) / F0_zValue);
        Current_F0_min := Current_F0_min + (LethalityRate_PerMin * (1.0 / 60.0));
    END_IF
ELSIF BatchPhase = PH_CIP THEN
    Current_F0_min := 0.0;   // Reset for the new batch once CIP starts
END_IF

// ------------------------------------------------------------------
// 3. DISSOLVED OXYGEN - SPLIT-RANGE CONTROL (active during Incubation)
//    Agitation is the fast, cheap first response; oxygen sparging only
//    kicks in once agitation is already at its ceiling.
// ------------------------------------------------------------------
IF BatchPhase = PH_INCUBATION THEN
    DO_PID(SP := Recipe.Incubation_DO_Setpoint_Pct, PV := AI_DO_Pct,
            KP := DO_Kp, TI := DO_Ti, MANUAL := FALSE, LMN_HLM := 100.0, LMN_LLM := 0.0);
    DO_ControllerOutput_Pct := DO_PID.LMN;

    IF DO_ControllerOutput_Pct <= 70.0 THEN
        // 0-70% of controller output maps onto the full agitation range;
        // sparge stays closed - agitation alone is doing the work.
        AO_AgitatorSpeed_RPM := Agitator_Min_RPM
            + (DO_ControllerOutput_Pct / 70.0) * (Agitator_Max_RPM - Agitator_Min_RPM);
        AO_O2SpargeValve_Pct := 0.0;
    ELSE
        // Agitation stays maxed; the remaining 70-100% of output opens
        // the oxygen sparge valve.
        AO_AgitatorSpeed_RPM := Agitator_Max_RPM;
        AO_O2SpargeValve_Pct := (DO_ControllerOutput_Pct - 70.0) / 30.0 * 100.0;
    END_IF

    Alarm_DO_Low := AI_DO_Pct < (Recipe.Incubation_DO_Setpoint_Pct * 0.5);
ELSE
    AO_AgitatorSpeed_RPM := 0.0;
    AO_O2SpargeValve_Pct := 0.0;
    Alarm_DO_Low := FALSE;
END_IF

// ------------------------------------------------------------------
// 4. pH CONTROL - DEADBAND DOSING (active during Incubation)
//    On/off dosing pumps with a deadband, not a continuous PID output -
//    a real dosing pump chattering open/closed on a noisy pH signal
//    wastes reagent and can itself destabilise pH.
// ------------------------------------------------------------------
IF BatchPhase = PH_INCUBATION THEN
    DO_AcidPump := AI_pH > (Recipe.Incubation_pH_Setpoint + pH_Deadband);
    DO_BasePump := AI_pH < (Recipe.Incubation_pH_Setpoint - pH_Deadband);
    Alarm_pH_Excursion := ABS(AI_pH - Recipe.Incubation_pH_Setpoint) > 0.5;
ELSE
    DO_AcidPump := FALSE;
    DO_BasePump := FALSE;
    Alarm_pH_Excursion := FALSE;
END_IF

// ------------------------------------------------------------------
// 5. BATCH PHASE STATE MACHINE (ISA-88 style)
// ------------------------------------------------------------------
IF DI_AbortBatch THEN
    BatchPhase := PH_ABORT;
END_IF

CASE BatchPhase OF

    PH_IDLE:
        IF DI_System_Enable AND DI_StartBatch THEN
            BatchPhase := PH_CIP;
        END_IF

    PH_CIP:
        IF DI_CIP_Complete THEN
            BatchPhase := PH_SIP;
        END_IF

    PH_SIP:
        IF Current_F0_min >= Recipe.SIP_Target_F0_min THEN
            BatchPhase := PH_COOLDOWN;
        END_IF
        // No timeout modelled here deliberately - see the project manual,
        // Chapter 10: a real system needs a maximum SIP duration alarm
        // so an unreachable F0 target cannot hold a vessel at high
        // temperature indefinitely.

    PH_COOLDOWN:
        T_CooldownConfirm(IN := ABS(AI_VesselTemp_C - Recipe.Cooldown_Temp_C) < 1.0,
                            PT := T_CooldownConfirm_PT);
        IF T_CooldownConfirm.Q THEN
            BatchPhase := PH_INOCULATION;
        END_IF

    PH_INOCULATION:
        // In this simplified model, inoculation is an operator/upstream-
        // system confirmed step; a real recipe would sequence a timed
        // transfer here. Advancing on a brief settle timer stands in
        // for that step.
        T_IncubationTimer(IN := TRUE, PT := T#2M);
        IF T_IncubationTimer.Q THEN
            T_IncubationTimer(IN := FALSE);
            BatchPhase := PH_INCUBATION;
        END_IF

    PH_INCUBATION:
        T_IncubationTimer(IN := TRUE, PT := REAL_TO_TIME(Recipe.Incubation_Duration_hr * 3600000.0));
        BatchElapsed_hr := TIME_TO_REAL(T_IncubationTimer.ET) / 3600000.0;
        IF T_IncubationTimer.Q OR (AI_OpticalDensity >= Recipe.Harvest_OD_Threshold) THEN
            T_IncubationTimer(IN := FALSE);
            BatchPhase := PH_HARVEST;
        END_IF

    PH_HARVEST:
        BatchPhase := PH_COMPLETE;   // Harvest sequencing itself owned by a downstream skid

    PH_COMPLETE:
        ; // Awaits operator acknowledgement / new batch start

    PH_ABORT:
        AO_HeatingValve_Pct := 0.0; AO_CoolingValve_Pct := 100.0;   // Fail safe: pull heat out
        AO_AgitatorSpeed_RPM := 0.0; AO_O2SpargeValve_Pct := 0.0;
        DO_AcidPump := FALSE; DO_BasePump := FALSE;

    ELSE
        ;
END_CASE

Alarm_SIP_Failed := (BatchPhase = PH_ABORT) AND (Current_F0_min < Recipe.SIP_Target_F0_min);

// ------------------------------------------------------------------
// 6. STATUS TEXT
// ------------------------------------------------------------------
CASE BatchPhase OF
    PH_IDLE:         SystemStatus := 'STANDBY';
    PH_CIP:           SystemStatus := 'CIP IN PROGRESS';
    PH_SIP:            SystemStatus := 'STERILISING (SIP)';
    PH_COOLDOWN:        SystemStatus := 'COOLING TO INOCULATE';
    PH_INOCULATION:      SystemStatus := 'INOCULATION';
    PH_INCUBATION:        SystemStatus := 'INCUBATION ACTIVE';
    PH_HARVEST:            SystemStatus := 'HARVEST';
    PH_COMPLETE:            SystemStatus := 'BATCH COMPLETE';
    PH_ABORT:                SystemStatus := 'BATCH ABORTED';
    ELSE                      SystemStatus := 'UNKNOWN';
END_CASE

END_FUNCTION_BLOCK
