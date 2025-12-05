# langgraph_demo.py
# Simple LangGraph example: a tiny workflow that turns a topic into bullet points.

from dataclasses import dataclass
from langgraph.graph import StateGraph


# 1) Define the state that flows through the graph.
#    We keep it small: topic -> ideas -> final formatted text.
@dataclass
class State:
    topic: str = ""
    ideas: str = ""
    formatted: str = ""


# 2) Node 1: "Brainstorm" ideas for the topic (mocked, no LLM for simplicity).
def brainstorm_node(state: State) -> State:
    topic = state.topic
    state.ideas = (
        f"1) Explain what {topic} is.\n"
        f"2) Show a tiny example of {topic}.\n"
        f"3) Compare {topic} to something familiar.\n"
    )
    return state


# 3) Node 2: Format the ideas nicely as bullet points.
def format_node(state: State) -> State:
    lines = [line.strip() for line in state.ideas.splitlines() if line.strip()]
    bullets = "\n".join(f"- {line}" for line in lines)
    state.formatted = f"Bullet points about {state.topic}:\n{bullets}"
    return state


# 4) Build the workflow graph: brainstorm -> format
def build_app():
    graph = StateGraph(State)

    # register nodes
    graph.add_node("brainstorm", brainstorm_node)
    graph.add_node("format", format_node)

    # connect them
    graph.add_edge("brainstorm", "format")

    # set where we start
    graph.set_entry_point("brainstorm")

    # compile into an executable app
    return graph.compile()


if __name__ == "__main__":
    app = build_app()

    # 5) Run the workflow with some initial state.
    initial_state = {"topic": "multi-agent orchestration"}
    final_state = app.invoke(initial_state)

    # 6) Show the result.
    print("=== LangGraph Demo Output ===")
    print(final_state["formatted"])
