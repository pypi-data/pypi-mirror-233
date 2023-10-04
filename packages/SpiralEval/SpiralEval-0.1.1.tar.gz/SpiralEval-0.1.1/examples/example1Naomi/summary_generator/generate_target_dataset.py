from SpiralEval.spiraleval import EvalGenerateDataset

api_path = '../../../openai_api.txt'
summary_path = 'character_summary.txt'
reference_path = '../../../val_references.json'

eval_generate_dataset = EvalGenerateDataset(api_path, summary_path, reference_path)

eval_generate_dataset.run()
