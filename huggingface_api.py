import transformers
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
import torch
model_name='mistralai/Mistral-7B-Instruct-v0.1'
hf_token = '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'
model_config = transformers.AutoConfig.from_pretrained(
   model_name, token=hf_token, trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=hf_token)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
   model_name,
   quantization_config=bnb_config,
)

inputs_not_chat = tokenizer.encode_plus("[INST]I'm interested in learning more about home made remedies and pesticides. Can you provide some information on these topics for the tomato bacterial leave disease?[/INST]", return_tensors="pt")['input_ids'].to('cuda')


attention_mask = torch.ones_like(inputs_not_chat)


generated_ids = model.generate(inputs_not_chat,
                              max_new_tokens=1000,
                              do_sample=True,
                              attention_mask=attention_mask)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded)