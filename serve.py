"""
VERIDEX AI Local Development & Mobile Testing Server
Serves the web application with correct WebAssembly & ONNX headers.
Auto-detects your local IP address for easy phone testing.
"""

import http.server
import socket
import socketserver
import ssl
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

PORT = 8000

def get_local_ip():
    """Find the local LAN IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class DualStackServer(http.server.ThreadingHTTPServer):
    """Multi-threaded HTTP server that handles simultaneous requests and supports both IPv4 and IPv6."""
    daemon_threads = True

    def server_bind(self):
        if getattr(self, "address_family", None) == socket.AF_INET6:
            try:
                # Enable dual-stack: accepts both IPv4 and IPv6 connections on the same port
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except Exception:
                pass
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow cross-origin resources, maps, and CDNs
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def guess_type(self, path):
        if str(path).endswith('.onnx') or str(path).endswith('.wasm'):
            return 'application/octet-stream'
        return super().guess_type(path)

def main():
    local_ip = get_local_ip()
    use_ssl = '--ssl' in sys.argv

    print("=" * 65)
    print(" [*] VERIDEX AI - MULTI-THREADED TEST SERVER")
    print("=" * 65)
    print(f" -> Localhost (IPv4):   http{'s' if use_ssl else ''}://127.0.0.1:{PORT}")
    print(f" -> Localhost (Name):   http{'s' if use_ssl else ''}://localhost:{PORT}")
    print(f" -> Mobile LAN Access:  http{'s' if use_ssl else ''}://{local_ip}:{PORT}")
    print("-" * 65)
    print(" NOTE FOR MOBILE TESTING (PHONE CAMERA & GPS):")
    print(" Modern mobile Chrome & Safari require HTTPS to activate the camera")
    print(" and GPS. For full mobile deployment, deploy to Vercel in 1 click:")
    print("   npx vercel --prod")
    print("=" * 65)

    # Attempt dual-stack IPv6 (covers both IPv6 ::1 and IPv4 127.0.0.1 / 0.0.0.0)
    try:
        DualStackServer.address_family = socket.AF_INET6
        httpd = DualStackServer(("::", PORT), CustomHandler)
    except Exception:
        DualStackServer.address_family = socket.AF_INET
        httpd = DualStackServer(("0.0.0.0", PORT), CustomHandler)

    with httpd:
        if use_ssl:
            cert_file = Path("cert.pem")
            key_file = Path("key.pem")
            if not cert_file.exists() or not key_file.exists():
                print("Generating self-signed SSL certificate for local HTTPS testing...")
                import subprocess
                subprocess.run([
                    "openssl", "req", "-x509", "-newkey", "rsa:2048",
                    "-keyout", "key.pem", "-out", "cert.pem", "-days", "365",
                    "-nodes", "-subj", "/CN=localhost"
                ])
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=cert_file, keyfile=key_file)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print(f"HTTPS enabled. Open https://{local_ip}:{PORT} on your phone.")

        print(f"Serving files from: {Path.cwd()}")
        print("Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    main()
