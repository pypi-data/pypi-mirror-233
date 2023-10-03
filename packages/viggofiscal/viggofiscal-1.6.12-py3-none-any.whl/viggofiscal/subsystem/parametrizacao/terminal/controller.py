import flask
from viggocore.common import exception, utils, controller


class Controller(controller.CommonController):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    def analisar(self):
        data = flask.request.get_json()
        considera_caixa = data.get('considera_caixa', False)
        try:
            tuplas = self.manager.analisar(**data)
        except exception.ViggoCoreException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        collection = []
        caixa_aberto = False
        if len(tuplas) > 0:
            permissao = False
        else:
            permissao = True
        for tupla in tuplas:
            if considera_caixa:
                tupla_dict = {
                    'user_name': tupla[0],
                    'terminal_descricao': tupla[1],
                    'caixa_numero': tupla[2]}
                if tupla[2] is not None:
                    caixa_aberto = True
            else:
                tupla_dict = {
                    'user_name': tupla[0],
                    'terminal_descricao': tupla[1],
                    'caixa_numero': None}
            collection.append(tupla_dict)

        response = {
            'permissao': permissao,
            'operadores_em_uso': collection,
            'caixa_aberto': caixa_aberto,
            'considera_caixa': considera_caixa}

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype="application/json")
