# Import necessary libraries
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset
import os
import torch
from sklearn.model_selection import train_test_split

def load_data(data_folder):
    """
    Load text data from files in the specified folder.
    
    Args:
    data_folder (str): Path to the folder containing text files.
    
    Returns:
    list: A list of text strings from the files.
    """
    texts = []
    for txt_file in os.listdir(data_folder):
        if txt_file.endswith(".txt"):
            with open(os.path.join(data_folder, txt_file), "r") as f:
                texts.append(f.read())
    return texts

def prepare_dataset(texts):
    """
    Prepare the dataset for training by creating input-label pairs.
    
    Args:
    texts (list): List of text strings.
    
    Returns:
    Dataset: A Hugging Face Dataset object containing input-label pairs.
    """
    inputs = ["summarize: " + text for text in texts]
    labels = ["UML code for: " + text for text in texts]
    
    data = {"input_text": inputs, "label_text": labels}
    return Dataset.from_dict(data)

def train_model():
    """
    Train the T5 model on the prepared dataset.
    
    This function loads the data, prepares the dataset, sets up the model and trainer,
    and then trains the model. The trained model is saved after training.
    """
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    
    texts = load_data("data/processed_cleaned/")
    dataset = prepare_dataset(texts)
    
    train_texts, test_texts = train_test_split(dataset, test_size=0.2)
    train_dataset = prepare_dataset(train_texts)
    test_dataset = prepare_dataset(test_texts)

    def preprocess_function(examples):
        """
        Tokenize the input and label texts.
        
        Args:
        examples (dict): Dictionary containing input and label texts.
        
        Returns:
        dict: Tokenized inputs with labels.
        """
        inputs = tokenizer(examples["input_text"], padding="max_length", max_length=512, truncation=True)
        labels = tokenizer(examples["label_text"], padding="max_length", max_length=512, truncation=True)
        inputs["labels"] = labels["input_ids"]
        return inputs

    train_dataset = train_dataset.map(preprocess_function, batched=True)
    test_dataset = test_dataset.map(preprocess_function, batched=True)
    
    training_args = TrainingArguments(
        output_dir='./models/finetuned_llm',
        evaluation_strategy="steps",
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        save_steps=1000,
        save_total_limit=2,
        num_train_epochs=5,
        logging_dir='./logs',
        logging_steps=500,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()

    trainer.save_model("./models/finetuned_llm")
    tokenizer.save_pretrained("./models/finetuned_llm")
    print("Model training complete and saved!")

if __name__ == "__main__":
    train_model()