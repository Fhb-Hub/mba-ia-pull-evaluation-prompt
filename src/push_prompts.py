"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

PROMPT_FILE_PATH = "prompts/bug_to_user_story_v2.yml"
PROMPT_NAME = "bug_to_user_story_v2"

load_dotenv()


def push_prompt_to_langsmith(client: Client, prompt_name: str, prompt_data: dict, owner: str) -> bool:
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt_template = prompt_data.get("user_prompt", "")

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt_template)
        ])

        full_name = f"{owner}/{prompt_name}"
        print(f"Pushando prompt: {full_name}")

        client.push_prompt(
            full_name,
            object=prompt,
            description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", []),
            is_public=True
        )

        print(f"✓ Prompt publicado: {full_name}")
        print(f"  Versão: {prompt_data.get('version', '')}")
        print(f"  Descrição: {prompt_data.get('description', '')}")
        print(f"  Técnicas: {', '.join(prompt_data.get('metadata', {}).get('techniques_applied', []))}")

        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push: {e}")
        return False


def main():
    print_section_header("PUSH DE PROMPTS")

    owner = os.getenv("USERNAME_LANGSMITH_HUB")
    if not owner:
        print("❌ USERNAME_LANGSMITH_HUB não configurado")
        return 1

    client = Client()

    prompt_data_dict = load_yaml(PROMPT_FILE_PATH)
    if not prompt_data_dict:
        return 1

    prompt_data = prompt_data_dict[PROMPT_NAME]

    is_valid, errors = validate_prompt_structure(prompt_data)
    if not is_valid:
        print("❌ Validação falhou:")
        for error in errors:
            print(f"   - {error}")
        return 1

    success = push_prompt_to_langsmith(client, PROMPT_NAME, prompt_data, owner)

    if success:
        print(f"\n✓ Prompt publicado em:")
        print(f"  https://smith.langchain.com/hub/{owner}/{PROMPT_NAME}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
