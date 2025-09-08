class NotRelatedToIELTS(Exception):
    ERROR_CODE = 1000

    def __init__(self, detail: str):

        self.detail = detail
        self.error_code = self.ERROR_CODE

    def __str__(self):
        return f"[ERROR] {self.error_code}: {self.detail}"

    def to_dict(self):
        return {"error": {"code": self.error_code, "message": self.detail}}
