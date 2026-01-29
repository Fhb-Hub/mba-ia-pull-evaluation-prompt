"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})

        assert "system_prompt" in prompt, "Campo 'system_prompt' não encontrado"
        assert prompt["system_prompt"].strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt.get("system_prompt", "")

        role_indicators = ["Você é um", "Você é uma", "Act as", "Your role"]
        has_role = any(indicator in system_prompt for indicator in role_indicators)

        assert has_role, "Prompt não define uma persona/role claramente"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt.get("system_prompt", "")

        format_indicators = ["user story", "User Story", "Given-When-Then", "formato", "FORMATO"]
        has_format = any(indicator in system_prompt for indicator in format_indicators)

        assert has_format, "Prompt não menciona formato de User Story"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt.get("system_prompt", "")

        example_indicators = ["Exemplo", "EXAMPLE", "exemplo", "Exemplo 1", "### Exemplo"]
        has_examples = any(indicator in system_prompt for indicator in example_indicators)

        assert has_examples, "Prompt não contém exemplos few-shot"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt.get("system_prompt", "")

        assert "[TODO]" not in system_prompt, "Prompt contém [TODO] não resolvido"
        assert "TODO:" not in system_prompt, "Prompt contém TODO: não resolvido"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})

        techniques = prompt.get("techniques_applied", [])

        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"

    def test_metadata_structure(self):
        """Verifica se o prompt possui todos os campos obrigatórios."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt = prompts.get("bug_to_user_story_v2", {})

        # Verificar campos obrigatórios no nível top
        assert "tags" in prompt, "Campo 'tags' não encontrado"
        assert "version" in prompt, "Campo 'version' não encontrado"
        assert "techniques_applied" in prompt, "Campo 'techniques_applied' não encontrado"
        assert "system_prompt" in prompt, "Campo 'system_prompt' não encontrado"
        assert "user_prompt" in prompt, "Campo 'user_prompt' não encontrado"

        # Verificar tipos
        assert isinstance(prompt["tags"], list), "tags deve ser uma lista"
        assert isinstance(prompt["techniques_applied"], list), "techniques_applied deve ser uma lista"
        assert isinstance(prompt["version"], str), "version deve ser uma string"
        assert isinstance(prompt["system_prompt"], str), "system_prompt deve ser uma string"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])