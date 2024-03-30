from socket import *

# Define the IP address and port number
HOST = '127.0.0.1'
PORT = 12345

# Create a TCP server socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print('Server is ready to receive')

def create_form(message=''):
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
    <title>Color Selection</title>
    <style>
        html {{
            height: 100%;
        }}

        body{{
            padding: 0px;
            background: linear-gradient(0deg, #383d95, #040d30 90%) no-repeat #383d95;
            min-height: 100%;
            margin: 0;
            font-family: "Gill Sans", sans-serif;
            font-size: 15pt;
            color: gold;
            text-align: center;
            display: flex; 
            flex-direction: column; 
            justify-content: center;
        }}
        #layers {{
            height: 200px;
            left: 0;
            overflow: hidden;
            position: absolute;
            top: 0;
            width: 100vw;
        }}

        #layers .layer {{
            background-size: auto 100%;
            background-position: 50% 0;
            background-repeat: repeat-x;
            height: 200px;
            left: 0;
            position: absolute;
            top: 0;
            transform: translate3d(0, 0, 0);
            width: 200vw;
        }}

        @keyframes twinkle {{
            from {{ opacity: .3; }}
            to {{ opacity: 1; }}
        }}

        @keyframes layer-1 {{
            from {{ transform: translate3d(0, 0, 0); }}
            to {{ transform: translate3d(-689px, 0, 0); }}
        }}
        #layers .layer:nth-child(1) {{
            animation: twinkle 10s ease-in -5s infinite alternate, layer-1 344s linear infinite;
            background-image: url('http://imgur.com/9beLKl9.png');
        }}

        @keyframes layer-2 {{
            from {{ transform: translate3d(0, 0, 0); }}
            to {{ transform: translate3d(-699px, 0, 0); }}
        }}
        #layers .layer:nth-child(2) {{
            animation: twinkle 3s ease-in -3s infinite alternate, layer-2 120s linear infinite;
            background-image: url('http://imgur.com/46MRYFa.png');
        }}

        @keyframes layer-3 {{
            from {{ transform: translate3d(0, 0, 0); }}
            to {{ transform: translate3d(-699px, 0, 0); }}
        }}
        #layers .layer:nth-child(3) {{
            animation: twinkle 3.5s ease-in infinite alternate, layer-3 349s linear infinite;
            background-image: url('http://imgur.com/46MRYFa.png');
        }}

        @keyframes layer-4 {{
            from {{ transform: translate3d(0, 0, 0); }}
            to {{ transform: translate3d(-480px, 0, 0); }}
        }}
        #layers .layer:nth-child(4) {{
            animation: twinkle 4s ease-in -2s infinite alternate, layer-4 240s linear infinite;
            background-image: url('http://imgur.com/BqkETyl.png');
        }}

        @keyframes layer-5 {{
            from {{ transform: translate3d(0, 0, 0); }}
            to {{ transform: translate3d(-486px, 0, 0); }}
        }}
        #layers .layer:nth-child(5) {{
            animation: twinkle 5.5s ease-in infinite alternate, layer-5 243s linear infinite;
            background-image: url('http://imgur.com/x1GB77K.png');
        }}

        @keyframes shooting-star {{
            0% {{
                opacity: 1;
                transform: translate3d(0, 0, 0);
            }}
            7.5% {{
                opacity: 1;
            }}
            15% {{
                opacity: 0;
                transform: translate3d(-270px, 180px, 0);
            }}
            100% {{
                opacity:0;
            }}
        }}

        #layers:before {{
            animation: 5s linear 6s shooting-star infinite;
            background-image: url('http://imgur.com/ilhrli3.png');
            background-size: 72px 50px;
            content: ' ';
            height: 50px;
            left: 80%;
            position: absolute;
            top: -50px;
            width: 72px;
            z-index: 100;
        }}
    </style>
</head>
<body>
    <div id="layers">
        <div class="layer"></div>
        <div class="layer"></div>
        <div class="layer"></div>
        <div class="layer"></div>
        <div class="layer"></div>
    </div>
    <h2>Please choose your color</h2>
    <form id="colorForm" action="/submit" method="get">
        Select a color:
        <input type="radio" name="color" value="red">Red
        <input type="radio" name="color" value="green">Green
        <input type="submit" value="Submit">
    </form>
    <p>{message}</p>
</body>
</html>
"""

while True:
    # Accept a connection from a client
    connection_socket, addr = server_socket.accept()

    # Receive the request from the client
    request = connection_socket.recv(1024).decode()

    # Parse the request to get the requested URL
    url = request.split()[1]

    if url == '/':
        # Display the color selection form
        response = create_form()
    elif url.startswith('/submit') and '=' in url:
        # Process the form submission
        color = url.split('=')[1]
        if color == "red" or color == "green":
            response = create_form(f'Your color is <span style="color:{color};">{color}</span>!')
        else:
            # Respond with a 404 status code for unknown URLs
            response = """HTTP/1.1 404 Not Found
                    Content-Type: text/html

                    <html>
                    <head><title>Not Found</title></head>
                    <body>
                    404 Not Found
                    </body>
                    </html>
                    """
    else:
        # Respond with a 404 status code for unknown URLs
        response = """HTTP/1.1 404 Not Found
                   Content-Type: text/html

                   <html>
                   <head><title>Not Found</title></head>
                   <body>
                   404 Not Found
                   </body>
                   </html>
                   """

    # Send the response back to the client
    connection_socket.sendall(response.encode())

    # Close the connection
    connection_socket.close()
