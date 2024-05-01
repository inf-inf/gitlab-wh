class RedirectError(Exception):
    """Исключение, при котором на фронте должен происходить редирект"""
    def __init__(self, url: str, status_code: int = 307) -> None:
        """_summary_

        Args:
            url (str): Адрес, на который необходим редирект
            status_code (int, optional): Статус код. По умолчанию: 307.
        """
        super().__init__()
        self.url = url
        self.status_code = status_code
