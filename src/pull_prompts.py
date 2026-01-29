"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_TO_PULL = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"

def pull_prompts_from_langsmith():
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    try:
        print(f"Puxando prompt: {PROMPT_TO_PULL}")
        client = Client()
        prompt = client.pull_prompt(PROMPT_TO_PULL)
        prompt_data = convert_prompt_to_dict(prompt)

        if save_yaml(prompt_data, OUTPUT_PATH):
            print(f"✓ Prompt salvo em: {OUTPUT_PATH}")
            return True
        return False

    except Exception as e:
        print(f"❌ Erro ao fazer pull: {e}")
        return False

def convert_prompt_to_dict(prompt) -> dict:
    return {
            "bug_to_user_story_v1": {
                "version": "v1",
                "description": "Prompt inicial para converter bugs em user stories",
                "tags": ["bug-analysis", "user-story", "product-management"],
                "system_prompt": get_message_template(prompt.messages, 0),
                "user_prompt": get_message_template(prompt.messages, 1),
                "metadata": {
                    "techniques_applied": ["zero-shot"]
                }
            }
        }

def get_message_template(messages, index: int, fallback: str = "") -> str:
    try:
        return messages[index].prompt.template
    except (IndexError, AttributeError):
        return fallback
        
def main():
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
