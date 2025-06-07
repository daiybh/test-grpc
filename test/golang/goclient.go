package main

import (
	"bufio"
	pb "testGRPC/chat"

	"context"
	"log"
	"os"

	"google.golang.org/grpc"
)

func main() {
	conn, _ := grpc.Dial("localhost:50051", grpc.WithInsecure())
	client := pb.NewChatServiceClient(conn)
	stream, _ := client.Chat(context.Background())

	// 接收响应
	go func() {
		for {
			resp, _ := stream.Recv()
			log.Printf("[%s] %s", resp.UserId, resp.Text)
		}
	}()

	// 发送请求
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		stream.Send(&pb.ChatRequest{UserId: "client", Text: scanner.Text()})
	}
}
