from flask import Flask, request, render_template, g
import cx_Oracle

app = Flask(__name__)

def conectar_bd():
    if 'db' not in g:
        try:
            dsn_tns = cx_Oracle.makedsn('host', 'porta', service_name='base')
            g.db = cx_Oracle.connect(user='usuario', password='senha', dsn=dsn_tns)
            app.logger.info("Conexão com o banco de dados foi bem-sucedida")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            app.logger.error(f"Erro ao conectar ao banco de dados: {error.code} - {error.message}")
            raise
    return g.db


def consultar_dados(cd_pessoa_fisica):
    conn = conectar_bd()
    
    select_query = """
    select b.cd_usuario_plano,
           a.cd_pessoa_fisica,
           obter_nome_PF(a.cd_pessoa_fisica) nome,
           pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
    from pls_segurado a,
         pls_segurado_carteira b
    where a.nr_sequencia = b.nr_seq_segurado
      and a.cd_pessoa_fisica = :cd_pessoa_fisica
      and a.nr_seq_plano in (3, 44)
      and a.ie_situacao_atend in ('A', 'F')
    order by a.nr_seq_plano asc
    """
    
    app.logger.info(f"Executando consulta SQL: {select_query} com cd_pessoa_fisica: {cd_pessoa_fisica}")
    
    cursor = conn.cursor()
    cursor.execute(select_query, {'cd_pessoa_fisica': cd_pessoa_fisica})
    result = cursor.fetchall()
    
    app.logger.info(f"Resultado da consulta: {result}")
    
    cursor.close()
    conn.close()
    
    return result

def executar_updates(cd_pessoa_fisica):
    conn = conectar_bd()
    
    updates = [
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (3,44)
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (3,44)
        )
        """,
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select '20' || pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (42)
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (42)
        )
        """,
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select '40' || pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (5)
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (5)
        )
        """
    ]
    
    for sql_update in updates:
        cursor = conn.cursor()
        cursor.execute(sql_update, {'cd_pessoa_fisica': cd_pessoa_fisica})
        conn.commit()
        cursor.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    cd_pessoa_fisica = None
    if request.method == 'POST':
        cd_pessoa_fisica = request.form['codigoInput']
        resultados = consultar_dados(cd_pessoa_fisica)
    return render_template('home.html', resultados=resultados, cd_pessoa_fisica=cd_pessoa_fisica)

@app.route('/executar_updates', methods=['POST'])
def executar_updates_route():
    cd_pessoa_fisica = request.form['cd_pessoa_fisica']
    executar_updates(cd_pessoa_fisica)
    resultados = consultar_dados(cd_pessoa_fisica)
    return render_template('home.html', resultados=resultados, cd_pessoa_fisica=cd_pessoa_fisica)

if __name__ == '__main__':
    app.run(debug=True)
