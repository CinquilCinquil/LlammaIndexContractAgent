import asyncio
from model import make_agent, make_memory, make_prompt_template
import time

email = "putyourtestemailhere@gmail.com"

async def main():
    agent = make_agent()
    chat_memory = make_memory()
    prompt_template = make_prompt_template(email)

    state = 0
    pause = 0

    input_sequence = [
        "Load the contract from data/example_contract.pdf.",
        pause,
        "An e-mail has been received. Continue to follow your instructions."
    ]
    
    input_loop = input_sequence[1:]
    len_input_seq = len(input_sequence)

    i = 0
    while True:
        if state == 0:
            query = (input_sequence[i % len_input_seq] if i < len_input_seq
                      else input_loop[(i - len_input_seq) % len(input_loop)])
            print("\nQUERY: ", query, "\n")
        else:
            state = 0

        if query == pause:
            input_ = int(input("Press 0 to continue or 1 to prompt"))
            if input_ == 1:
                query = input("Enter query: ")
                state = 1
        else:
            response = await agent.run(user_msg = query, 
                                    chat_history = prompt_template,
                                    memory = chat_memory)
            print("### AGENT RESPONSE ###\n")
            print(response)
            print("\n###")
        time.sleep(2) # Avoids going over request/minute quota
        i += 1

asyncio.run(main())
