from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import datasets

def fine_tune_model(train_path, valid_path, model_name="gpt2"):
    """
    Fine-tunes a pretrained model on custom data.
    """
    # Load dataset
    train_dataset = datasets.load_dataset('json', data_files=train_path, split='train')
    valid_dataset = datasets.load_dataset('json', data_files=valid_path, split='validation')

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize data
    def tokenize_data(batch):
        return tokenizer(batch['text'], truncation=True, padding="max_length", max_length=512)

    train_dataset = train_dataset.map(tokenize_data, batched=True)
    valid_dataset = valid_dataset.map(tokenize_data, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        num_train_epochs=3,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
    )

    trainer.train()
    return model
