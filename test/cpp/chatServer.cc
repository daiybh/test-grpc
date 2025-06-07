#include <grpcpp/grpcpp.h>
#include "chat.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::ServerReaderWriter;
using grpc::Status;
using namespace chat;
class ChatServiceImpl final : public ChatService::Service {
  Status Chat(ServerContext* context,
              ServerReaderWriter<ChatResponse, ChatRequest>* stream) override {
    ChatRequest request;
    while (stream->Read(&request)) {  // 持续读取客户端流
      std::string response_text = "Echo: " + request.text();
      ChatResponse response;
      response.set_user_id("server");
      response.set_text(response_text);
      stream->Write(response);  // 向客户端发送响应流
    }
    return Status::OK;
  }
};

int main() {
  ServerBuilder builder;
  builder.AddListeningPort("0.0.0.0:50051", grpc::InsecureServerCredentials());
  ChatServiceImpl service;
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  server->Wait();
  return 0;
}