# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import os
import shutil
import json
import tempfile
from typing import Dict


class ImportExportService:

    @staticmethod
    def export_data(data_file: str, export_path: str) -> Dict:
        try:
            if not os.path.exists(data_file):
                return {
                    'success': False,
                    'error': f'Source file {data_file} does not exist'
                }

            shutil.copy2(data_file, export_path)

            with open(export_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['_export_info'] = {
                'export_app': 'Smart Task Manager',
                'version': '1.3.0'
            }

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return {
                'success': True,
                'export_path': export_path,
                'export_size': os.path.getsize(export_path)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def import_data(data_file: str, import_path: str) -> Dict:
        backup_path = None
        try:
            backup_path = ImportExportService._create_temp_backup(data_file)

            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            import_data.pop('_export_info', None)

            if not ImportExportService._validate_import_data(import_data):
                if backup_path and os.path.exists(backup_path):
                    shutil.copy2(backup_path, data_file)
                    os.remove(backup_path)
                return {
                    'success': False,
                    'error': 'Invalid import data format'
                }

            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(import_data, f, indent=4, ensure_ascii=False)

            if backup_path and os.path.exists(backup_path):
                os.remove(backup_path)

            return {
                'success': True,
                'imported_items': {
                    'tasks': len(import_data)
                }
            }

        except Exception as e:
            if backup_path and os.path.exists(backup_path):
                try:
                    shutil.copy2(backup_path, data_file)
                    os.remove(backup_path)
                except Exception:
                    pass

            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def _create_temp_backup(data_file: str):
        if not os.path.exists(data_file):
            return None

        temp_dir = tempfile.gettempdir()
        backup_path = os.path.join(temp_dir, 'smarttm_import_backup.json')

        try:
            shutil.copy2(data_file, backup_path)
            return backup_path
        except Exception:
            return None

    @staticmethod
    def _validate_import_data(data) -> bool:
        if not isinstance(data, dict):
            return False

        for key, value in data.items():
            if key.startswith('_'):
                continue
            if not isinstance(value, dict):
                return False
            if 'id' not in value or 'title' not in value:
                return False

        return True
