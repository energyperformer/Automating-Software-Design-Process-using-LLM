
Doc for project:
https://www.notion.so/Project-11c59cd34c37806ab046daee81d03d76


This project aims to automate the software design process using Large Language Models (LLMs). It leverages the power of AI to assist in various stages of software development, from requirements gathering to code generation.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package manager)
- Bash shell (for running the setup and project scripts)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Automating-Software-Design-Process-using-LLM-s.git
   cd Automating-Software-Design-Process-using-LLM-s
   ```

2. Run the setup script:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```
   This script will create a virtual environment, activate it, and install all the required dependencies from the `requirements.txt` file.

     ```

## Usage

1. To run the project, use the provided `run_project.sh` script:
   ```
   chmod +x run_project.sh
   ./run_project.sh
   ```

2. Follow the prompts to input your project requirements and preferences.

3. The system will generate various artifacts, including:
   - System architecture diagrams
   - Class diagrams
   - Sequence diagrams
   - API specifications
   - Code snippets

4. Review the generated output in the `output` directory.

## Project Structure
```
├── run_project.sh
├── setup.sh
├── requirements.txt
├── src/
│ ├── requirements_analysis.py
│ ├── architecture_design.py
│ ├── class_design.py
│ ├── sequence_diagram_generator.py
│ ├── api_spec_generator.py
│ └── code_generator.py
├── utils/
│ ├── openai_utils.py
│ └── diagram_utils.py
├── output/
│ ├── diagrams/
│ ├── api_specs/
│ └── code/
├── tests/
├── .env
└── README.md
```
