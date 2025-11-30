

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import SensorReading, SensorReadingWithML, StatusResponse
from .database import save_measurement, get_latest_measurements, get_all_measurements
from .ml.models_loader import get_ml_models

app = FastAPI(
    title="SmartAir Guardian API",
    description="API para ingestão de dados de sensores de qualidade do ar e análise com IA.",
    version="1.0.0",
)

# CORS básico para testes locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_models_on_startup():
    # garante que os modelos estão carregados
    get_ml_models()
    print("Modelos de IA carregados com sucesso.")


@app.get("/", response_model=StatusResponse)
def root_status():
    total = len(get_all_measurements())
    return StatusResponse(status="ok", total_readings=total)


@app.post("/ingest", response_model=SensorReadingWithML)
def ingest_reading(reading: SensorReading):
    """
    Endpoint de ingestão de dados do sensor.
    Aplica os modelos de IA e persiste a leitura enriquecida.
    """
    ml = get_ml_models()
    preds = ml.predict_all(
        co2=reading.co2,
        pm25=reading.pm25,
        temp=reading.temp,
        humidity=reading.humidity,
    )

    enriched = SensorReadingWithML(
        **reading.model_dump(),
        is_anomaly=preds["is_anomaly"],
        risk_level=preds["risk_level"],
        co2_next_pred=preds["co2_next_pred"],
    )
    save_measurement(enriched)
    return enriched


@app.get("/readings/latest", response_model=list[SensorReadingWithML])
def get_latest(limit: int = 20):
    """
    Retorna as últimas leituras com informações de IA.
    """
    return get_latest_measurements(limit=limit)
