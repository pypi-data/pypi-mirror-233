from guardian_audit import GuardianAudit
from chatgpt_wrapper import GPTWrapper
import json

def audit_toxicity(prompts):
    toxicity_messages = []
    for prompt in prompts['toxicity']["toxicity_prompts"]:
        full_prompt = f"complete the following sentence: {prompt}"
        completion = gpt.complete(full_prompt)["choices"][0]["text"]
        processed_prompt = full_prompt.split(":")[1]
        processed_prompt = processed_prompt + completion

        toxicity_messages.append({
            "prompt": prompt,
            "response": processed_prompt.strip()
        })
    return toxicity_messages

def audit_stereotype(prompts):
    stereotype_messages = []
    # audit ChatGPT
    for prompt in prompts['stereotype']["stereotype_prompts"]:
        full_prompt = prompt
        completion = gpt.complete(full_prompt)["choices"][0]["text"]
        processed_prompt = full_prompt.split(":")[1]
        processed_prompt = processed_prompt + completion

        stereotype_messages.append({
            "prompt": prompt,
            "response": processed_prompt.strip()
        })
    return stereotype_messages


config = {
    "tenant_id": "HolisticAI-58jnt",
    "apikey": "YmIzMGQzZDAtMTY0Yi00Mjk2LWIxY2UtMTJhMWRmMjhhNTI3",
    "audit_id": "157d4f31-9970-4814-80e9-e2f717343184"
}

audit = GuardianAudit(config)

gpt = GPTWrapper()
audit_prompts = audit.load_prompts()


to_audit = {
    'stereotype': audit_stereotype(audit_prompts),
    'toxicity': audit_toxicity(audit_prompts)
}
# send messages to be processed
audit.process(to_audit)


