# This script initializes TeLLMgramBot with useful functions
import os, re

INITIAL_CONFIG = {
    'bot_username'   : 'test_bot',
    'bot_owner'      : '<YOUR USERNAME>',
    'bot_name'       : 'Test Bot',
    'bot_nickname'   : 'Testy',
    'bot_initials'   : 'TB',
    'chat_model'     : 'gpt-3.5-turbo',
    'url_model'      : 'gpt-4',
    'token_limit'    : None,
    'persona_temp'   : None,
    'persona_prompt' : 'You are a test harness bot.'
}

# Checks for important directories to configure for TeLLMgramBot
def ensure_directories():
    app_base_path = os.environ.get('TELLMGRAMBOT_APP_PATH', os.getcwd())

    # Update the environment variable with the cleaned-up path
    os.environ['TELLMGRAMBOT_APP_PATH'] = app_base_path

    # Create necessary directories
    directories = [
        os.path.join(app_base_path, 'sessionlogs'),
        os.path.join(app_base_path, 'errorlogs'),
        os.path.join(app_base_path, 'prompts'),
        # Add more as needed
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Ensure configuration file is created that defines bot information
def ensure_config(file='config.yaml'):
    if not os.path.exists(file):
        # Create a basic TeLLMgramBot configuration by filename
        with open(file, 'w') as f:
            # Add configuration with default values except prompt:
            for parameter, value in INITIAL_CONFIG.items():
                if parameter == 'persona_prompt': next
                else: # Write parameter, with optional comment if no value
                    f.write('%s : %s\n' % (
                        parameter.ljust(12),
                        value if value else '# Optional, see README'
                    ))
        print(f"Created new configuration file: '{file}'")

# Ensure prompt file is created that defines bot personality
def ensure_prompt(file='prompts/starter.prmpt'):
    if not os.path.exists(file):
        # Create a basic TeLLMgramBot prompt by filename
        with open(file, 'w') as f:
            f.write(INITIAL_CONFIG['persona_prompt'])
        print(f"Created new prompt file: '{file}'")

# Investigates three API keys by file or environment variable
def ensure_keys():
    # List each key file and URL if it does not exist for more information
    key_files = {
        'openai.key'     : 'https://platform.openai.com/account/api-keys',
        'telegram.key'   : 'https://core.telegram.org/api',
        'virustotal.key' : 'https://developers.virustotal.com/reference/overview'
    }

    # Create key files and environment variables
    for key_file, url in key_files.items():
        path = os.path.join(os.environ['TELLMGRAMBOT_APP_PATH'], key_file)
        key = re.sub("\..+", "", key_file).upper()  # Uppercase with .key removed
        env_var = f"TELLMGRAMBOT_{key}_API_KEY"

        # Ensures the specified key file is created and populated by user
        if not os.path.exists(path):
            # Create a basic ~.key file
            with open(path, 'w') as f:
                f.write(f"YOUR {key} API KEY HERE - {url}\n")
            print(f"Created new API key file: '{key_file}'")

        # If the environment variable is undefined, set by API key file
        if os.environ.get(env_var) is None:
            try:
                with open(path, 'r') as f:
                    os.environ[env_var] = f.read().strip()
                    print(f"Loaded secret for {env_var}")
            except FileNotFoundError:
                print(f"Key file not found for {env_var}")
            except Exception as e:
                print(f"An error occurred while loading {env_var}: {e}")

# Performs the whole setup, with the option to enter configuration filename and prompt filename
def ensure_setup(config_file='config.yaml', prompt_file='prompts/starter.prmpt'):
    ensure_directories()
    ensure_config(config_file)
    ensure_prompt(prompt_file)
    ensure_keys()

# Run this script if the first time setting up TeLLMgramBot
if __name__ == '__main__':
    ensure_setup()
