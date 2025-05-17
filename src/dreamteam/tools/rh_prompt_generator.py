import yaml

def generate_prompts(pdg_input, output_dir):
    """Génère agents.yaml et tasks.yaml pour une subteam"""
    with open(pdg_input) as f:
        data = yaml.safe_load(f)
    # TODO: implémenter logique
    print("Prompts générés vers", output_dir)
