from random import randint
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
import sqlite3
from .models import Produto, Compra
from django.shortcuts import redirect

def compras_list(request):

    gerador()

    compras = Compra.objects.all()
    busca = request.POST.get('busca')
    if busca:
        compras = Compra.objects.filter(cod_compra = busca)
        return render(request, 'mercado/compras_list.html', {'compras': compras})

    return render(request, 'mercado/compras_list.html', {'compras': compras})

def produto(request):

    gerador()
    
    produtos = Produto.objects.all()

    busca = request.POST.get('busca')
    
    if busca:           
        produtos = Produto.objects.filter(nome = busca)
        return render(request, 'mercado/lista_produtos.html', {'produtos': produtos})
        
    return render(request, 'mercado/lista_produtos.html', {'produtos': produtos})

def cancelar_compra(request):
    conector = sqlite3.connect('db.sqlite3')
    cursor = conector.cursor()
    
    sql = 'select * from gerador'
    cursor.execute(sql)
    codigo_compra = cursor.fetchone()

    sqlDelete = 'delete from mercado_compra where cod_compra = :param'
    cursor.execute(sqlDelete, {'param': codigo_compra[0]})
    conector.commit()

    cursor.close()
    conector.close()
    
    return redirect('produto')

def finalizar_compra(request):
    conector = sqlite3.connect('db.sqlite3')
    cursor = conector.cursor()
    sql = 'delete from gerador'
    sql2 = 'insert into mercado_compra(cod_compra, produtos, total, codigo_prod) values (?,?,?,?)'
    sql3 = 'select cod_compra from mercado_compra'

    cursor.execute(sql)
    conector.commit()

    cursor.execute(sql3)
    lista_cod = cursor.fetchall()
    lista_cod_int = []
    for l in lista_cod:
        lista_cod_int.append(l[0])
    lista_cod_int_rev = list(reversed(lista_cod_int))
    print(lista_cod_int_rev[0])
    sql4 = 'select total from mercado_compra where cod_compra = :param'
    cursor.execute(sql4, {'param': lista_cod_int_rev[0]})
    totais = cursor.fetchall()
    totai_float = []
    for t in totais:
        totai_float.append(t[0])
    total_compra = sum(totai_float)
    conector.commit()

    valores = [lista_cod_int_rev[0],"TOTAL",total_compra,""]
    cursor.execute(sql2, valores)
    conector.commit()

    cursor.close()
    conector.close()
    
    return redirect('produto')

def compra_detal(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    print(compra.cod_compra)
    conector = sqlite3.connect('db.sqlite3')
    cursor = conector.cursor()
    sql = "select cod_compra, produtos, total, codigo_prod from mercado_compra where cod_compra = :param"
    cursor.execute(sql, {'param' : compra.cod_compra})
    resposta = cursor.fetchall()
    print(resposta)
    return render(request, 'mercado/compra_detal.html', {'compra': resposta})

def compra_edit(request):
    produtos = Produto.objects.all()
    busca = request.POST.get('cod')

    if busca:
        compra = []
        prods = Produto.objects.filter(id = busca)

        conector = sqlite3.connect('db.sqlite3')
        cursor = conector.cursor()

        sql1 = 'select * from gerador'
        cursor.execute(sql1)
        codigo_produto = cursor.fetchone()
        
        esto = 0
        sqlEstoque = 'update mercado_produto set estoque = ? where id = :param'
        sqlLiquido = 'update mercado_produto set liquido = ? where nome = :param2'
        sqlBuscaLiquido = 'select liquido from mercado_produto where nome = :param3'

        for c in prods:
            compra.append(codigo_produto[0])
            compra.append(c.nome)
            compra.append(c.preco_uni)
            compra.append(c.id)

            esto = c.estoque - 1
            cursor.execute(sqlEstoque, (esto, c.id))
            conector.commit()

            cursor.execute(sqlBuscaLiquido, {'param3': c.nome})
            liqui = cursor.fetchone()
            conector.commit()
            
            totalLiquido = liqui[0] + c.preco_uni
            cursor.execute(sqlLiquido, (totalLiquido, c.nome))
            conector.commit()

        sql2 = "insert into mercado_compra(cod_compra, produtos, total, codigo_prod) values (?,?,?,?)"
        cursor.execute(sql2,compra)        
        conector.commit()
        
        # buscando o ID da compra
        sqlCod_compra = 'select cod_compra from mercado_compra'
        cursor.execute(sqlCod_compra)
        conector.commit
        compra_cod_compra = cursor.fetchall()
        compra_cod_compra.reverse()

        cursor.close()
        conector.close()

        compras = Compra.objects.filter(cod_compra = codigo_produto[0])

        totalCompra = []
        for c in compras:
            totalCompra.append(c.total)
        
        total = 0.0
        for t in totalCompra:
            total += t

        return render(request, 'mercado/compra_edit.html', {'produtos': produtos, 'prods':prods, 'compras': compras, 'total': total, 'compra_cod_compra': compra_cod_compra[0] })
    
    return render(request, 'mercado/compra_edit.html', {'produtos': produtos, })


# gerador de codigo de compra
def gerador():
    conector = sqlite3.connect('db.sqlite3')
    cursor = conector.cursor()
    sql = 'insert into gerador(codigo_compra) values (:param)'
    codigo_produto = randint(1000,10000000)
    cursor.execute(sql, {'param': codigo_produto})
    conector.commit()
    cursor.close()
    conector.close()