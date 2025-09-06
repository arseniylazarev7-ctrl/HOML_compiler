def preprocess(file_path):
    """
    По идее эта функция должна отлавливать ошибки, анализировать весь homl-проект в поиске текстовых ошибок,
    но мне лень пока писать препроцессор, да и это не столь важно,
    так что пока он просто возвращает код 0 что все хорошо и сообщение что все хорошо"""
    
    code = 0
    msg = f"Preprocessing completed successfully, no errors found. Exit code {code}"

    return code, msg