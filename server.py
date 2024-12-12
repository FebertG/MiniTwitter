from concurrent import futures
import grpc
import minitwitter_pb2
import minitwitter_pb2_grpc
from db_connection import get_db_connection

class MiniTwitterServicer(minitwitter_pb2_grpc.MiniTwitterServicer):
    def sendMessage(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Messages (content, timestamp) VALUES (?, GETDATE())", request.content)
        conn.commit()
        conn.close()
        return minitwitter_pb2.Response(status="Message received")

    def getMessages(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (?) content FROM Messages ORDER BY timestamp DESC", request.count)
        messages = [row[0] for row in cursor.fetchall()]
        conn.close()
        return minitwitter_pb2.MessagesResponse(messages=messages)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    minitwitter_pb2_grpc.add_MiniTwitterServicer_to_server(MiniTwitterServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server running on port 50052")
    server.wait_for_termination()
    print("aaa")

if __name__ == "__main__":
    serve()

