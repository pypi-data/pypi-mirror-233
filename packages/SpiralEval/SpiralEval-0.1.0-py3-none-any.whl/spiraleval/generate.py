import openai
import json
import random
import copy


class EvalGenerateDataset:
    def __init__(self, api_key_path, char_summary_path, data_path):
        with open(api_key_path) as f:
            self.api_key = f.read().strip()
        with open(data_path, 'r', encoding='utf-8') as f:
            self.japanese_data = json.load(f)
        with open(char_summary_path, "r", encoding="utf-8") as file:
            self.character_summary = file.read()

        openai.api_key = self.api_key

    def random_extract_questions(self, reference, extract_numbers: int):
        """
        Randomly extract 20 questions from the reference.
        This 20 questions would be used on the evaluation.
        """
        random.seed(42)
        selected_pairs = random.sample(reference, min(extract_numbers, len(reference)))
        return selected_pairs

    def generate_evaluation(self, qa_pairs: dict, character_summary: str, sample_selected_answers, difficulty: bool):
        """
        Generate answers to 20 questions so that we can easily distinguish
        answers from the real person and answers from LLM
        if difficulty is True, we get easy_answers. Otherwise, we get hard_answers
        """
        # Extract all answers
        questions = [item["question"] for item in qa_pairs]
        answers = []
        if difficulty:
            difficulty_choice = 'Please answer in a way that person would definitely not answer using Japanese. Please increase the variations in the answers, such as speaking style, dialect, sentence endings, affirmations, negations, etc. These can be thought of as some of the vectors for possible ways to answer. When you respond, please choose only one from these vectors and reflect it in your answer.'
        else:
            difficulty_choice = "I want you to answer in a way that seems like that person at first glance, but upon closer examination, that person wouldn't answer that way. Answer in Japanese. When answering, please try to mimic the actual speaking style of the person to the extent that it's not so difficult to distinguish."
        for a_question in questions:
            generate_prompt = f"""This is a summary of someone's character traits. {character_summary}  The following sentence is an actual statement made by that person. {sample_selected_answers} I will give you a question. {a_question} {difficulty_choice} Please answer in only one way.
            === Example1 ===
            私はカレーが好きです。
            === end of example1 ===
            Let's begin!
            """
            easy_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{generate_prompt}"}
                ],
                temperature=0,
            )
            answers.append(easy_response.choices[0]["message"]["content"])
        new_qa_pairs = copy.deepcopy(qa_pairs)
        for i, item in enumerate(new_qa_pairs):
            item["answer"] = answers[i]
        return new_qa_pairs

    def run(self, number_pairs=20):
        answers = [item['answer'] for item in self.japanese_data]
        sample_selected_answers = random.sample(answers, 10)

        question_answers_pairs = self.random_extract_questions(self.japanese_data, number_pairs)

        easy_pairs = self.generate_evaluation(question_answers_pairs, self.character_summary, sample_selected_answers, True)
        hard_pairs = self.generate_evaluation(question_answers_pairs, self.character_summary, sample_selected_answers, False)

        evaluation = question_answers_pairs + easy_pairs + hard_pairs
        with open("evaluation_for_spiral_eval.json", "w", encoding="utf-8") as file:
            json.dump(evaluation, file, ensure_ascii=False, indent=4)

