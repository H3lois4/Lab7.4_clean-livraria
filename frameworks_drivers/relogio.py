from datetime import datetime

from use_cases.portas import Relogio


class RelogioDoSistema(Relogio):
    def agora(self):
        return datetime.now().replace(microsecond=0)
