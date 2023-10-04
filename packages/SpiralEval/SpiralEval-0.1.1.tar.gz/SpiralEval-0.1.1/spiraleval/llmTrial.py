import json
import pandas as pd
import openai
import random


class EvalLLMTrial:
    def __init__(self, openai_key, character_summary, references_file):
        self.character_summary = character_summary
        self.all_references = self._load_json(references_file)
        openai.api_key = self._load_txt(openai_key)

        # Prompt user for target sentence and store it in target_data format
        self.target_data = self.get_user_input()

    def get_user_input(self):
        question = input("Please enter your target question: ")
        answer = input("Please enter the answer for the target question: ")
        return [{'question': question, 'answer': answer}]

    @staticmethod
    def _load_txt(file_path):
        with open(file_path) as f:
            return f.read().strip()

    @staticmethod
    def _load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def ask_gpt_get_json_result(self, schema, prompt):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}
                ],
                functions=[{"name": "generate_gpt_content", "parameters": schema}],
                function_call={"name": "generate_gpt_content"},
                temperature=0,
            )
        except Exception as e:
            print(f"Error generating content from GPT-4: {e}")
            return None
        try:
            json_result = json.loads(completion.choices[0].message.function_call.arguments)
        except:
            print("Error parsing JSON result.")
            print(completion.choices[0].message.function_call.arguments)
            return None
        return json_result

    def generate_decision_dataframe(self, instruction, references, target_sentence_body):
        references_text = ""
        for i, ref in enumerate(references):
            references_text += f"{i+1}. Question: {ref['question']} Answer: {ref['answer']}\n"

        instruction_1 = instruction
        instruction_2 = """
        The following reference is 10 pairs of question and answer.
        """
        instruction_3 = """
        The following is the target pair of question and answer for judgement.
        """
        target_sentence = f"target_sentence: {target_sentence_body}\n"
        instruction = instruction_1 + instruction_2 + references_text + instruction_3 + target_sentence
        schema = {
            "type": "object",
            "properties": {
                "decision": {"type": "boolean"},
                "reason": {"type": "string"},
            },
            "required": ["decision", "reason"]
        }
        result = self.ask_gpt_get_json_result(schema, instruction)
        return [result['decision'], result['reason']]

    def spiral_eval(self, instruction, target_sentence_body, all_references, n=1):
        # すべてのリファレンスをランダムな順序でシャッフル
        random.seed(42)
        shuffled_references = random.sample(all_references, len(all_references))

        dfs = []
        for i in range(n):
            # シャッフルされたリストから10のリファレンスを取得
            start_index = i * 10
            end_index = start_index + 10
            references = shuffled_references[start_index:end_index]

            decision, reason = self.generate_decision_dataframe(instruction, references, target_sentence_body)
            dfs.append([target_sentence_body, decision, reason, references])
        df = pd.DataFrame(dfs, columns=["target", "result_decision", "result_reason", "references"])
        return df

    def run(self, instruction):
        all_result_df = pd.DataFrame()

        # Process each pair of a question and its answer.
        for item in self.target_data:
            target_sentence_body = item['question'] + ' ' + item['answer']
            result_df = self.spiral_eval(instruction, target_sentence_body, self.all_references, n=1)
            all_result_df = pd.concat([all_result_df, result_df])

            all_result_df.to_csv('llm_result_df_trial.csv', index=False)
