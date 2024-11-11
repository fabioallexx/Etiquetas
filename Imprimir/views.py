import win32print
import win32api
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Maquina
import os
from django.conf import settings
from django.contrib import messages

def imprimir_etiqueta(request, nome):
    maquina = get_object_or_404(Maquina, nome=nome)
    zpl_content = gerar_zpl(maquina.nome)

    try:
        enviar_para_impressora(zpl_content)
        return HttpResponse("Etiqueta enviada para impressão com sucesso.")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar a etiqueta para impressão: {e}", status=500)

def enviar_para_impressora(zpl):
    printer_name = "ZDesigner GK420t (EPL)"

    try:
        printer_handle = win32print.OpenPrinter(printer_name)
        job = win32print.StartDocPrinter(printer_handle, 1, ("Etiqueta", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)
        
        win32print.WritePrinter(printer_handle, zpl.encode('utf-8'))
        
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)
    except Exception as e:
        raise Exception(f"Erro ao enviar ZPL para a impressora: {e}")

def lista_maquinas(request):
    search_query = request.GET.get('search', '')
    maquinas_selecionadas = request.session.get('maquinas_selecionadas', [])
    
    if search_query:
        maquinas = Maquina.objects.filter(nome__icontains=search_query).order_by('nome')
    else:
        maquinas = Maquina.objects.filter(nome__icontains='A').order_by('nome')

    if request.method == 'POST':
        maquinas_selecionadas_post = request.POST.getlist('maquinas')

        if maquinas_selecionadas_post:
            request.session['maquinas_selecionadas'] = maquinas_selecionadas_post

            return redirect('visualizar_maquinas_selecionadas')
        else:
            messages.error(request, "Nenhuma máquina foi selecionada.")

    return render(request, 'Imprimir/maquina_list.html', {
        'maquinas': maquinas,
        'maquinas_selecionadas': maquinas_selecionadas,
        'search_query': search_query
    })

def gerar_zpl(nome):
    zpl_path = os.path.join(settings.BASE_DIR, "zpl_templates", "biblioteca.zpl")
    with open(zpl_path, "r") as file:
        zpl_template = file.read()

    zpl_template = zpl_template.replace("{Trackit}", nome)

    return zpl_template

def visualizar_etiqueta(request, nome):
    maquina = get_object_or_404(Maquina, nome=nome)

    if request.method == "POST" and request.POST.get("action") == "confirmar":
        zpl_content = gerar_zpl(maquina.nome)
        
        try:
            enviar_para_impressora(zpl_content)
            return HttpResponse("Etiqueta enviada para impressão com sucesso.")
        except Exception as e:
            return HttpResponse(f"Erro ao enviar a etiqueta para impressão: {e}", status=500)
    
    return render(request, 'Imprimir/visualizar_etiqueta.html', {'maquina': maquina})

def imprimir_etiqueta_customizada(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        
        if nome:
            zpl_content = gerar_zpl(nome)
            try:
                enviar_para_impressora(zpl_content)
                success_message = f"Etiqueta para '{nome}' enviada para impressão com sucesso."
                return render(request, 'Imprimir/imprimir_customizado.html', {'success_message': success_message})
            except Exception as e:
                error_message = f"Erro ao enviar a etiqueta para '{nome}' para impressão: {e}"
                return render(request, 'Imprimir/imprimir_customizado.html', {'error_message': error_message})
        else:
            error_message = "Nome não pode ser vazio."
            return render(request, 'Imprimir/imprimir_customizado.html', {'error_message': error_message})
    
    return render(request, 'Imprimir/imprimir_customizado.html')

def visualizar_maquinas_selecionadas(request):
    maquinas_selecionadas = request.session.get('maquinas_selecionadas', [])

    maquinas = Maquina.objects.filter(nome__in=maquinas_selecionadas)

    if request.method == 'POST':
        if 'imprimir' in request.POST:
            zpl_content = "\n".join([gerar_zpl(maquina) for maquina in maquinas_selecionadas])
            try:
                enviar_para_impressora(zpl_content)
                messages.success(request, "Etiquetas enviadas para impressão com sucesso.")
                return redirect('lista_maquinas')
            except Exception as e:
                messages.error(request, f"Erro ao enviar as etiquetas para impressão: {e}")
                return redirect('visualizar_maquinas_selecionadas')
        elif 'cancelar' in request.POST:
            request.session['maquinas_selecionadas'] = []
            return redirect('lista_maquinas')

    return render(request, 'Imprimir/visualizar_selecionadas.html', {'maquinas': maquinas})

def remover_maquina(request, nome):
    maquinas_selecionadas = request.session.get('maquinas_selecionadas', [])
    if nome in maquinas_selecionadas:
        maquinas_selecionadas.remove(nome)
        request.session['maquinas_selecionadas'] = maquinas_selecionadas
    return redirect('visualizar_maquinas_selecionadas')