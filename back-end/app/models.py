from . import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    departamento = db.Column(db.String(100))


class Sala(db.Model):
    __tablename__ = "salas"

    id_sala = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    bloco = db.Column(db.String(5), nullable=False)
    numero_pcs = db.Column(db.Integer)


class Switch(db.Model):
    __tablename__ = "switches"

    id_switch = db.Column(db.Integer, primary_key=True)
    numero_portas = db.Column(db.Integer, nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    mac = db.Column(db.String(17), nullable=False)
    versao_snmp = db.Column(db.Integer, nullable=False)
    porta_uplink = db.Column(db.Integer, nullable=False)
    chave_community = db.Column(db.String(32))
    protocolo_autenticacao = db.Column(db.String(25))
    protocolo_criptografia = db.Column(db.String(25))
    chave_autenticacao = db.Column(db.String(256))
    chave_privada = db.Column(db.String(256))
    nivel_seguranca = db.Column(db.Integer)


class LigacaoSalaSwitch(db.Model):
    __tablename__ = "ligacao_sala_switch"

    id_sala = db.Column(db.Integer, db.ForeignKey("salas.id_sala", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_switch = db.Column(db.Integer, db.ForeignKey("switches.id_switch", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class AgendamentoSalaSwitch(db.Model):
    __tablename__ = "agendamento_sala_switch"
    
    id_sala = db.Column(db.Integer, db.ForeignKey("salas.id_sala", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_switch = db.Column(db.Integer, db.ForeignKey("switches.id_switch", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)


class Maquina(db.Model):
    __tablename__ = "maquinas"

    id_maquina = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25), nullable=False)
    ip = db.Column(db.String(12), nullable=False)
    tipo_maquina = db.Column(db.Boolean, nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey("salas.id_sala", ondelete="SET NULL", onupdate="CASCADE"))
    mac = db.Column(db.String(12))


class MaquinasUsadasProfessores(db.Model):
    __tablename__ = "maquinas_usadas_professores"
    
    id_funcionario = db.Column(db.Integer, db.ForeignKey("funcionarios.id_funcionario", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_maquina_professor = db.Column(db.Integer, db.ForeignKey("maquinas.id_maquina", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    data_acesso = db.Column(db.DateTime)


class MaquinasConectadasSwitch(db.Model):
    __tablename__ = "maquinas_conectadas_switch"

    id_maquina = db.Column(db.Integer, db.ForeignKey("maquinas.id_maquina", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    id_switch = db.Column(db.Integer, db.ForeignKey("switches.id_switch", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    porta = db.Column(db.Integer, nullable=False)
