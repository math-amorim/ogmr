from flask import Blueprint, request, jsonify
from .. import db
from ..models import (
    Sala,
    Switch,
    Maquina,
    MaquinasConectadasSwitch,
    AgendamentoSalaSwitch,
    LigacaoSalaSwitch
)
from ..snmp import SNMPManager

api = Blueprint("api", __name__)

@api.route("/salas", methods=["GET"])
def listar_salas():
    salas = Sala.query.all()
    return jsonify([{
        "id_sala": s.id_sala,
        "numero": s.numero,
        "bloco": s.bloco,
        "numero_pcs": s.numero_pcs
    } for s in salas])


@api.route("/salas", methods=["POST"])
def criar_sala():
    dados = request.json
    sala = Sala(
        numero=dados["numero"],
        bloco=dados["bloco"],
        numero_pcs=dados.get("numero_pcs")
    )
    db.session.add(sala)
    db.session.commit()
    return jsonify({"mensagem": "Sala criada"}), 201

@api.route("/switches", methods=["GET"])
def listar_switches():
    switches = Switch.query.all()
    return jsonify([{
        "id_switch": s.id_switch,
        "numero_portas": s.numero_portas,
        "ip": s.ip,
        "mac": s.mac,
        "versao_snmp": s.versao_snmp
    } for s in switches])


@api.route("/switches", methods=["POST"])
def criar_switch():
    dados = request.json
    switch = Switch(
        numero_portas=dados["numero_portas"],
        ip=dados["ip"],
        mac=dados["mac"],
        versao_snmp=dados["versao_snmp"],
        porta_uplink=dados["porta_uplink"],
        chave_community=dados.get("chave_community"),
        protocolo_autenticacao=dados.get("protocolo_autenticacao"),
        protocolo_criptografia=dados.get("protocolo_criptografia"),
        chave_autenticacao=dados.get("chave_autenticacao"),
        chave_privada=dados.get("chave_privada"),
        nivel_seguranca=dados.get("nivel_seguranca")
    )
    db.session.add(switch)
    db.session.commit()
    return jsonify({"mensagem": "Switch criado"}), 201

@api.route("/maquinas", methods=["GET"])
def listar_maquinas():
    maquinas = Maquina.query.all()
    return jsonify([{
        "id_maquina": m.id_maquina,
        "nome": m.nome,
        "ip": m.ip,
        "tipo_maquina": m.tipo_maquina,
        "id_sala": m.id_sala,
        "mac": m.mac
    } for m in maquinas])


@api.route("/maquinas", methods=["POST"])
def criar_maquina():
    dados = request.json
    maquina = Maquina(
        nome=dados["nome"],
        ip=dados["ip"],
        tipo_maquina=dados["tipo_maquina"],
        id_sala=dados["id_sala"],
        mac=dados.get("mac")
    )
    db.session.add(maquina)
    db.session.commit()
    return jsonify({"mensagem": "Máquina criada"}), 201

@api.route("/ligacoes", methods=["POST"])
def criar_ligacao():
    dados = request.json
    lig = LigacaoSalaSwitch(
        id_sala=dados["id_sala"],
        id_switch=dados["id_switch"]
    )
    db.session.add(lig)
    db.session.commit()
    return jsonify({"mensagem": "Ligação criada"}), 201


@api.route("/ligacoes", methods=["GET"])
def listar_ligacoes():
    ligacoes = LigacaoSalaSwitch.query.all()
    return jsonify([{
        "id_sala": l.id_sala,
        "id_switch": l.id_switch
    } for l in ligacoes])

@api.route("/agendamentos", methods=["POST"])
def criar_agendamento():
    dados = request.json
    ag = AgendamentoSalaSwitch(
        id_sala=dados["id_sala"],
        id_switch=dados["id_switch"],
        data_inicio=dados["data_inicio"],
        data_fim=dados["data_fim"]
    )
    db.session.add(ag)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento criado"}), 201


@api.route("/agendamentos", methods=["GET"])
def listar_agendamentos():
    agends = AgendamentoSalaSwitch.query.all()
    return jsonify([{
        "id_sala": a.id_sala,
        "id_switch": a.id_switch,
        "data_inicio": a.data_inicio.isoformat(),
        "data_fim": a.data_fim.isoformat()
    } for a in agends])

@api.route("/porta", methods=["POST"])
def alterar_porta():
    dados = request.json

    id_switch = dados["id_switch"]
    id_maquina = dados["id_maquina"]
    porta = dados["porta"]
    # garantir que status seja um inteiro (1 para ligado, 0 para desligado)
    try:
        status = int(dados["status"])
    except Exception:
        return jsonify({"erro": "status inválido"}), 400

    switch = Switch.query.filter_by(id_switch=id_switch).first()

    snmp = SNMPManager(
        hostname=switch.ip,
        community_read=switch.chave_community,
        community_write=switch.chave_community,
        version=switch.versao_snmp
    )

    snmp_sucesso = snmp.alterar_estado_porta(porta, status)

    registro = MaquinasConectadasSwitch.query.filter_by(
        id_maquina=id_maquina,
        id_switch=id_switch
    ).first()

    if registro:
        registro.status = True if status == 1 else False
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": "falha ao atualizar registro", "detalhe": str(e)}), 500

    return jsonify({
        "sucesso": snmp_sucesso,
        "porta": porta,
        "status": status
    })
