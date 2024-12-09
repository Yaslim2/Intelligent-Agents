from Environment import Environment
from ModelReactiveAgent import ModelReactiveAgent
from SimpleReactiveAgent import SimpleReactiveAgent
import threading
import copy

def initialize_world(world_size, dirt_config, obstacle_config):
    """Inicializa o mundo com as configurações de sujeira e obstáculos."""
    world = Environment(world_size[0], world_size[1], obstacle_config)
    print(dirt_config['cols'])
    world.addDirt(dirt_columns=dirt_config['cols'], dirt_rows=dirt_config['rows'])
    return world

def simulate_simple_agent(world, agent_position):
    """Executa a limpeza com um agente reativo simples."""
    agent = SimpleReactiveAgent(world, agent_position)
    cleaning_thread = threading.Thread(target=agent.startCleaning)
    cleaning_thread.start()
    agent.stopCleaning()
    cleaning_thread.join()
    return agent

def simulate_model_agent(world, agent_position):
    """Executa a limpeza com um agente reativo baseado em modelo."""
    agent = ModelReactiveAgent(world, agent_position)
    agent.startCleaning()
    return agent

def display_world_state(title, world):
    """Exibe o estado atual do mundo no console."""
    print(f"\n# {title}:\n")
    for row in world.grid:
        print(row)
    print("\n##############################\n")

def calculate_average_scores(scores):
    """Calcula a pontuação média para cada métrica."""
    return [sum(score_list) / len(score_list) for score_list in zip(*scores)]

def run_simulation(world_size, dirt_configs, obstacle_configs, agent_positions):
    """Executa as simulações para todas as configurações."""
    simple_agent_scores = []
    model_agent_scores = []

    for idx, (dirt_config, obstacle_config, agent_position) in enumerate(zip(dirt_configs, obstacle_configs, agent_positions)):
        # Configura o mundo para a simulação
        initial_world = initialize_world(world_size, dirt_config, obstacle_config)
        simple_world_copy = copy.deepcopy(initial_world)
        model_world_copy = copy.deepcopy(initial_world)

        display_world_state(f"Simulação {idx + 1} - Mundo antes da limpeza", initial_world)

        # Executa a simulação para os agentes
        simple_agent = simulate_simple_agent(simple_world_copy, agent_position)
        model_agent = simulate_model_agent(model_world_copy, agent_position)

        # Registra as pontuações
        simple_agent_scores.append((simple_agent.score_1, simple_agent.score_2))
        model_agent_scores.append((model_agent.score_1, model_agent.score_2))

        display_world_state(f"Simulação {idx + 1} - Mundo após limpeza (Agente reativo simples)", simple_world_copy)
        display_world_state(f"Simulação {idx + 1} - Mundo após limpeza (Agente reativo baseado em modelo)", model_world_copy)

        # Exibe as pontuações da simulação atual
        print(f"Simulação {idx + 1} (Agente reativo simples): Métrica 1: {simple_agent.score_1}, Métrica 2: {simple_agent.score_2}")
        print(f"Simulação {idx + 1} (Agente reativo baseado em modelo): Métrica 1: {model_agent.score_1}, Métrica 2: {model_agent.score_2}")
        print("\n##############################\n")

    # Calcula as pontuações médias e exibe os resultados finais
    simple_avg_scores = calculate_average_scores(simple_agent_scores)
    model_avg_scores = calculate_average_scores(model_agent_scores)
    print(f"Resultados Finais:")
    print(f"Agente reativo simples - Média Métrica 1: {simple_avg_scores[0]}, Média Métrica 2: {simple_avg_scores[1]}")
    print(f"Agente reativo baseado em modelo - Média Métrica 1: {model_avg_scores[0]}, Média Métrica 2: {model_avg_scores[1]}")

if __name__ == "__main__":
    # Configurações do mundo
    world_size = (6, 6)

    # Configurações para diferentes simulações
    dirt_configs = [
        {'cols': [1, 2, 4], 'rows': [0, 3]},  # Configuração 1
        {'cols': [0, 5], 'rows': [1, 2, 4]},  # Configuração 2
        {'cols': [2, 3], 'rows': [1, 5]},     # Configuração 3
    ]

    obstacle_configs = [
        [[0, 1], [4, 5], [2, 3]],  # Obstáculos para simulação 1
        [[1, 4], [3, 0], [5, 2]],  # Obstáculos para simulação 2
        [[2, 2], [4, 1], [3, 5]],  # Obstáculos para simulação 3
    ]

    # Posições iniciais dos agentes para diferentes simulações
    agent_positions = [
        [0, 5],  # Posição do agente na simulação 1
        [5, 0],  # Posição do agente na simulação 2
        [3, 3],  # Posição do agente na simulação 3
    ]

    # Inicia as simulações
    run_simulation(world_size, dirt_configs, obstacle_configs, agent_positions)