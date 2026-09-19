# GPU runtime recommended (Google Colab)

# Data source: Denver City Council meeting excerpt, could be found here:
# https://drive.google.com/file/d/1N_kpSojRR5RYzupz6nqM8hMSoEF_R7pU/view?usp=sharing


from transformers import AutoModelForCausalLM

from audio_transcription import audio_filename
from client import LLAMA
from quantization_and_tokenizer import quant_config, inputs, streamer, tokenizer

def inference(quant_config, inputs, streamer, tokenizer, model_name=LLAMA):
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        quantization_config=quant_config
    )
    outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)

    response = tokenizer.decode(outputs[0])

    filename = f"{audio_filename}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response)

    print(f"\nSuccess! Brochure saved as '{filename}' in the current folder.\n")

if __name__ == "__main__":
    inference(quant_config, inputs, streamer, tokenizer)