import argparse
import os

import streamlit as st
import openai
import pwinput

from easyenvi import EasyEnvironment

from . import llm

from .git_utils import git_assistant

max_len_models = {
    "gpt-3.5-turbo": 4000,
    "gpt-3.5-turbo-0301": 4000,
    "gpt-3.5-turbo-0613": 4000,
    "gpt-3.5-turbo-16k": 16000,
    "gpt-3.5-turbo-16k-0613": 16000,
    "gpt-4": 8000,
    "gpt-4-0314": 8000,
    "gpt-4-0613": 8000
}

def get_gpt(args):
    if args.gpt_model is None:
        gpt_model = "gpt-3.5-turbo-0613"
    else:
        gpt_model = args.gpt_model

    if gpt_model not in max_len_models:
        max_len_prompt = 4000
    else:
        max_len_prompt = max_len_models[gpt_model]

    return gpt_model, max_len_prompt

def main():

    parser = argparse.ArgumentParser(description="Git Assistant Tool")
    subparsers = parser.add_subparsers(dest="command")

    generate_readme_parser = subparsers.add_parser("generate-readme", help="Generate the README.md file using generative AI.")
    generate_readme_parser.add_argument("--github_url", type=str, help="GitHub repository URL", required=False)
    generate_readme_parser.add_argument("--gpt_model", type=str, help="OPEN AI GPT model", required=False)

    chatbot_parser = subparsers.add_parser("chatbot", help="Interact with a chatbot and ask questions about the repository.")
    chatbot_parser.add_argument("--github_url", type=str, help="GitHub repository URL", required=False)
    chatbot_parser.add_argument("--gpt_model", type=str, help="OPEN AI GPT model", required=False)

    args = parser.parse_args()

    # provider = "VA"
    # for k, v in st.secrets['OPEN_AI'][provider].items():
    #         os.environ[k] = v
    # azure_engine = st.secrets['OPEN_AI'][provider]['api_type_CHAT_GPT'] == "azure"

    print("\n\033[1m(git-assistant)\033[0m: Please copy/paste your OpenAI API token. Tutorial to get your free API token : https://www.youtube.com/watch?v=EQQjdwdVQ-M")
    openai.api_key = pwinput.pwinput("\n\033[1m(user)\033[0m: OPEN AI TOKEN: ")

    azure_engine = False

    gpt_model, max_len_prompt = get_gpt(args)
    
    writer = llm.ChatGPT(model=gpt_model, azure_engine=azure_engine)
    gitty = git_assistant(repo_url=args.github_url, folder=".", writer=writer)
    
    if args.github_url is not None:
        print('\n\033[1m(git-assistant)\033[0m: I am cloning the repository...')
        gitty.clone_repository()
    
    local_path = gitty.folder + '/.gitassistant'
    if not os.path.exists(local_path):
        os.mkdir(local_path)

    def md_loader(path, **kwargs):
        return path.read(**kwargs)

    def md_saver(obj, path, **kwargs):
        path.write(obj, **kwargs)

    env = EasyEnvironment(
        local_path=local_path,
        extra_loader_config={'md': (md_loader, 'rt')},
        extra_saver_config={'md': (md_saver, 'wt')}
        )

    files = os.listdir(local_path)
    if args.command == "generate-readme":

        if 'metadata.pickle' in files:
            gitty.summary_concat = env.local.load('metadata.pickle')
            print(len(gitty.summary_concat), "vs", max_len_prompt*1.5)
            if len(gitty.summary_concat) > max_len_prompt*1.5:
                choice = "Y"
            else:
                print('\n\033[1m(git-assistant)\033[0m: I have already been initialised in this repository. Run a new initialisation if the repository has singificantly changed since my last initialisation. Do you want to re-do the initialisation ?')
                choice = input("\n\033[1m(user)\033[0m: Response [Y or N]: ")
        else:
            choice = "Y"
        
        if choice == "Y":
            print("\n\033[1m(git-assistant)\033[0m: I am initialising ! Please wait a bit...")
            gitty.get_files_content()
            gitty.get_summary_concat(max_len_summary_concat=max_len_prompt*0.7)
            env.local.save(gitty.summary_concat, 'metadata.pickle')

        choice = "0"
        while choice != "2":
            if ('structure.md' in files) & (choice == "0"):
                gitty.structure_md = env.local.load('structure_md.md')
            else:
                print("\n\033[1m(git-assistant)\033[0m: I am genenerated your README structure...")
                if not hasattr(gitty, 'global_summary'):
                    gitty.get_global_summary()
                structure_md = gitty.generate_readme_structure()
                env.local.save(structure_md, 'structure_md.md')
            print(f"\n\033[1m(git-assistant)\033[0m: Here is the generated README structure I stored in {local_path}/structure_md.md:")
            print(f"{gitty.structure_md}\n")
            print("Do you want to generate a new README structure or to generate the README content according to this structure?")
            print("(1) - Generate a new README structure.")
            print("(2) - Generate README content according to this structure.")
            print("Tap 1 or 2.")
            print(f"Note: If you want to modify this structure by yourself, please modify the file {local_path}/structure_md.md then tap 2")
            choice = input("\n\033[1m(user)\033[0m: Response [1 or 2]: ")
        
        gitty.structure_md = env.local.load('structure_md.md')
        readme = gitty.generate_readme()
        env.local.save(readme, 'README.md')

        print(f'\n\033[1m(git-assistant)\033[0mThe README has been successfully generated! It has been stored into {local_path}/README.md')

    elif args.command == "chatbot":

        if 'metadata.pickle' in files:
            gitty.summary_concat = env.local.load('metadata.pickle')
            if len(gitty.summary_concat) > max_len_prompt * 1.5:
                choice = "Y"
        
        if choice == "Y":
            print("\n\033[1m(git-assistant)\033[0m: I am initialising ! Please wait a bit...")
            gitty.get_files_content()
            gitty.get_summary_concat(max_len_summary_concat=max_len_prompt*0.7)
            env.local.save(gitty.summary_concat, 'metadata.pickle')

        gitty.initialize_chatbot()

        print("\n\033[1m(git-assistant)\033[0m: Hello, do you have a question about this repository?")

        while True:
            user_msg = input('\n\033[1m(user)\033[0m: Question: ')
            response = gitty.chatbot_question(question=user_msg)
            print(f"\n\033[1m(git-assistant)\033[0m: {response}")


if __name__ == "__main__":
    main()