import grpc
import minitwitter_pb2
import minitwitter_pb2_grpc

def send_message(content):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.sendMessage(minitwitter_pb2.MessageRequest(content=content))
        print("Server response:", response.status)

def get_messages(count):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.getMessages(minitwitter_pb2.GetMessagesRequest(count=count))
        print("Messages:", response.messages)

if __name__ == "__main__":
    send_message("Hello, MiniTwitter!")
    get_messages(5)
