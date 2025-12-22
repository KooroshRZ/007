# main.py

from agent import run_agent

def main():
    while True:
        user = input("\n> ")
        if user.lower() in {"exit", "quit"}:
            break
        print(run_agent(user))

if __name__ == "__main__":
    main()
