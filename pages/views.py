from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
import os

def react_view(request):
    """Serve o frontend React apenas para rotas não reconhecidas."""
    if request.path.startswith('/api/') or request.path == '/csrf/':
        return JsonResponse({'status': 'error', 'message': 'Rota não encontrada'}, status=404)
    return render(request, os.path.join(settings.BASE_DIR, 'frontend', 'index.html'))

def get_csrf_token(request):
    """Retorna o token CSRF."""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@csrf_exempt
def login_user(request):
    """Autentica o usuário."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'is_admin': user.is_staff})
            return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato de dados inválido.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard_view(request):
    """Retorna informações do painel de administração."""
    return JsonResponse({'message': 'Bem-vindo ao painel de administração!'})

@csrf_exempt
def menu_items(request):
    """Gerencia itens do menu."""
    if request.method == 'GET':
        MENU_ITEMS = [
            {'id': 1, 'name': 'Kebab', 'price': 15.99},
            {'id': 2, 'name': 'Hummus', 'price': 7.99},
        ]
        return JsonResponse(MENU_ITEMS, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        MENU_ITEMS.append(data)
        return JsonResponse({'status': 'success', 'item': data})
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=405)

@login_required
def whoami(request):
    """Retorna o estado de autenticação do usuário."""
    return JsonResponse({
        'is_authenticated': True,
        'username': request.user.username,
    })

@csrf_exempt
def logout_user(request):
    """Realiza o logout do usuário."""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logout realizado com sucesso.'})
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'}, status=405)