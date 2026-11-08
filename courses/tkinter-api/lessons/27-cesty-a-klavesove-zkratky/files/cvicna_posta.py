"""Místní SMTP záchyt pro výuku; žádnou zprávu nepředává dál.

Vyžaduje aiosmtpd>=1.4.6,<2. Běží pouze na 127.0.0.1 a volném portu.
Režimy: prijmout, odmitnout (RCPT 550), pomalu (převzetí před opožděným 250).
Zprávy jsou jen v paměti a po konci programu se ztratí.
"""
import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
import threading
from aiosmtpd.controller import Controller


@dataclass(frozen=True)
class ZachycenaZprava:
    odesilatel: str
    prijemci: tuple
    data: bytes


class Zachyt:
    host = '127.0.0.1'
    port = 0
    def __init__(self):
        self._zamek = threading.Lock()
        self._zpravy = []
        self._rezim = 'prijmout'

    @property
    def zpravy(self):
        with self._zamek:
            return list(self._zpravy)

    def nastav_rezim(self, rezim):
        if rezim not in ('prijmout', 'odmitnout', 'pomalu'):
            raise ValueError('Neznámý režim místního záchytu.')
        with self._zamek:
            self._rezim = rezim

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        with self._zamek:
            rezim = self._rezim
        if rezim == 'odmitnout':
            return '550 5.1.1 Cvicne odmitnuti prijemce'
        envelope.rcpt_tos.append(address)
        return '250 2.1.5 OK'

    async def handle_DATA(self, server, session, envelope):
        with self._zamek:
            self._zpravy.append(ZachycenaZprava(envelope.mail_from, tuple(envelope.rcpt_tos), bytes(envelope.original_content)))
            rezim = self._rezim
        # Záměrně až po převzetí: timeout klienta nedokazuje, že server nic nepřijal.
        if rezim == 'pomalu':
            await asyncio.sleep(.35)
        return '250 2.0.0 Zprava zustava pouze v mistnim zachytu'


class _Controller(Controller):
    def _trigger_server(self):
        # aiosmtpd 1.4.6 při port=0 potřebuje pro úvodní probuzení skutečně přidělený port.
        if self.server is not None:
            self.port = self.server.sockets[0].getsockname()[1]
        super()._trigger_server()


@contextmanager
def cvicna_posta():
    zachyt = Zachyt()
    controller = _Controller(zachyt, hostname=zachyt.host, port=0, ready_timeout=3,
                             decode_data=False, data_size_limit=2_000_000)
    try:
        controller.start()
        zachyt.port = controller.port
        yield zachyt
    finally:
        controller.stop(no_assert=True)
