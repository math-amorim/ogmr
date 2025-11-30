from easysnmp import Session
from enum import Enum
from typing import List


class PortState(Enum):
    ENABLED = 1
    DISABLED = 2


MIB_PORT_STATUS = {
    "OPER": ".1.3.6.1.2.1.2.2.1.8",
    "ADMIN": ".1.3.6.1.2.1.2.2.1.7",
    "FDB_PORT": ".1.3.6.1.2.1.17.4.3.1.2"
}


class SNMPManager:
    def __init__(self, host: str, community_read: str, community_write: str, version: int = 2, hostname: str = None, community: str = None):
        if hostname and not host:
            host = hostname
        if community and not community_read:
            community_read = community
            community_write = community

        self.read_sess = Session(hostname=host, community=community_read, version=version)
        self.write_sess = Session(hostname=host, community=community_write, version=version)

    def get_ports_by_mac(self, mac: str = ""):
        if mac != "":
            # buscar porta por mac
            return self.read_sess.get(f"{MIB_PORT_STATUS['FDB_PORT']}.{mac}")
        # retorna todas se vazio
        return self.read_sess.walk(MIB_PORT_STATUS['FDB_PORT'])

    # altera o estado de uma porta aqui
    def set_port_state(self, port: int, state: PortState) -> bool:
        try:
            self.write_sess.set(f"{MIB_PORT_STATUS['ADMIN']}.{port}", state.value, 'i')
            return True
        except Exception as e:
            print(f"Erro ao alterar porta {port}: {e}")
            return False


    def fetch_port_status(self, port: int = 0) -> List[dict]:
        # retorna status de uma porta
        if port > 0:
                oper = self.read_sess.get(f"{MIB_PORT_STATUS['OPER']}.{port}").value
                admin = self.read_sess.get(f"{MIB_PORT_STATUS['ADMIN']}.{port}").value
                return [{"port": port, "operational": oper, "administrative": admin}]

        statuses = []
        oper_list = self.read_sess.walk(MIB_PORT_STATUS['OPER'])
        admin_list = self.read_sess.walk(MIB_PORT_STATUS['ADMIN'])

        # retorna status de várias portas
        for idx, (oper, admin) in enumerate(zip(oper_list, admin_list), start=1):
            statuses.append({
                "port": idx,
                "operational": oper.value,
                "administrative": admin.value
            })
        return statuses

    def set_ports(self, ports: List[int], state: PortState) -> bool:
        for p in ports:
            if not self.set_port_state(p, state):
                return False
        return True
