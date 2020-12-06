import json
from ..shared import db, ResponseCodes, ResponseTypes, request_data, AlchemyEncoder
from ..models import Allergy, IngredientKeyword
from flask import Response


def get_allergies():

    result = db.session.query(Allergy)

    return Response(
        json.dumps([r for r in result], cls=AlchemyEncoder),
        status=ResponseCodes.SUCCESS,
        mimetype=str(ResponseTypes.JSON)
    )

def get_ingredient_keywords():

    result = db.session.query(IngredientKeyword)

    return Response(
        json.dumps([r for r in result], cls=AlchemyEncoder),
        status=ResponseCodes.SUCCESS,
        mimetype=str(ResponseTypes.JSON)
    )

def create_ingredient_keyword():

    data = request_data()
    try:
        ikw = IngredientKeyword(
            keyword = data.get('keyword', None),
            allergy_id = data.get('allergy_id', None)
        )
        db.session.add(ikw)
        db.session.commit()
        response_data = json.loads(json.dumps(ikw, cls=AlchemyEncoder))
        response_data['id'] = ikw.id
        
        return Response(
            json.dumps(response_data),
            status=ResponseCodes.SUCCESS,
            mimetype=str(ResponseTypes.JSON)
        )

    except Exception as ex:
        return Response(
            json.dumps({'error': str(ex)}),
            status=ResponseCodes.FAILURE,
            mimetype=str(ResponseTypes.JSON)
        )

def create_allergy():

    data = request_data()
    try:
        allergy = Allergy(
            name = data.get('name', None),
        )
        db.session.add(allergy)
        db.session.commit()
        response_data = json.loads(json.dumps(allergy, cls=AlchemyEncoder))
        response_data['id'] = allergy.id

        return Response(
            json.dumps(response_data),
            status=ResponseCodes.SUCCESS,
            mimetype=str(ResponseTypes.JSON)
        )

    except Exception as ex:
        return Response(
            json.dumps({'error': str(ex)}),
            status=ResponseCodes.FAILURE,
            mimetype=str(ResponseTypes.JSON)
        )