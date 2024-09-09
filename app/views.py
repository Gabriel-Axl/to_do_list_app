from flask import Blueprint, request, jsonify
from app import session  
from .models import Tarefa 
views = Blueprint('views', __name__)

@views.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    
    if not data or not 'titulo' in data:
        return jsonify({"message": "Dados inválidos"}), 400

    nova_tarefa = Tarefa(
        titulo=data['titulo'],
        descricao=data.get('descricao'),
        data_conclusao=data.get('data_conclusao')
    )
    try:
        session.add(nova_tarefa)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"message": "Erro ao salvar tarefa"}), 500

    return jsonify({"message":"Salvo com sucesso!"}), 201

@views.route('/tarefas', methods=['GET'])
def listarTarefas():
    tarefas = session.query(Tarefa).all()
    return jsonify([{
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "data_criacao": tarefa.data_criacao,
        "data_conclusao": tarefa.data_conclusao
    } for tarefa in tarefas]), 200
    
@views.route('/tarefas/<int:id>', methods=['PUT'])
def editarTarefa(id):
    tarefa = session.query(Tarefa).get(id)
    if not tarefa:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    tarefa.titulo = request.json.get('titulo', tarefa.titulo)
    tarefa.descricao = request.json.get('descricao', tarefa.descricao)
    tarefa.data_conclusao = request.json.get('data_conclusao', tarefa.data_conclusao)
    
    session.commit()
    
    return jsonify({
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "data_criacao": tarefa.data_criacao,
        "data_conclusao": tarefa.data_conclusao
    }), 201
    
@views.route('/tarefas/<int:id>', methods=['DELETE'])
def deletarTarefa(id):
    tarefa = session.query(Tarefa).get(id)
    if not tarefa:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    session.delete(tarefa)
    session.commit()
    
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200