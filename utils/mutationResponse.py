from flask import jsonify


def mutation_response(result: bool):
    return jsonify({'success': result})
