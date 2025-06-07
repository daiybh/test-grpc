
set path=%path%;"E:\codes\vcpkg\packages\protobuf_x64-windows\tools\protobuf"

mkdir chat
protoc --go_out=./chat ^
 --go_opt=paths=source_relative ^
 --go-grpc_out=./chat ^
 --go-grpc_opt=paths=source_relative ^
 -I../../protos ../../protos/chat.proto

