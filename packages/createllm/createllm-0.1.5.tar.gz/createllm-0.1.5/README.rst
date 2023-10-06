Python package that let you create own transformers based models on your own data

Example
---------------

from createllm import CreateLLM
path = "File.txt"
model = CreateLLM.GPTTrainer(path)
model = model.trainer()


SavedModel = CreateLLM.LLMModel("Path to Model folder")
print(SavedModel.generate("Add Your Text Here"))