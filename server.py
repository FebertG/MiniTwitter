from concurrent import futures
import grpc
import minitwitter_pb2
import minitwitter_pb2_grpc
from db_connection import get_db_connection


class MiniTwitterServicer(minitwitter_pb2_grpc.MiniTwitterServicer):

    def registerUser(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzamy, czy użytkownik o podanym emailu lub nazwie już istnieje
        cursor.execute("SELECT UserID FROM Users WHERE Name = ? OR Email = ?", request.name, request.email)
        existing_user = cursor.fetchone()

        if existing_user is not None:
            return minitwitter_pb2.Response(status="User with this name or email already exists")

        # Dodajemy nowego użytkownika do bazy danych
        cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", request.name, request.email)
        conn.commit()
        conn.close()

        return minitwitter_pb2.Response(status="User registered successfully")

    def loginUser(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzamy, czy użytkownik o danej nazwie lub emailu istnieje w bazie danych
        cursor.execute("SELECT UserID FROM Users WHERE Name = ? AND Email = ?", request.name, request.email)
        user = cursor.fetchone()

        if user is None:
            return minitwitter_pb2.Response(status="User not found")

        return minitwitter_pb2.Response(status="Login successful")

    def sendMessage(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzamy, czy użytkownik o danej nazwie istnieje w bazie danych
        cursor.execute("SELECT UserID FROM Users WHERE Name = ?", request.name)
        user_id = cursor.fetchone()

        if user_id is None:
            # Jeśli użytkownik nie istnieje, rejestrujemy go w bazie danych (dodajemy Email, jeśli potrzebne)
            cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", request.name, f"{request.name}@example.com")
            conn.commit()
            # Pobieramy ID nowo dodanego użytkownika
            cursor.execute("SELECT UserID FROM Users WHERE Name = ?", request.name)
            user_id = cursor.fetchone()[0]
            print(f"Nowy użytkownik '{request.name}' został zarejestrowany.")

        user_id = user_id[0]  # UserID z bazy danych

        # Wstawiamy wiadomość do tabeli Messages
        cursor.execute("INSERT INTO Messages (UserID, MessageText, Timestamp) VALUES (?, ?, GETDATE())",
                       user_id, request.content)
        conn.commit()
        conn.close()

        return minitwitter_pb2.Response(status="Message received")

    def getMessages(self, request, context):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobieramy najnowsze 'n' wiadomości z datą i godziną
        cursor.execute("""
            SELECT TOP (?) Users.Name, Messages.MessageText, FORMAT(Messages.Timestamp, 'yyyy-MM-dd HH:mm:ss')
            FROM Messages
            JOIN Users ON Messages.UserID = Users.UserID
            ORDER BY Messages.Timestamp DESC
        """, request.count)

        messages = [f"{row[0]} ({row[2]}): {row[1]}" for row in cursor.fetchall()]
        conn.close()

        return minitwitter_pb2.MessagesResponse(messages=messages)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #wielowątkowość
    minitwitter_pb2_grpc.add_MiniTwitterServicer_to_server(MiniTwitterServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server running on port 50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
