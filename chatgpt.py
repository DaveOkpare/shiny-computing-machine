import os
import re
from time import sleep

import openai
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = os.getcwd()
CONFIG = os.path.join(BASE_PATH, ".env")
KEY = "OPEN_AI_KEY"
FILE_INPUT = "/Users/RichesofGod/PycharmProjects/AI/CLI/main.py"
START_LINE = 11
END_LINE = 20


class OpenAI:

    @staticmethod
    def create_env_file(OPENAI_API_KEY):
        if os.path.exists(CONFIG):
            with open(CONFIG, "a+") as f:
                f.seek(0)
                data = f.read()
                if "OPENAI_API_KEY" in data:
                    return False
                if len(data) > 0:
                    f.write("\n")
                print("Creating environment variable file ...\n\n")
                f.write(f"OPENAI_API_KEY={OPENAI_API_KEY}")
                return True

    def initialize_open_ai(self):
        if self.create_env_file(KEY):
            load_dotenv()
            sleep(5)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def read_file(path: str, start_line: int = None, end_line: int = None):
        with open(path, 'r') as f:
            data = f.readlines()

            if start_line is None:
                start_at = 0
            if end_line is None:
                end_at = len(data)
            else:
                start_at = start_line - 1
                end_at = end_line

            line_number = range(start_at, end_at)
            lines = []

            for i, line in enumerate(data):
                if i in line_number:
                    lines.append(line)
                elif i > line_number[-1]:
                    break
        output = "".join(lines)
        return output

    def generate_prompt(self, file_path, start_at, end_at):
        file_input = self.read_file(file_path, start_at, end_at)
        prompt = "# Python 3 \n"
        prompt += file_input
        prompt += "\n\n# Explanation of what the code does\n\n#"
        return prompt

    def get_response(self):
        self.initialize_open_ai()
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=self.generate_prompt(FILE_INPUT, START_LINE, END_LINE),
            temperature=0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n#"]
        )
        output = response['choices'][0]['text']
        clean_output = re.sub(r'#', '', output)
        return clean_output
