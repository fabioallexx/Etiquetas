import win32print
import win32api
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Maquina
import os
from django.conf import settings

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
    maquinas = Maquina.objects.all()
    return render(request, 'Imprimir/leitor_list.html', {'maquinas': maquinas})

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