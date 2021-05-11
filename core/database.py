import sqlite3

connection = sqlite3.connect('./core/dados.db')
cursor =connection.cursor()

# retorna o request do dados no formato de dicionario
def dict_factory(cursor, row):
        dicionario = {}
        for idx, col in enumerate(cursor.description):
            dicionario[col[0]] = row[idx]
        return dicionario
        
# =======>    Usuario - INICIO <=======

def add_user(nickname,nome,senha,data_nasc):
        cursor.execute('''INSERT INTO usuario(nickname,nome,senha,data_nasc) VALUES (?,?,?,?)''', (nickname,nome,senha,data_nasc))
        connection.commit()

def  updata_user(nickname,senha,idUpdate):

        cursor.execute('''UPDATE usuario SET
                nickname=?,senha=? where  id = ?''',
                (nickname,senha,idUpdate))
        connection.commit()

def  updata_user_score(score,idUpdate):

        cursor.execute('''UPDATE usuario SET
                score=? where  id = ?''',
                (score,idUpdate))
        connection.commit()

def  del_user(idDeletar):
            cursor.execute('delete from usuario where id = {}'.format(idDeletar))
            connection.commit()
       
def  del_user_all():
           cursor.execute('DELETE FROM table usuario')
           connection.commit()  

def consultData_user():
        cursor.row_factory = dict_factory
        cursor.execute('select usuario.ID, usuario.nickname, usuario.nome , usuario.senha, usuario.score from usuario')
        return cursor.fetchall()

def consultData_user_id(idUser):
        cursor.row_factory = dict_factory
        cursor.execute('select usuario.ID, usuario.nickname,usuario.nome, usuario.score, usuario.senha from usuario where id ={}'.format(idUser))
        return cursor.fetchall()

def consultData_ranking_user():
        cursor.row_factory = dict_factory
        cursor.execute('SELECT  nickname, score FROM usuario ORDER BY score DESC;')
        return cursor.fetchall()

# =======> Usuario - FIM <======

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# =======>    Conteudo - INICIO <======
def add_content(titulo,pergunta,dica,informacao,pontuacao,resposta):
        cursor.execute('''INSERT INTO conteudo(titulo,pergunta,dica,informacao,pontuacao,resposta) VALUES (?,?,?,?,?,?)''', (titulo,pergunta,dica,informacao,pontuacao,resposta))
        connection.commit()

def  updata_content(titulo,pergunta,dica,informacao,pontuacao,resposta,codUpdate):

        cursor.execute('''UPDATE conteudo SET titulo=?,pergunta=? ,dica=? 
                        ,informacao=?,pontuacao=?,resposta=? where  COD =?''',
                        (titulo,pergunta,dica,informacao,pontuacao,resposta,codUpdate))
        connection.commit()

# verifica essa função 
def  del_content(codDeletar):
            cursor.execute('delete from conteudo where COD = {}'.format(codDeletar))
            connection.commit()

def  del_content_all(self):
           cursor.execute('DELETE FROM table conteudo')
           connection.commit()  

# =======> Conteudo - FIM <======

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#xxxxxxxxxxxxxxxxxxxxx> RELACIONAMENTO  <xxxxxxxxxxxxxxx

# =======> Responde - INICIO <======

def add_responde(fk_usuario_ID,fk_conteudo_COD):
        cursor.execute('''INSERT INTO responde(fk_usuario_ID,fk_conteudo_COD) VALUES (?,?)''', (fk_usuario_ID,fk_conteudo_COD))
        connection.commit()
        
# =======> Responde - Final<======

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# =======> Alternativas  - INICIO <======

def consultData_content_search(COD):
        cursor.row_factory = dict_factory
        cursor.execute('select * from conteudo where COD == {}'.format(COD))
        return cursor.fetchall()

def consultData_content():
        cursor.row_factory = dict_factory
        cursor.execute('select * from conteudo')
        return cursor.fetchall()

# vai retorna uma lista dicionario contendo o COD das perguntas que o usuario já fez
def consultData_content_user(idUser):
        cursor.row_factory = dict_factory
        cursor.execute('''SELECT conteudo.COD, conteudo.pergunta
        FROM responde INNER JOIN  conteudo 
        ON    conteudo.COD  = responde.fk_conteudo_COD
        WHERE  responde.fk_usuario_ID == {}'''.format(idUser))
        return cursor.fetchall()

# campo: a, b ,c , d ,e ....
def add_alternatives(opcao,descricao,fk_conteudo_COD):
        cursor.execute('''INSERT INTO alternativas(opcao,descricao,fk_conteudo_COD) VALUES (?,?,?)''', (opcao,descricao,fk_conteudo_COD))
        connection.commit()

def consultData_alternatives(CODcontent):
        cursor.row_factory = dict_factory
        cursor.execute(''' 
        SELECT alternativas.opcao ,alternativas.descricao
        FROM conteudo INNER JOIN alternativas 
        ON    conteudo.COD  ==  alternativas.fk_conteudo_COD 
        WHERE conteudo.COD == {}'''.format(CODcontent))
        return cursor.fetchall()

# =======> Alternativas  - FINAL <======

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# chamadas:

#add_user("L","lucas","123","05/04/2001") #id = 1
#add_user("Li","lili","123","05/04/2001")  #id = 2
#add_user("Lu","lulu","321","05/04/2001")  #id = 3

#add_content("programação","ruby","teste","informação...",5,"A") #cod = 1
#add_content("programação","c++","dica...","informação...",5,"B")    #cod = 2
#add_content("programação","dart","dica...","informação...",5,"c")      #cod = 3
#add_content("programação","portugol","dica...","informação...",5,"c")      #cod = 4
  
#add_responde(1,1)  #cod = 1
#add_responde(1,2)  #cod = 2
# user_id = 1 não fez sql e c

#add_responde(2,3)  #cod = 3
#add_responde(2,2)  #cod = 4

#dd_alternatives("A","Calcular porcentagens",5)
#add_alternatives("D","Realizar cálculos aritméticos de investimentos",5)
#add_alternatives("C","Calcular o resto de uma divisão inteira",5)
#add_alternatives("B","Retornar o módulo matemático (valor absoluto)",5)
#updata_user_score(5,17)
#print(consultData_raking_user())
#print(consultData_user())

