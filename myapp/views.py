from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

@api_view(['GET'])
@permission_classes([])
def public_endpoint(request):
    return Response({"message": "This is a public endpoint. No authentication required."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    user = request.user
    token = Token.objects.get(user=user)
    return Response({"message": f"This is a protected endpoint. Welcome, {user.username}! Your token is {token.key}"})