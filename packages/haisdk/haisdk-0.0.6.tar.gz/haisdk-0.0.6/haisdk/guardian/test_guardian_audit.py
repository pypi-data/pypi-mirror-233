from guardian_audit import GuardianAudit
from chatgpt_wrapper import GPTWrapper
import json

config = {
    "tenant_id": "HolisticAI-58jnt",
    "apikey": "YmIzMGQzZDAtMTY0Yi00Mjk2LWIxY2UtMTJhMWRmMjhhNTI3",
    "audit_id": "da2c2ffe-5f00-48ff-9012-1749d2af35e7"
}

audit = GuardianAudit(config)
gpt = GPTWrapper()

audit_prompts = audit.load_prompts()

stereotype_messages = []
# audit ChatGPT
for prompt in audit_prompts['stereotype']["stereotype_prompts"][0:70]:
    full_prompt = f"complete the following sentence: {prompt}"
    completion = gpt.complete(full_prompt)["choices"][0]["text"]
    processed_prompt = full_prompt.split(":")[1]
    processed_prompt = processed_prompt + completion

    stereotype_messages.append({
    "prompt": prompt,
    "response": processed_prompt.strip()
    })


toxicity_messages = []
for prompt in audit_prompts['toxicity']["toxicity_prompts"][0:70]:
    full_prompt = f"complete the following sentence: {prompt}"
    completion = gpt.complete(full_prompt)["choices"][0]["text"]
    processed_prompt = full_prompt.split(":")[1]
    processed_prompt = processed_prompt + completion

    toxicity_messages.append({
    "prompt": prompt,
    "response": processed_prompt.strip()
    })


to_audit = {
    'stereotype': stereotype_messages,
    'toxicity': toxicity_messages
}
# send messages to be processed
audit.process(to_audit)