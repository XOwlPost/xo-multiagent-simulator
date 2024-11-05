from fabric import task

@task
def setup_docker_containers(c):
    # Stop and Remove Existing Containers
    c.run("docker stop agent0-container || true")
    c.run("docker rm agent0-container || true")
    c.run("docker stop aider-container || true")
    c.run("docker rm aider-container || true")

    # Create a Docker Network
    c.run("docker network create agent-network || true")

    # Run Containers
    c.run("docker run -d --name agent0-container --network agent-network frdel/agent-zero-exe")
    c.run("docker run -d --name aider-container --network agent-network -e OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> paulgauthier/aider-full")

    # Model Configuration
    c.run("python llm_models_orchestrator.py")  # Assuming llm_models_orchestrator.py is in the same directory

    # Health Check
    c.run("docker exec agent0-container ping -c 4 aider-container")

    # Optional Local LLMs
    c.run("if [ -d /media/pop/YUMI/LocalLLMs ]; then echo 'Local LLMs found'; fi")
