import pandas as pd
from sqlalchemy.orm import Session
import logging
from typing import Dict, List, Any
import re

import models

logger = logging.getLogger("barista_api")


class ETLPipeline:
    def __init__(self, file_path: str, db: Session, model_type: str = "employees"):
        self.file_path = file_path
        self.db = db
        self.model_type = model_type
        self.data = None

        # Только модель сотрудников
        self.model_mapping = {
            'employees': models.Employee,
        }

        # Только обязательные поля для сотрудников
        self.required_fields = {
            'employees': ['id', 'department_id', 'full_name', 'position', 'workplace_id', 'hire_date'],
        }

    def extract(self) -> pd.DataFrame:
        logger.info(f"Начало извлечения данных из {self.file_path} для модели {self.model_type}")
        try:
            if self.file_path.endswith(('.xls', '.xlsx')):
                self.data = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
            else:
                raise ValueError("Неподдерживаемый формат файла")

            logger.info(f"Успешно извлечено {len(self.data)} строк")
            self.data.columns = self.data.columns.str.lower().str.strip()
            return self.data
        except Exception as e:
            logger.error(f"Ошибка извлечения: {e}")
            raise

    def validate(self) -> Dict[str, List[str]]:
        logger.info(f"Начало валидации данных для модели {self.model_type}")

        errors = {
            'missing_columns': [],
            'missing_values': [],
            'invalid_emails': [],
            'invalid_dates': [],
            'foreign_key_errors': [],
            'duplicate_ids': []
        }

        # Проверка наличия обязательных столбцов
        required = self.required_fields.get(self.model_type, [])
        for field in required:
            if field not in self.data.columns:
                errors['missing_columns'].append(f"Отсутствует обязательный столбец: {field}")

        if errors['missing_columns']:
            return errors

        # Проверка пропущенных значений
        for field in required:
            missing_count = self.data[field].isna().sum()
            if missing_count > 0:
                errors['missing_values'].append(f"{field}: {missing_count} пропущенных значений")

        # Проверка email
        if 'email' in self.data.columns:
            email_rows = self.data['email'].notna()
            if email_rows.any():
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                invalid_emails = self.data.loc[email_rows, 'email'].apply(
                    lambda x: not bool(re.match(email_pattern, str(x)))
                ).sum()
                if invalid_emails > 0:
                    errors['invalid_emails'].append(f"Найдено {invalid_emails} некорректных email")

        # Проверка дат
        date_fields = [col for col in self.data.columns if 'date' in col]
        for field in date_fields:
            if field in self.data.columns:
                try:
                    pd.to_datetime(self.data[field], errors='raise')
                except:
                    errors['invalid_dates'].append(f"Некорректный формат даты в поле {field}")

        # Проверка внешних ключей
        self._validate_foreign_keys(errors)

        # Проверка дубликатов ID
        if 'id' in self.data.columns:
            duplicate_ids = self.data['id'].duplicated().sum()
            if duplicate_ids > 0:
                errors['duplicate_ids'].append(f"Найдено {duplicate_ids} дублирующихся ID")

        return errors

    def _validate_foreign_keys(self, errors: Dict[str, List[str]]):
        # Только для сотрудников
        if self.model_type == 'employees':
            # Проверка department_id
            if 'department_id' in self.data.columns:
                valid_departments = {str(dept[0]) for dept in self.db.query(models.Department.id).all()}
                invalid_dept = self.data[~self.data['department_id'].isin(valid_departments)]['department_id'].unique()
                if len(invalid_dept) > 0:
                    errors['foreign_key_errors'].append(f"Несуществующие department_id: {list(invalid_dept)}")

            # Проверка workplace_id
            if 'workplace_id' in self.data.columns:
                valid_workplaces = {str(wp[0]) for wp in self.db.query(models.Workplace.id).all()}
                invalid_wp = self.data[~self.data['workplace_id'].isin(valid_workplaces)]['workplace_id'].unique()
                if len(invalid_wp) > 0:
                    errors['foreign_key_errors'].append(f"Несуществующие workplace_id: {list(invalid_wp)}")

    def transform(self) -> pd.DataFrame:
        logger.info(f"Начало трансформации данных для модели {self.model_type}")

        # Очистка текстовых данных
        text_columns = self.data.select_dtypes(include=['object']).columns
        for col in text_columns:
            self.data[col] = self.data[col].replace(['nan', 'null', 'None', ''], pd.NA)
            mask = self.data[col].notna()
            self.data.loc[mask, col] = self.data.loc[mask, col].astype(str).str.strip()

        # Обработка дат
        date_columns = [col for col in self.data.columns if 'date' in col]
        for col in date_columns:
            self.data[col] = pd.to_datetime(self.data[col], errors='coerce').dt.date

        # Приведение ID к строковому типу
        if 'id' in self.data.columns:
            self.data['id'] = self.data['id'].astype(str).str.strip()

        logger.info("Трансформация завершена")
        return self.data

    def load(self) -> int:
        logger.info(f"Начало загрузки данных для модели {self.model_type}")

        model_class = self.model_mapping.get(self.model_type)
        if not model_class:
            raise ValueError(f"Неизвестный тип модели: {self.model_type}")

        added_count = 0
        skipped_count = 0

        # Подготовка данных для проверки внешних ключей
        valid_departments = {str(dept[0]) for dept in self.db.query(models.Department.id).all()}
        valid_workplaces = {str(wp[0]) for wp in self.db.query(models.Workplace.id).all()}

        try:
            for _, row in self.data.iterrows():
                try:
                    # Проверяем существование записи с таким ID
                    existing = self.db.query(model_class).filter_by(id=str(row['id'])).first()
                    if existing:
                        skipped_count += 1
                        continue

                    # Проверка внешних ключей
                    department_id = str(row.get('department_id', ''))
                    workplace_id = str(row.get('workplace_id', ''))

                    if department_id not in valid_departments:
                        logger.warning(f"Пропуск строки {row['id']}: несуществующий department_id {department_id}")
                        skipped_count += 1
                        continue

                    if workplace_id not in valid_workplaces:
                        logger.warning(f"Пропуск строки {row['id']}: несуществующий workplace_id {workplace_id}")
                        skipped_count += 1
                        continue

                    # Проверка email
                    if 'email' in row and pd.notna(row['email']):
                        email = str(row['email'])
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, email):
                            logger.warning(f"Пропуск строки {row['id']}: некорректный email {email}")
                            skipped_count += 1
                            continue

                    # Подготовка данных для модели
                    model_data = {}
                    for column in self.data.columns:
                        if column in row and pd.notna(row[column]):
                            model_data[column] = row[column]

                    # Создание объекта модели
                    model_instance = model_class(**model_data)
                    self.db.add(model_instance)
                    added_count += 1

                except Exception as e:
                    logger.warning(f"Ошибка при обработке строки {row.get('id', 'unknown')}: {e}")
                    skipped_count += 1
                    continue

            self.db.commit()
            logger.info(f"Загрузка завершена. Добавлено: {added_count}, Пропущено: {skipped_count}")
            return added_count

        except Exception as e:
            logger.error(f"Ошибка загрузки: {e}")
            self.db.rollback()
            raise

    def run(self):
        logger.info(f"Запуск ETL процесса для модели {self.model_type}")

        # Извлечение
        self.extract()

        # Валидация
        validation_errors = self.validate()

        # Только критические ошибки блокируют загрузку
        critical_errors = bool(validation_errors['missing_columns'] or validation_errors['duplicate_ids'])

        if not critical_errors:
            self.transform()
            added_count = self.load()
        else:
            added_count = 0
            logger.warning("Пропущены этапы трансформации и загрузки из-за критических ошибок валидации")

        return validation_errors, added_count
