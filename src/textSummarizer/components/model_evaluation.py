from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch
import pandas as pd
from tqdm import tqdm
from textSummarizer.entity import ModelEvaluationConfig

# The ModelEvaluation class is used for evaluating the performance of a machine learning model.
class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
    
    def generate_batch_sized_chunks(self,list_of_elements, batch_size):
        """
        The function generates batch-sized chunks from a given list of elements.
        
        :param list_of_elements: The list of elements that you want to split into smaller batches
        :param batch_size: The batch_size parameter determines the number of elements in each
        batch-sized chunk
        """
        #split the dataset into smaller batches that we can process simultaneously
        #yield successive batch-sized chunks from list_of_elements."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]

    
    def calculate_metric_on_test_ds(self,dataset, metric, model, tokenizer, 
                               batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
                               column_text="article", 
                               column_summary="highlights"):
        
        """
        The function `calculate_metric_on_test_ds` takes in a dataset, a metric, a model, a tokenizer,
        and other optional parameters, and calculates a metric score (e.g., ROUGE) on the test dataset
        using the model's generated summaries and the target summaries.
        
        :param dataset: The dataset parameter is the test dataset that contains the articles and their
        corresponding summaries. It should be a pandas DataFrame or any other data structure that can be
        indexed using column names
        :param metric: The `metric` parameter is an instance of a metric class that is used to evaluate
        the generated summaries. It should have methods such as `add_batch()` to add predictions and
        references, and `compute()` to compute the metric score
        :param model: The `model` parameter refers to the pre-trained model that will be used for
        generating summaries. It should be an instance of a model class that has a `generate` method,
        such as a BART or T5 model
        :param tokenizer: The tokenizer is responsible for converting the input text into tokens that
        can be understood by the model. It is used to tokenize the input text and generate input tensors
        for the model
        :param batch_size: The batch_size parameter determines the number of samples that will be
        processed in each iteration. It is used to divide the dataset into smaller batches for efficient
        processing, defaults to 16 (optional)
        :param device: The "device" parameter specifies whether to use the GPU ("cuda") or CPU ("cpu")
        for computation. If a GPU is available, it will be used by default
        :param column_text: The name of the column in the dataset that contains the text data
        (articles), defaults to article (optional)
        :param column_summary: The `column_summary` parameter is used to specify the column name in the
        dataset that contains the target summaries, defaults to highlights (optional)
        :return: the computed ROUGE scores.
        """

        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches), total=len(article_batches)):
            
            inputs = tokenizer(article_batch, max_length=1024,  truncation=True, 
                            padding="max_length", return_tensors="pt")
            
            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                            attention_mask=inputs["attention_mask"].to(device), 
                            length_penalty=0.8, num_beams=8, max_length=128)
            ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''
            
            # Finally, we decode the generated texts, 
            # replace the  token, and add the decoded texts with the references to the metric.
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, 
                                    clean_up_tokenization_spaces=True) 
                for s in summaries]      
            
            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]
            
            
            metric.add_batch(predictions=decoded_summaries, references=target_batch)
            
        #  Finally compute and return the ROUGE scores.
        score = metric.compute()
        return score


    def evaluate(self):
        """
        The function evaluates the performance of a Pegasus model on a test dataset using the ROUGE
        metric and saves the results to a CSV file.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
       
        #loading data 
        dataset_samsum_pt = load_from_disk(self.config.data_path)


        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
  
        rouge_metric = load_metric('rouge')

        score = self.calculate_metric_on_test_ds(
        dataset_samsum_pt['test'][0:10], rouge_metric, model_pegasus, tokenizer, batch_size = 2, column_text = 'dialogue', column_summary= 'summary'
            )

        rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

        df = pd.DataFrame(rouge_dict, index = ['pegasus'] )
        df.to_csv(self.config.metric_file_name, index=False)