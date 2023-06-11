

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
from account.models import UserManager,User
from chat.models import Chat

# class SendMessageView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Process the chat message and send it to WebSocket consumers
#         message = request.data.get('message')
#         # Handle the message and send it to WebSocket consumers using Channels
#         return Response({'status': 'success', 'message': message})



class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user  # Logged-in user will be the sender
        recipient_name = request.data.get('recipient')
        message_content = request.data.get('content')

       # Check if recipient exists in the database
        recipient = User.objects.filter(name=recipient_name).first()

        if not sender or not recipient:
            return Response({'status': 'error', 'message': 'Invalid sender or recipient'})

        # Create and save the message to the database
        message = Chat.objects.create(sender=sender, recipient=recipient, content=message_content)

        # Process the chat message and send it to WebSocket consumers
        # Handle the message and send it to WebSocket consumers using Channels
        
        # Return the response with the status and message
        return Response({'status': 'success', 'message': message_content})



# class ViewMessagesView(APIView):
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         sender_name = request.query_params.get('sender')
#         recipient_name = request.query_params.get('recipient')

#         # Get messages between the sender and recipient
#         messages = Chat.objects.filter(
#             sender__name=sender_name,
#             recipient__name=recipient_name
#         )

#         # Serialize the messages or perform any additional processing

#         # Return the response with the serialized messages
#         return Response({'messages': messages})














class GetMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        messages = Chat.objects.filter(sender=user) | Chat.objects.filter(recipient=user)
        message_data = [{'sender': message.sender.name, 'recipient': message.recipient.name, 'content': message.content} for message in messages]

        # Return the messages
        return Response({'status': 'success', 'messages': message_data})