import grpc
from concurrent import futures
import run_codegen
import chat_pb2_grpc, chat_pb2

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        for request in request_iterator:
            yield chat_pb2.ChatResponse(user_id="server", text=f"pySerer Echo: {request.text}")

server = grpc.server(futures.ThreadPoolExecutor())
chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()