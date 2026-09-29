class ProcessService:
    def process(self, text: str) -> str:
        return text


def get_process_service() -> ProcessService:
    return ProcessService()
