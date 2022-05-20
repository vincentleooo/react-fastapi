import uvicorn
import pickle
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import librosa
from model.music_genre_classification.predict_audio import CNN
from tqdm import tqdm
import pandas as pd
import torch.nn.functional as F

# Initializing the fast API server
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Music(BaseModel):
    path: str

sr = 22050
SAMPLES_PER_SLICE = 63945
N_MFCC = 60

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load("model/music_genre_classification/Models/Final_2D_CNN.pt", map_location=device)

model.eval()

def prediction(input):
    data, sr = librosa.load(input)

    mfcc_list = []

    for s in tqdm(range(int(len(data) / SAMPLES_PER_SLICE))):
        start_sample = SAMPLES_PER_SLICE * s
        end_sample = start_sample + SAMPLES_PER_SLICE
        song = data
        mfcc = librosa.feature.mfcc(
            y=song[start_sample:end_sample], sr=sr, n_mfcc=N_MFCC
        )
        mfcc = mfcc.T
        mfcc_list.append(mfcc.tolist())
        
    pred_labels = []

    for i in mfcc_list:
        tensorised = torch.tensor(i)
        output = model(tensorised.unsqueeze(0).to(device)).detach()
        pred_label = torch.argmax(F.softmax(output, dim=1))
        pred_labels.append(pred_label.item())

    genres_list = [
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock",
    ]

    pred_cats = []

    for i in pred_labels:
        pred_cats.append(genres_list[i])

    return f"Predictions for {input}:\n{pd.Series(pred_cats).value_counts(normalize=True).to_string(index=True)}"

@app.post("/predict/")
async def predict(input: Music):
    path = input.path
    pred = prediction(path)
    return {"message": pred}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')