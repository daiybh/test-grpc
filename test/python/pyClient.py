import grpc
import threading
import run_codegen

import chat_pb2
import chat_pb2_grpc

def run_client():
    # 创建 gRPC 通道和客户端存根
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    # 创建双向流
    stream = stub.Chat()

    # 启动线程接收服务端响应
    def receive_responses():
        try:
            for response in stream:
                print(f"[{response.user_id}] {response.text}")
        except grpc.RpcError as e:
            print(f"接收错误: {e.code()}: {e.details()}")

    receiver = threading.Thread(target=receive_responses)
    receiver.daemon = True
    receiver.start()

    # 主线程发送用户输入
    try:
        while True:
            text = input("你: ")  # 用户输入消息
            if text.lower() == 'exit':
                break
            request = chat_pb2.ChatRequest(user_id="python_client", text=text)
            stream.write(request)  # 发送消息到服务端
    except KeyboardInterrupt:
        pass
    finally:
        stream.done_writing()  # 结束发送
        receiver.join()        # 等待接收线程结束
        channel.close()

if __name__ == '__main__':
    run_client()