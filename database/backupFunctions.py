import zipfile


class BackupFunctions:
    def __init__(self):
        self.file = 'uniqueMeal.db'

    def createBackup(self):
        with zipfile.ZipFile('backup.zip', 'w') as zipF:
            zipF.write(self.file, compress_type=zipfile.ZIP_DEFLATED)

    def restoreBackup(self):
        with zipfile.ZipFile('backup.zip', 'r') as zipF:
            zipF.extractall()
        print("Backup restored successfully.")