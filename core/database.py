import sqlite3

class master():

        def __init__(self):
                self._connection = sqlite3.connect('./core/dados.db')
                self._cursor = self._connection.cursor()

        def dict_factory(self,cursor, row):
                dicionario = {}
                for idx, col in enumerate(self._cursor.description):
                        dicionario[col[0]] = row[idx]
                return dicionario

class DataUser(master):

        def add_user(self,nickname,nome,senha,data_nasc):
                self._cursor.execute('''INSERT INTO usuario(nickname,nome,senha,data_nasc) VALUES (?,?,?,?)''', (nickname,nome,senha,data_nasc))
                self._connection.commit()
                

        def updata_user(self,nickname,senha,idUpdate):
                self._cursor.execute('''UPDATE usuario SET nickname=?,senha=? where  id = ?''',
                (nickname,senha,idUpdate))
                self._connection.commit()

        def updata_user_score(self,score,idUpdate):
               self._cursor.execute('''UPDATE usuario SET score=? where  id = ?''',(score,idUpdate))
               self._connection.commit()

        def del_user(self,idDeletar ):
                self._cursor.execute('delete from usuario where id = {}'.format(idDeletar))
                self._connection.commit()

        def del_user_all(self):
                self._cursor.execute('DELETE FROM table usuario')
                self._connection.commit()

        def consultData_user(self):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('select usuario.ID, usuario.nickname, usuario.nome , usuario.senha, usuario.score from usuario')
                
                return self._cursor.fetchall()

        def consultData_user_id(self,idUser):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('select usuario.ID, usuario.nickname,usuario.nome, usuario.score, usuario.senha from usuario where id ={}'.format(idUser))
                
                return self.cursor.fetchall()

        def consultData_ranking_user(self):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('SELECT  nickname, score FROM usuario ORDER BY score DESC;')

                return self._cursor.fetchall()

class DataContent(master):
        
        def add_content(self,titulo,pergunta,dica,informacao,pontuacao,resposta):
                self._cursor.execute('''INSERT INTO conteudo(titulo,pergunta,dica,informacao,pontuacao,resposta) VALUES (?,?,?,?,?,?)''', (titulo,pergunta,dica,informacao,pontuacao,resposta))
                self._connection.commit()

        def  updata_content(self,titulo,pergunta,dica,informacao,pontuacao,resposta,codUpdate):

                self._cursor.execute('''UPDATE conteudo SET titulo=?,pergunta=? ,dica=? 
                                ,informacao=?,pontuacao=?,resposta=? where  COD =?''',
                                (titulo,pergunta,dica,informacao,pontuacao,resposta,codUpdate))
                self._connection.commit()

        def  del_content(self,codDeletar):
                self._cursor.execute('delete from conteudo where COD = {}'.format(codDeletar))
                self._connection.commit()

        def  del_content_all(self):
                self._cursor.execute('DELETE FROM table conteudo')
                self._connection.commit()  

       
        def add_responde(self,fk_usuario_ID,fk_conteudo_COD):
                self._cursor.execute('''INSERT INTO responde(fk_usuario_ID,fk_conteudo_COD) VALUES (?,?)''', (fk_usuario_ID,fk_conteudo_COD))
                self._connection.commit()
                
        

        def consultData_content_search(self,COD):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('select * from conteudo where COD == {}'.format(COD))
                return self._cursor.fetchall()

        def consultData_content(self):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('select * from conteudo')
                return self._cursor.fetchall()

        def consultData_content_user(self,idUser):
                self._cursor.row_factory = self.dict_factory
                self._cursor.execute('''SELECT conteudo.COD, conteudo.pergunta
                FROM responde INNER JOIN  conteudo 
                ON    conteudo.COD  = responde.fk_conteudo_COD
                WHERE  responde.fk_usuario_ID == {}'''.format(idUser))
                return self._cursor.fetchall()

        def add_alternatives(self,opcao,descricao,fk_conteudo_COD):
                self._cursor.execute('''INSERT INTO alternativas(opcao,descricao,fk_conteudo_COD) VALUES (?,?,?)''', (opcao,descricao,fk_conteudo_COD))
                self._connection.commit()

        def consultData_alternatives(self,CODcontent):
                self._cursor.row_factory = self.dict_factoryy
                self._cursor.execute(''' 
                SELECT alternativas.opcao ,alternativas.descricao
                FROM conteudo INNER JOIN alternativas 
                ON    conteudo.COD  ==  alternativas.fk_conteudo_COD 
                WHERE conteudo.COD == {}'''.format(CODcontent))
                return self._cursor.fetchall()




