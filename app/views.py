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

    session.add(nova_tarefa)
    session.commit()

    return jsonify({
        "id": nova_tarefa.id,
        "titulo": nova_tarefa.titulo,
        "descricao": nova_tarefa.descricao,
        "data_criacao": nova_tarefa.data_criacao,
        "data_conclusao": nova_tarefa.data_conclusao
    }), 201
