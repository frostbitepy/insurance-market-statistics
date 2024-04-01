import io
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder

from database import (
        retrieve_insurer,
        get_financial_exercises_by_insurer,
        upload_financial_exercise,
        get_field_value,
        get_all_field_values
)

from pipeline import (
        generate_dataframes_list,
        process_data,
)

from models import (
        Insurer,
)

router = APIRouter()


@router.get("/insurer")
async def get_all_insurers():
    try:
        return await retrieve_insurer()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exercise/{insurer_id}")
async def get_exercises_by_insurer(insurer_id: str):
    try:
        return await get_financial_exercises_by_insurer(insurer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/field_value/{insurer_id}/{year}/{month}/{field}")
async def get_field_value_route(insurer_id: str, year: int, month: str, field: str):
    value = await get_field_value(insurer_id, year, month, field)
    if value is not None:
        return {"value": value}
    else:
        raise HTTPException(status_code=404, detail="Document not found or field does not exist")
    

@router.get("/all_field_values/{year}/{month}/{field}")
async def get_all_field_values_route(year: int, month: str, field: str):
    try:
        results = await get_all_field_values(year, month, field)
        if results:
            return results
        else:
            raise HTTPException(status_code=404, detail="No documents found for the given year and month")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/exercise")
async def upload_exercise(data: dict):
    try:
        result = await upload_financial_exercise(data)
        return {"inserted_id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/{year}/{month}")
async def process_file(year: int, month: str, file: UploadFile = File(...)):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        try:
            df_list = generate_dataframes_list(io.BytesIO(await file.read()))
            processed_data = [process_data(df, year, month) for df in df_list]
            ids = []
            for data in processed_data:
                id = await upload_financial_exercise(data)
                ids.append(id)
            return {"inserted_ids": ids}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid file format")
    else:
        raise HTTPException(status_code=400, detail="Invalid file format")