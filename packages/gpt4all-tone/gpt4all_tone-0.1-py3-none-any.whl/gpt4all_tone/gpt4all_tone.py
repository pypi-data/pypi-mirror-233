import os
import json
import argparse
from gpt4all import GPT4All

DEFAULT_MODEL_NAME = "orca-mini-3b.ggmlv3.q4_0.bin"
SYSTEM_TEMPLATE = 'Please respond with a numerical value indicating the sentiment of the following text: use 1 for positive, 0 for negative, 0.5 for neutral, and 0.75 for more positive, or 0.25 for more negative.'


class ToneAnalyzer:
    def __init__(self, model_name, input):
        self.model_name = model_name
        self.input = input
        self.model = GPT4All(model_name)

    def run(self):
        with self.model.chat_session(SYSTEM_TEMPLATE):
            prompt = "Is the next text more positive? '" + self.input+ "'. Answer only '1' or '0' without any other words."
            res = self.model.generate(prompt=prompt, max_tokens=5, temp=0.1)
            return res


def parse_arguments():
    parser = argparse.ArgumentParser(description="gpt4all_tone")
    parser.add_argument("--model", help="Specifies the model name. Default is orca-mini-3b.ggmlv3.q4_0.bin", default=DEFAULT_MODEL_NAME)
    parser.add_argument("--input", help="Specifies the input text to analyze.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    analyzer = ToneAnalyzer(args.model, args.input)
    result = analyzer.run()
    print(result)


if __name__ == "__main__":
    main()
