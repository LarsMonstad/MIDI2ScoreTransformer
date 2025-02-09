# created as a inference script for midi files without ASAP dataset text annotation. 
import torch
import argparse
from pathlib import Path
from tokenizer import MultistreamTokenizer
from models.roformer import Roformer  
from utils import infer

DEFAULT_CKPT = "MIDI2ScoreTF.ckpt"

def midi_to_musicxml(midi_path: str, ckpt_path: str = DEFAULT_CKPT, output_path: str = None):
    # Set default output path if not specified
    if not output_path:
        output_path = Path(midi_path).with_suffix('.xml').name
    
    # Initialize components
    tokenizer = MultistreamTokenizer()
    model = Roformer.load_from_checkpoint(ckpt_path).eval().to("cuda" if torch.cuda.is_available() else "cpu")
    
    # Tokenize and process MIDI
    input_tokens = tokenizer.tokenize_midi(midi_path)
    batched_input = {k: v.unsqueeze(0).to(model.device) for k, v in input_tokens.items()}
    
    # Run inference
    with torch.no_grad():
        output = infer(batched_input, model, chunk=512, overlap=64, kv_cache=True)
    
    # Save MusicXML
    score = tokenizer.detokenize_mxl({k: v[0].cpu() for k, v in output.items()})
    score.write("musicxml", fp=output_path)
    print(f"Successfully saved score to {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert MIDI to MusicXML')
    parser.add_argument('midi_path', type=str, help='Path to input MIDI file')
    parser.add_argument('-m', '--model', type=str, default=DEFAULT_CKPT, 
                       help=f'Path to model checkpoint (default: {DEFAULT_CKPT})')
    parser.add_argument('-o', '--output', type=str, 
                       help='Output path for MusicXML file (default: <midi_name>.xml)')
    
    args = parser.parse_args()
    
    midi_to_musicxml(
        midi_path=args.midi_path,
        ckpt_path=args.model,
        output_path=args.output
    )