# uagents_demo.py
# Simple uAgents example: coordinator and worker talk over a protocol.

from uagents import Agent, Bureau, Context, Model, Protocol

# 1) Define message models
class Task(Model):
    topic: str


class Result(Model):
    topic: str
    ideas: str


# 2) Define a protocol
work_proto = Protocol(name="idea_protocol", version="1.0")


# 3) Create the agents
worker = Agent(name="worker")
coordinator = Agent(name="coordinator")


# 4) Protocol handlers

# Worker: receives Task, sends back Result
@work_proto.on_message(model=Task, replies={Result})
async def handle_task(ctx: Context, sender: str, msg: Task):
    topic = msg.topic
    ideas = (
        f"1) Define {topic}.\n"
        f"2) Explain why {topic} matters.\n"
        f"3) Give one real-world example of {topic}.\n"
    )
    await ctx.send(sender, Result(topic=topic, ideas=ideas))


# Coordinator: receives Result and prints it
@work_proto.on_message(model=Result)
async def handle_result(ctx: Context, sender: str, msg: Result):
    print("\n=== uAgents Demo Output ===")
    print(f"From: {sender}")
    print(f"Topic: {msg.topic}")
    print(msg.ideas)
    print("============================\n")


# 5) Startup event: coordinator sends the first Task
@coordinator.on_event("startup")
async def send_initial_task(ctx: Context):
    await ctx.send(worker.address, Task(topic="multi-agent orchestration"))


# 6) Attach protocol to both agents
worker.include(work_proto)
coordinator.include(work_proto)


# 7) Run both agents in a Bureau
if __name__ == "__main__":
    bureau = Bureau()
    bureau.add(worker)
    bureau.add(coordinator)
    bureau.run()
