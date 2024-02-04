from textSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer
from transformers import pipeline


class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
    
    def predict(self,text):
        """
        The `predict` function takes in a text as input, tokenizes it, and uses a pre-trained model to
        generate a summary of the text. The generated summary is then returned as output.
        
        :param text: The `text` parameter is the input dialogue that you want to summarize. It can be a
        string containing the conversation or dialogue that you want to summarize
        :return: the generated summary text.
        """
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": 128}

        pipe = pipeline("summarization", model=self.config.model_path,tokenizer=tokenizer)

        print("Dialogue:")
        print(text)

        output = pipe(text, **gen_kwargs)[0]["summary_text"]
        print("\nModel Summary:")
        print(output)

        return output