Add-Type -AssemblyName System.Speech

function Synthesize-Audio {
    param (
        [string]$text,
        [string]$outputPath
    )
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.Rate = 0
    $synth.Volume = 100

    $voice = $synth.GetInstalledVoices() | Select-Object -First 1
    if ($voice) {
        $synth.SelectVoice($voice.VoiceInfo.Name)
    }

    $synth.SetOutputToWaveFile($outputPath)
    $synth.Speak($text)
    $synth.Dispose()
    Write-Output "Successfully generated: $outputPath"
}

$artifactsDir = "C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21"

# Script 1: Architecture, Command Center & UI Walkthrough
$script1 = @"
Welcome to FluxWarden, an autonomous agentic AI platform for enterprise incident investigation, adaptive recovery, and system resilience.
Presented by Kailash Sharma for the Agentic AI Hackathon at Tech Zephyr 4.0, IIT Bhubaneswar.
In this first demonstration, we tour the Command Center interface.
The Mission Control view displays the live autonomous state machine, currently in Idle and ready for operational dispatch.
Navigating to Service Topology reveals our live Canvas visualization with ten interconnected microservices, dependency directed graphs, and pulsing packet flows.
Switching to Live Telemetry, we monitor real-time request rates, error rates, and p99 latency across all services, streaming at one thousand six hundred requests per second.
The Chaos Lab provides one-click injection for realistic failure scenarios, including bad deployments, database connection exhaustion, memory leaks, and cascading failures.
Under Incident Forensics, engineers can review root cause analyses, failure timeline events, hypotheses, and forensic evidence logs.
The Mission Chat interface allows operators to converse with the agent in natural language and grant human approvals for high-risk remediation actions.
Operational Memory indexes past incidents and learned resolution strategies using semantic retrieval.
Finally, the Architecture and Judge Scorecard tabs provide interactive component inspection and confirm complete compliance with all sixty-eight hackathon requirements.
"@

# Script 2: Deterministic Demo - Adaptive Incident Recovery
$script2 = @"
This is Demonstration Two: Deterministic Incident Recovery and Adaptive Replanning.
We trigger the live demonstration sequence by clicking RUN DEMO.
Step One: A bad deployment is injected into the payment API. The error rate instantly spikes to seventy-four percent, and service health transitions to critical red.
Steps Two through Five: FluxWarden autonomously begins investigation. The agent queries service health, inspects recent container logs, and detects an uncaught null pointer exception introduced in release v42.
Step Six demonstrates our critical differentiating capability: The agent initiates a standard rollback to release v41, but the rollback intentionally fails because the container image is corrupted in the registry.
A static script would crash or loop indefinitely. But FluxWarden detects the tool failure, updates its failed actions history, and dynamically transitions to the Replan state.
Steps Seven to Nine: The agent inspects operational memory and queries standby backup services, discovering that backup-service v40 is healthy and synchronized.
Step Ten: The agent executes adaptive recovery, rerouting ingress traffic from the failed payment API to the standby backup replica. The live topology canvas reflects the immediate traffic shift.
Steps Eleven through Fourteen: The six-probe verification engine engages, executing synthetic transactions, latency SLA checks, error rate monitoring, dependency probes, and database ACID consistency validations.
Step Fifteen: All six verification probes pass with flying colors. The glowing incident resolution card appears, detailing the root cause, failed rollback, successful adaptive recovery, and post-mortem report ready for export.
"@

# Script 3: Chaos Lab Injection, Mission Chat & Human-in-the-Loop Approval
$script3 = @"
This is Demonstration Three: Chaos Lab Scenario Injection, Mission Chat, and Human-in-the-Loop Safety Controls.
Section 17 of our design specification requires strict human authorization for high-risk infrastructure interventions.
We enter the Chaos Lab and inject a high-severity Database Connection Pool Exhaustion incident into order-db.
The active connection count spikes to ninety-nine percent, thread pools deadlock, and API gateway requests begin queuing.
Switching to Mission Chat, the operator prompts the agent: 'Investigate order database deadlock and execute emergency connection drain and restart.'
FluxWarden parses the objective, evaluates safety boundaries, and identifies that restarting a core database is a High Risk Tier Three action.
Instead of proceeding unilaterally, the agent halts and surfaces the Human Approval Modal.
The modal displays the blast radius, targeted resources, rollback safety plan, and justification.
The human operator reviews the proposed action and clicks Approve Action.
With authorization granted, the agent executes the connection pool drain, safely restarts the database instance, and confirms recovery via telemetry probes.
FluxWarden seamlessly balances full agentic autonomy with enterprise-grade safety and human oversight.
"@

Synthesize-Audio -text $script1 -outputPath "$artifactsDir\fluxwarden_demo_1_overview_audio.wav"
Synthesize-Audio -text $script2 -outputPath "$artifactsDir\fluxwarden_demo_2_recovery_audio.wav"
Synthesize-Audio -text $script3 -outputPath "$artifactsDir\fluxwarden_demo_3_chaos_approval_audio.wav"

Write-Output "ALL_AUDIO_FILES_SYNTHESIZED_SUCCESSFULLY"
