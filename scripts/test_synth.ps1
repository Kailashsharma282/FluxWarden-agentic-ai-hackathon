Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.Volume = 100

$voice = $synth.GetInstalledVoices() | Select-Object -First 1
if ($voice) {
    $synth.SelectVoice($voice.VoiceInfo.Name)
}

$outputAudio = "C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21\test_audio.wav"
$synth.SetOutputToWaveFile($outputAudio)
$synth.Speak("FluxWarden is operational and ready for incident investigation and recovery.")
$synth.Dispose()
Write-Output "AUDIO_GENERATED: $outputAudio"
