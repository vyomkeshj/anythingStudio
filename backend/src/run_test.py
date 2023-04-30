import asyncio
from sanic import Sanic
from sanic.response import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Sanic("huggingface_example")

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

@app.route("/classify", methods=["POST"])
async def classify(request):
    text = request.json["text"]
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    loop = asyncio.get_event_loop()
    outputs = await loop.run_in_executor(None, model, inputs)
    predictions = outputs.logits.argmax(dim=1).tolist()

    return json({"predictions": predictions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)