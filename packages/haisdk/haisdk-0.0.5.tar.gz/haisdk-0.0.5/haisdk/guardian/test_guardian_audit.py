from guardian_audit import GuardianAudit
from chatgpt_wrapper import GPTWrapper

config = {
    "tenant_id": "HolisticAI-58jnt",
    "apikey": "YmIzMGQzZDAtMTY0Yi00Mjk2LWIxY2UtMTJhMWRmMjhhNTI3",
    "audit_id": "326075a1-d6cf-4e53-a2f1-e09ab2d093b6"
}

audit = GuardianAudit(config)
gpt = GPTWrapper()

audit_prompts = audit.load_prompts()

messages = []
# audit ChatGPT
for prompt in audit_prompts['stereotype']["stereotype_prompts"][0:10]:
    full_prompt = f"complete the following sentence: {prompt}"
    completion = gpt.complete(full_prompt)["choices"][0]["text"]
    processed_prompt = full_prompt.split(":")[1]
    processed_prompt = processed_prompt + completion

    messages.append({
    "prompt": prompt,
    "response": processed_prompt.strip()
    })

# send messages to be processed
audit.process('stereotype', messages)



