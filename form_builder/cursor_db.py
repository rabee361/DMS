from django.db import connection
import json
from .models import CustomForm


def table_exists(table_name):
    """
    Check if a table with the given name exists in the database
    
    Args:
        table_name (str): The name of the table to check
        
    Returns:
        bool: True if the table exists, False otherwise
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=%s",
            [table_name]
        )
        return cursor.fetchone() is not None


def list_forms():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM form_builder_customform")
        return cursor.fetchall()



def get_form_fields(form_name):
    with connection.cursor() as cursor:
        # Get the table name from the form_builder_customform table
        cursor.execute("SELECT id FROM form_builder_customform WHERE name = %s", [form_name])
        form_id = cursor.fetchone()[0]

        # Get the column names using PRAGMA table_info
        cursor.execute(f"PRAGMA table_info(`{form_name}`)")
        columns = cursor.fetchall()
        print(columns)
        
        # Filter out id and created_at columns and return column names
        return [col[1] for col in columns if col[1] not in ('id', 'created_at')]



def create_form_table(form_name):
    """
    Create a new form table in the database with only id and created_at columns.
    """
    with connection.cursor() as cursor:
        try:
            connection.set_autocommit(False)
            create_table_sql = f"""
                CREATE TABLE `{form_name}` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(create_table_sql)
            connection.commit()
            return {
                'success': True,
                'table_name': form_name
            }
        except Exception as e:
            connection.rollback()
            print(e)
            raise e
        finally:
            connection.set_autocommit(True)



def add_fields_to_form(form_id, fields):
    """
    Add fields to an existing form table by form_id.
    """
    with connection.cursor() as cursor:
        try:
            connection.set_autocommit(False)
            # Get the form name from the form_id
            form = CustomForm.objects.get(id=form_id)
            form_name = form.name

            for field in fields:
                field_name = field['name'].lower().replace(' ', '_')
                field_type = field['type'].upper()

                if field_type == 'VARCHAR':
                    max_length = field.get('max_length', 255)
                    field_def = f"{field_name} VARCHAR({max_length})"
                elif field_type == 'INTEGER':
                    field_def = f"{field_name} INTEGER"
                elif field_type == 'TEXT':
                    field_def = f"{field_name} TEXT"
                elif field_type == 'DATE':
                    field_def = f"{field_name} DATE"
                elif field_type == 'BOOLEAN':
                    field_def = f"{field_name} BOOLEAN"
                elif field_type == 'DECIMAL':
                    field_def = f"{field_name} DECIMAL(10,2)"
                else:
                    continue  # Skip unknown field types

                if field.get('required', False):
                    field_def += " NOT NULL"

                alter_sql = f"ALTER TABLE `{form_name}` ADD COLUMN {field_def}"
                cursor.execute(alter_sql)

            connection.commit()
            return {
                'success': True,
                'table_name': form_name
            }
        except Exception as e:
            connection.rollback()
            print(e)
            raise e
        finally:
            connection.set_autocommit(True)


def get_form(form_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM `{form_name}`"
        )
        return cursor.fetchall()



def delete_form(form_name):
    with connection.cursor() as cursor:
        cursor.execute(
            f"DROP TABLE IF EXISTS `{form_name}`"
        )


def insert_record_with_fields(table_name, fields, values):
    """
    Insert a record with specific field values into a form table
    
    Args:
        table_name (str): The name of the table to insert into
        fields (list): List of field names
        values (list): List of values corresponding to fields
    """
    with connection.cursor() as cursor:
        fields_str = ', '.join(fields)
        placeholders = ', '.join(['%s'] * len(fields))
        
        sql = f"INSERT INTO `{table_name}` ({fields_str}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        
        return True


def add_record(form_name, records: list):
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO `{form_name}` (record) VALUES (%s)",
            records
        )


def remove_record(form_name, record_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"DELETE FROM `{form_name}` WHERE id = %s",
            [record_id]
        )


def update_record(form_name, record_id, record):
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE `{form_name}` SET record = %s WHERE id = %s",
            [record, record_id]
        )

