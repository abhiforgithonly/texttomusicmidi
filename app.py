from audiocraft.models import MusicGen
import streamlit as st
import torch
import torchaudio
import os
import numpy as np
import base64
import time
from midiutil.MidiFile import MIDIFile
from scipy import signal
import librosa

@st.cache_resource
def load_model():
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    return model

def generate_music_tensors(description, duration: int):
    print("Description: ", description)
    print("Duration: ", duration)
    model = load_model()
    
    model.set_generation_params(
        use_sampling=True,
        top_k=250,
        duration=duration
    )
    
    output = model.generate(
        descriptions=[description],
        progress=True,
        return_tokens=True
    )
    
    return output[0]

def save_audio(samples: torch.Tensor):
    """Renders an audio player for the given audio samples and saves them to a local directory.
    
    Args:
        samples (torch.Tensor): a Tensor of decoded audio samples
            with shapes [B, C, T] or [C, T]
        
    Returns:
        The path to the saved audio file
    """
    
    print("Samples (inside function): ", samples)
    sample_rate = 32000
    save_path = "audio_output/"
    
    # Create directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    assert samples.dim() == 2 or samples.dim() == 3
    
    samples = samples.detach().cpu()
    if samples.dim() == 2:
        samples = samples[None, ...]
    
    saved_paths = []
    for idx, audio in enumerate(samples):
        audio_path = os.path.join(save_path, f"audio_{idx}.wav")
        torchaudio.save(audio_path, audio, sample_rate)
        saved_paths.append(audio_path)
    
    return saved_paths[0]  # Return the path to the first audio file

def audio_to_midi(audio_path, output_path, min_note=36, max_note=84):
    """
    Convert audio to MIDI by extracting pitch information.
    
    Args:
        audio_path: Path to the audio file
        output_path: Path to save the MIDI file
        min_note: Minimum MIDI note number
        max_note: Maximum MIDI note number
    """
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)
    
    # Convert to mono if stereo
    if len(y.shape) > 1:
        y = np.mean(y, axis=0)
    
    # Extract pitch with librosa
    hop_length = 512
    n_fft = 2048
    
    # Use harmonic part for better pitch detection
    y_harmonic = librosa.effects.harmonic(y)
    
    # Pitch tracking
    pitches, magnitudes = librosa.piptrack(
        y=y_harmonic, 
        sr=sr, 
        n_fft=n_fft,
        hop_length=hop_length
    )
    
    # Create a new MIDI file with 1 track
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    volume = 100
    
    # Add track name and tempo
    midi.addTrackName(track, time, "Generated from Audio")
    midi.addTempo(track, time, 120)
    
    # Time in beats
    time_step = hop_length / sr
    curr_time = 0
    active_notes = {}
    
    # Process each frame
    for frame in range(pitches.shape[1]):
        # Find the pitch with the highest magnitude
        index = np.argmax(magnitudes[:, frame])
        pitch = pitches[index, frame]
        
        if pitch > 0:  # If pitch is detected
            # Convert frequency to MIDI note number
            midi_note = int(round(librosa.hz_to_midi(pitch)))
            
            # Constrain to the specified range
            midi_note = max(min_note, min(midi_note, max_note))
            
            # Add note if not already active
            if midi_note not in active_notes:
                midi.addNote(track, channel, midi_note, curr_time, time_step, volume)
                active_notes[midi_note] = curr_time
            
        curr_time += time_step
    
    # Write the MIDI file
    with open(output_path, "wb") as midi_file:
        midi.writeFile(midi_file)
    
    return output_path

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

st.set_page_config(
    page_icon="musical_note",
    page_title="Music Gen with MIDI"
)

def main():
    
    st.title("Text to Music Generator 🎵")
    
    with st.expander("See explanation"):
        st.write("Music Generator app built using Meta's Audiocraft library. We are using Music Gen Small model. This app generates audio and also allows exporting to MIDI format for further editing in DAWs.")
    
    # Create output directories if they don't exist
    os.makedirs("audio_output", exist_ok=True)
    
    text_area = st.text_area("Enter your description...")
    time_slider = st.slider("Select time duration (In Seconds)", 0, 20, 10)
    
    # MIDI conversion options
    st.sidebar.header("MIDI Conversion Settings")
    midi_min_note = st.sidebar.slider("Min MIDI Note", 0, 127, 36)
    midi_max_note = st.sidebar.slider("Max MIDI Note", 0, 127, 84)
    
    if st.button("Generate Music"):
        if text_area and time_slider:
            st.json({
                'Your Description': text_area,
                'Selected Time Duration (in Seconds)': time_slider,
                'MIDI Min Note': midi_min_note,
                'MIDI Max Note': midi_max_note
            })
            
            with st.spinner("Generating music..."):
                try:
                    # Generate music
                    music_tensors = generate_music_tensors(text_area, time_slider)
                    print("Music Tensors: ", music_tensors)
                    
                    # Save audio file
                    audio_filepath = save_audio(music_tensors)
                    timestamp = int(time.time())
                    final_audio_path = f"audio_output/generated_audio_{timestamp}.wav"
                    os.rename(audio_filepath, final_audio_path)
                    
                    # Display the audio
                    st.subheader("Generated Audio")
                    audio_file = open(final_audio_path, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
                    st.markdown(get_binary_file_downloader_html(final_audio_path, 'Audio (WAV)'), unsafe_allow_html=True)
                    
                    # Generate MIDI from the audio
                    st.subheader("MIDI Conversion")
                    
                    midi_filename = f"generated_midi_{timestamp}.mid"
                    midi_save_path = f"audio_output/{midi_filename}"
                    with st.spinner("Converting to MIDI..."):
                        midi_filepath = audio_to_midi(final_audio_path, midi_save_path, 
                                                   min_note=midi_min_note, max_note=midi_max_note)
                    
                    st.success("MIDI file generated successfully!")
                    st.markdown(get_binary_file_downloader_html(midi_filepath, 'MIDI File'), unsafe_allow_html=True)
                    
                    # Show saved file information
                    st.subheader("Saved Files")
                    st.info(f"Audio saved as: {os.path.basename(final_audio_path)}")
                    st.info(f"MIDI saved as: {midi_filename}")
                    
                    st.info("Note: The MIDI conversion is an approximation of the audio's pitch content. For best results, you may want to edit the MIDI file in a DAW.")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please try again with a different description or duration.")
        else:
            st.warning("Please enter a description and set the duration before generating.")

if __name__ == "__main__":
    main()