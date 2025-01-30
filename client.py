import grpc
import minitwitter_pb2
import minitwitter_pb2_grpc

def register_user(user_name, email):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.registerUser(minitwitter_pb2.RegisterUserRequest(name=user_name, email=email))
        print("Server response:", response.status)

def login_user(user_name, email):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.loginUser(minitwitter_pb2.LoginUserRequest(name=user_name, email=email))
        print("Server response:", response.status)
        return response.status == "Login successful"  # Zwracamy True, jeśli login był udany

def send_message(user_name, content):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.sendMessage(minitwitter_pb2.MessageRequest(name=user_name, content=content))
        print("Server response:", response.status)

def get_messages(count):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = minitwitter_pb2_grpc.MiniTwitterStub(channel)
        response = stub.getMessages(minitwitter_pb2.GetMessagesRequest(count=count))
        print("Messages:")
        for message in response.messages:
            print(f"- {message}")

def main():
    user_logged_in = False
    user_name = ""
    user_email = ""

    while True:
        print("\n--- MiniTwitter ---")
        print("1. Register")
        print("2. Login")
        if user_logged_in:
            print("3. Send a message")
            print("4. Get messages")
        print("5. Exit")
        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == "1":
            user_name = input("Enter your username: ")
            user_email = input("Enter your email: ")
            register_user(user_name, user_email)

        elif choice == "2":
            user_name = input("Enter your username: ")
            user_email = input("Enter your email: ")
            user_logged_in = login_user(user_name, user_email)

        elif choice == "3" and user_logged_in:
            content = input("Enter your message (max 80 characters): ")
            if len(content) > 80:
                print("Message too long! It must be 80 characters or less.")
            else:
                send_message(user_name, content)

        elif choice == "4" and user_logged_in:
            try:
                count = int(input("How many messages to retrieve? "))
                if count <= 0:
                    print("Please enter a positive number.")
                else:
                    get_messages(count)
            except ValueError:
                print("Invalid number. Please enter a valid integer.")

        elif choice == "5":
            print("Exiting MiniTwitter...")
            break

        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    main()
