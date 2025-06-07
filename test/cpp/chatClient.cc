#include <grpcpp/grpcpp.h>
#include "chat.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::ClientReaderWriter;
using grpc::Status;
using namespace chat;
class ChatClient {
 public:
  ChatClient(std::shared_ptr<Channel> channel)
      : stub_(ChatService::NewStub(channel)) {}

  void Chat() {
    ClientContext context;
    std::shared_ptr<ClientReaderWriter<ChatRequest, ChatResponse>> stream(
        stub_->Chat(&context));

    // 启动线程接收服务端响应
    std::thread reader([stream]() {
      ChatResponse response;
      while (stream->Read(&response)) {  // 持续读取服务端流
        std::cout << "[" << response.user_id() << "] " << response.text() << std::endl;
      }
    });

    // 主线程发送客户端请求
    std::string input;
    while (std::getline(std::cin, input)) {
      ChatRequest request;
      request.set_user_id("client");
      request.set_text(input);
      stream->Write(request);
    }
    stream->WritesDone();  // 结束发送
    reader.join();         // 等待接收线程结束
  }

 private:
  std::unique_ptr<ChatService::Stub> stub_;
};

int main() {
  ChatClient client(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
  client.Chat();
  return 0;
}