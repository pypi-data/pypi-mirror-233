import openai
import json


class EvalSummary:
    char_limit_for_japanese = 4000
    char_limit_for_english = 6000

    def __init__(self, api_key_path, data_path):
        with open(api_key_path) as f:
            self.api_key = f.read().strip()
        with open(data_path, 'r', encoding='utf-8') as f:
            self.japanese_data = json.load(f)
        openai.api_key = self.api_key

    def split_data_by_char_limit(self, data, char_limit):
        chunks = []
        current_chunk = []
        current_char_count = 0
        for entry in data:
            answer_length = len(entry['answer'])

            # 現在の累計文字数と新しい回答の文字数の合計が制限を超える場合、新しいチャンクを開始します
            if current_char_count + answer_length > char_limit:
                chunks.append(current_chunk)
                current_chunk = []
                current_char_count = 0

            current_chunk.append(entry)
            current_char_count += answer_length

        # 最後のチャンクを追加します（もし残りがあれば）
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def summarise_extract_character(self, chunks):
        responses = []
        for chunk in chunks:
            prompt = f"""I will give you a dictionary object with pairs of questions and answers extracted from an interview of a person. Please analyze the character of that person.
            {chunk}"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}
                ],
                temperature=0,
            )
            responses.append(response.choices[0]["message"]["content"])
        return responses

    def split_summaries_by_char_limit(self, dataset, char_limit=6000):
        chunks = []
        current_chunk = ""
        current_length = 0

        for entry in dataset:
            entry_length = len(entry)

            if current_length + entry_length > char_limit:
                # 現在のチャンクを保存
                chunks.append(current_chunk)
                # チャンクとカウンターをリセット
                current_chunk = ""
                current_length = 0

            # エントリを現在のチャンクに追加
            current_chunk += entry + "\n\n"  # エントリ間に空行を追加
            current_length += entry_length

        # 最後のチャンクを追加
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def summarise_split_summary(self, chunks):
        responses = chunks[:]
        previous_length = float('inf')

        while len(responses) < previous_length:
            previous_length = len(responses)
            new_responses = []

            for chunk in responses:
                prompt = f"""The following text describes the personality and principles of a certain individual. Please extract the characteristics of this person from this long text.
                {chunk}"""

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{prompt}"}
                    ],
                    temperature=0,
                )
                new_responses.append(response.choices[0]["message"]["content"])

            responses = self.split_summaries_by_char_limit(new_responses, EvalSummary.char_limit_for_english)
        return responses

    def run(self):
        splits_japanese = self.split_data_by_char_limit(self.japanese_data, EvalSummary.char_limit_for_japanese)
        split_summary = self.summarise_extract_character(splits_japanese)
        splits_english_summary = self.split_summaries_by_char_limit(split_summary, EvalSummary.char_limit_for_english)
        summary = self.summarise_split_summary(splits_english_summary)

        with open('character_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary[0])
        with open('split_summary.json', 'w', encoding='utf-8') as f:
            json.dump(split_summary, f, ensure_ascii=False, indent=4)

        print(split_summary)
        print(summary)

