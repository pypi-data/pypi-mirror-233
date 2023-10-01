import json
import os
import requests
import logging

class LebryDB:
    def __init__(self, nome_arquivo, webhook_url=None):
        """
        Inicializa uma instância do LebryDB.

        :param nome_arquivo: O nome do arquivo de banco de dados.
        :param webhook_url: URL para envio de webhooks (opcional).
        """
        self.nome_arquivo = nome_arquivo
        self.data = self._carregar_dados()
        self.webhook_url = webhook_url
        self.logger = self._configurar_logger()

    def _configurar_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Configurar um manipulador de log para gravar mensagens em um arquivo
        log_file_handler = logging.FileHandler("lebrydb.log")
        log_file_handler.setLevel(logging.INFO)

        # Formato das mensagens de log
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file_handler.setFormatter(log_format)

        # Adicionar o manipulador de log à instância do logger
        logger.addHandler(log_file_handler)

        return logger

    def _carregar_dados(self):
        """
        Carrega os dados do arquivo de banco de dados.

        :return: Os dados do banco de dados.
        """
        if not self.nome_arquivo or not os.path.exists(self.nome_arquivo):
            return {}
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _salvar_dados(self):
        """
        Salva os dados no arquivo de banco de dados.
        """
        if self.nome_arquivo:
            with open(self.nome_arquivo, 'w') as arquivo:
                json.dump(self.data, arquivo, indent=4)

    def inserir(self, chave, documento):
        """
        Insere um documento na base de dados.

        :param chave: A chave do documento.
        :param documento: O documento a ser inserido.
        """
        try:
            # Validar a chave e o documento
            self._validar_chave(chave)
            self._validar_documento(documento)

            # Verificar se a chave já existe
            if chave in self.data:
                raise KeyError("Chave já existe na base de dados")

            # Inserir o documento
            self.data[chave] = documento
            self._salvar_dados()
            self._enviar_webhook("insercao", chave, documento)
        except Exception as e:
            self.logger.error(f"Erro ao inserir: {str(e)}")
            raise e

    def consultar(self, chave):
        """
        Consulta um documento na base de dados.

        :param chave: A chave do documento a ser consultado.
        :return: O documento correspondente à chave.
        """
        try:
            # Validar a chave
            self._validar_chave(chave)

            # Consultar o documento
            if chave not in self.data:
                raise KeyError("Chave não encontrada na base de dados")

            return self.data[chave]
        except Exception as e:
            self.logger.error(f"Erro ao consultar: {str(e)}")
            raise e

    def atualizar(self, chave, novo_documento):
        """
        Atualiza um documento na base de dados.

        :param chave: A chave do documento a ser atualizado.
        :param novo_documento: O novo documento.
        """
        try:
            # Validar a chave e o novo documento
            self._validar_chave(chave)
            self._validar_documento(novo_documento)

            # Verificar se a chave existe
            if chave not in self.data:
                raise KeyError("Chave não encontrada na base de dados")

            # Atualizar o documento
            self.data[chave] = novo_documento
            self._salvar_dados()
            self._enviar_webhook("atualizacao", chave, novo_documento)
        except Exception as e:
            self.logger.error(f"Erro ao atualizar: {str(e)}")
            raise e

    def excluir(self, chave):
        """
        Exclui um documento da base de dados.

        :param chave: A chave do documento a ser excluído.
        """
        try:
            # Validar a chave
            self._validar_chave(chave)

            # Verificar se a chave existe
            if chave not in self.data:
                raise KeyError("Chave não encontrada na base de dados")

            # Excluir o documento
            documento_excluido = self.data.pop(chave)
            self._salvar_dados()
            self._enviar_webhook("exclusao", chave, documento_excluido)
        except Exception as e:
            self.logger.error(f"Erro ao excluir: {str(e)}")
            raise e

    def alterar_webhook_url(self, nova_url):
        """
        Altera a URL do webhook.

        :param nova_url: A nova URL do webhook.
        """
        self.webhook_url = nova_url

    def _enviar_webhook(self, evento, chave, documento):
        """
        Envia um webhook.

        :param evento: O tipo de evento (insercao, atualizacao, exclusao).
        :param chave: A chave do documento.
        :param documento: O documento relacionado ao evento.
        """
        if self.webhook_url:
            dados_webhook = {
                "evento": evento,
                "chave": chave,
                "documento": documento
            }
            try:
                response = requests.post(self.webhook_url, json=dados_webhook)
                response.raise_for_status()
                self.logger.info("Webhook enviado com sucesso.")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Falha ao enviar o webhook: {str(e)}")

    def listar_chaves(self):
        """
        Lista todas as chaves na base de dados.

        :return: Uma lista de chaves.
        """
        return list(self.data.keys())

    def contar_documentos(self):
        """
        Conta a quantidade de documentos na base de dados.

        :return: O número de documentos na base de dados.
        """
        return len(self.data)

    def limpar_base_de_dados(self):
        """
        Limpa a base de dados, removendo todos os documentos.
        """
        try:
            self.data = {}
            self._salvar_dados()
            self.logger.info("Base de dados limpa com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao limpar a base de dados: {str(e)}")

    def consultar_por_criterios(self, criterios):
        """
        Consulta documentos com base em critérios.

        :param criterios: Um dicionário de critérios de consulta.
        :return: Uma lista de documentos que atendem aos critérios.
        """
        resultados = []
        for chave, documento in self.data.items():
            criterios_atendidos = all(documento.get(campo) == valor for campo, valor in criterios.items())
            if criterios_atendidos:
                resultados.append({chave: documento})
        return resultados

    def exportar_dados(self, nome_arquivo_exportacao):
        """
        Exporta os dados para um arquivo JSON.

        :param nome_arquivo_exportacao: O nome do arquivo de exportação.
        """
        try:
            with open(nome_arquivo_exportacao, 'w') as arquivo:
                json.dump(self.data, arquivo, indent=4)
            self.logger.info(f"Dados exportados para {nome_arquivo_exportacao} com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao exportar dados: {str(e)}")

    def _validar_chave(self, chave):
        """
        Valida uma chave.

        :param chave: A chave a ser validada.
        """
        if not isinstance(chave, str):
            raise ValueError("A chave deve ser uma string.")

    def _validar_documento(self, documento):
        """
        Valida um documento.

        :param documento: O documento a ser validado.
        """
        if not isinstance(documento, dict):
            raise ValueError("O documento deve ser um dicionário.")

    def _validar_critérios(self, criterios):
        """
        Valida os critérios de consulta para evitar injeção de código.

        :param criterios: Um dicionário de critérios de consulta.
        :raises: ValueError se os critérios não forem válidos.
        """
        for campo, valor in criterios.items():
            if not isinstance(campo, str):
                raise ValueError("Os campos dos critérios devem ser strings.")
            if not isinstance(valor, (str, int, float, bool, type(None))):
                raise ValueError("Os valores dos critérios devem ser tipos primitivos (str, int, float, bool) ou None.")

    def obter_historico(self, chave):
        """
        Obtém o histórico de versões de um documento específico.

        :param chave: A chave do documento.
        :return: Uma lista de todas as versões anteriores do documento.
        """
        try:
            # Validar a chave
            self._validar_chave(chave)

            # Verificar se a chave existe
            if chave not in self.data:
                raise KeyError("Chave não encontrada na base de dados")

            # Obter o histórico de versões do documento
            historico_versoes = self.data[chave].get("historico_versoes", [])
            return historico_versoes
        except Exception as e:
            self.logger.error(f"Erro ao obter histórico: {str(e)}")
            raise e

