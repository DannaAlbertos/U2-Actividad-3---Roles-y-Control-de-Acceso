import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRETO = os.environ.get("JWT_SECRET")
if not SECRETO:
    raise RuntimeError("Falta la variable de entorno JWT_SECRET")

ALGORITMO = "HS256"
MINUTOS_VIGENCIA = 30


def crear_token(company_user_id: int, company_id: int) -> str:
    ahora = datetime.now(timezone.utc)
    datos = {
        "companyUserId": company_user_id,
        "companyId": company_id,
        "exp": ahora + timedelta(minutes=MINUTOS_VIGENCIA),
    }
    return jwt.encode(datos, SECRETO, algorithm=ALGORITMO)