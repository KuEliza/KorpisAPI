from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import logging
import tempfile

from database import SessionLocal
from etl_pipeline import ETLPipeline

router = APIRouter(prefix="/etl", tags=["ETL процессы"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def process_etl_file(file: UploadFile, db: Session):
    # Проверка формата файла
    allowed_extensions = {'.csv', '.xls', '.xlsx'}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат файла. Разрешенные форматы: {', '.join(allowed_extensions)}"
        )

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        content = file.file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Запуск ETL процесса только для сотрудников
        pipeline = ETLPipeline(temp_file_path, db, model_type="employees")
        validation_errors, added_count = pipeline.run()

        # Проверяем, есть ли КРИТИЧЕСКИЕ ошибки валидации
        critical_errors = bool(
            validation_errors['missing_columns'] or
            validation_errors['duplicate_ids']
        )

        response_data = {
            "Имя файла": file.filename,
            "Тип данных": "employees",
            "Ошибки валидации": validation_errors,
            "Добавлено записей": added_count
        }

        if critical_errors:
            response_data.update({
                "Статус": "error",
                "Текст": "Файл содержит критические ошибки валидации"
            })
            raise HTTPException(
                status_code=400,
                detail=response_data
            )

        # Успешная обработка (возможно с некритическими ошибками)
        response_data.update({
            "Статус": "success",
            "Текст": "Файл успешно обработан"
        })
        return response_data

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/upload-employees", summary="Загрузка сотрудников из файла")
async def upload_employees(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        return process_etl_file(file, db)
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Ошибка при обработке файла сотрудников: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера при обработке файла: {str(e)}"
        )
