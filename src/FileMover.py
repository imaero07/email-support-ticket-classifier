from pathlib import Path
import shutil
import logging
log = logging.getLogger(__name__)

class FileMover:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path +"output")
        if self.folder_path.exists():
            try:
                shutil.rmtree(self.folder_path)
            except Exception as e:
                log.warning(f"Не удалось очистить директорию output: {e}")
            else:
                log.info("Output директория очищена")

    def move_files(self, email, category):
        folder = Path(self.folder_path) / category
        folder.mkdir(parents=True, exist_ok=True)
        src = Path(email.source_path)
        dst = folder / src.name
        try:
            shutil.copy2(src, dst)
        except FileNotFoundError as e:
            log.error(f"Ошибка директории {dst}: {e}")
        except PermissionError as e:
            log.error(f"Ошибка прав программы: {e}")
        except Exception as e:
            log.error(f"Неизвестная ошибка: {e}")
        else:
            log.debug(f"Письмо {src.name} из {src} успешно скопировано в {dst}")