"""
ngrok Helper for Large File Uploads
====================================
This module helps set up ngrok tunneling for large file uploads
that exceed GitHub Codespaces/FastAPI default limits.

Usage:
    1. Set NGROK_AUTH_TOKEN environment variable
    2. Run: python ngrok_helper.py
    3. Use the provided ngrok URL in your frontend
"""
import os
import sys
import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_ngrok_tunnel(
    port: int = 8000,
    auth_token: Optional[str] = None,
    domain: Optional[str] = None
) -> Optional[str]:
    """
    Set up an ngrok tunnel for the backend.
    
    Args:
        port: Local port to tunnel
        auth_token: ngrok auth token (or from env var NGROK_AUTH_TOKEN)
        domain: Custom ngrok domain (optional)
    
    Returns:
        The public ngrok URL or None if failed
    """
    try:
        from pyngrok import ngrok, conf
        
        # Get auth token
        token = auth_token or os.getenv('NGROK_AUTH_TOKEN')
        if not token:
            logger.error("No ngrok auth token provided. Set NGROK_AUTH_TOKEN env var.")
            return None
        
        # Set configuration
        conf.get_default().auth_token = token
        
        # Close any existing tunnels
        ngrok.kill()
        
        # Connect
        logger.info(f"Starting ngrok tunnel on port {port}...")
        
        if domain:
            tunnel = ngrok.connect(port, domain=domain)
        else:
            tunnel = ngrok.connect(port)
        
        public_url = tunnel.public_url
        logger.info(f"✅ ngrok tunnel established: {public_url}")
        logger.info(f"   Local: http://localhost:{port}")
        logger.info(f"   Public: {public_url}")
        
        return public_url
        
    except ImportError:
        logger.error("pyngrok not installed. Install with: pip install pyngrok")
        return None
    except Exception as e:
        logger.error(f"Failed to set up ngrok tunnel: {e}")
        return None


def print_setup_instructions(ngrok_url: str):
    """Print setup instructions for the user."""
    print("\n" + "=" * 60)
    print("🌐 NGROK TUNNEL ESTABLISHED")
    print("=" * 60)
    print(f"\n📡 Public URL: {ngrok_url}")
    print("\n🔧 Frontend Configuration:")
    print(f"   Set VITE_API_URL={ngrok_url} in your frontend .env file")
    print("\n📋 Example .env:")
    print(f"   VITE_API_URL={ngrok_url}")
    print("\n⚠️  Important Notes:")
    print("   - This tunnel will remain active until you stop it")
    print("   - The URL changes each time you restart ngrok (unless using a custom domain)")
    print("   - Keep your auth token secret!")
    print("\n🛑 To stop the tunnel:")
    print("   Press Ctrl+C or run: ngrok kill")
    print("=" * 60 + "\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Set up ngrok tunnel for large file uploads')
    parser.add_argument('--port', type=int, default=8000, help='Local port (default: 8000)')
    parser.add_argument('--token', type=str, help='ngrok auth token')
    parser.add_argument('--domain', type=str, help='Custom ngrok domain (optional)')
    
    args = parser.parse_args()
    
    # Get token from args or environment
    token = args.token or os.getenv('NGROK_AUTH_TOKEN')
    
    if not token:
        print("\n❌ Error: No ngrok auth token provided!")
        print("\n🔑 How to get your auth token:")
        print("   1. Sign up at https://ngrok.com")
        print("   2. Go to https://dashboard.ngrok.com/get-started/your-authtoken")
        print("   3. Copy your authtoken")
        print("\n📝 Usage:")
        print("   Option 1: Set environment variable:")
        print("      export NGROK_AUTH_TOKEN=your_token_here")
        print("      python ngrok_helper.py")
        print("\n   Option 2: Pass as argument:")
        print("      python ngrok_helper.py --token your_token_here")
        print("\n   Option 3: Use ngrok CLI directly:")
        print("      ngrok config add-authtoken your_token_here")
        print("      ngrok http 8000")
        sys.exit(1)
    
    # Set up tunnel
    url = setup_ngrok_tunnel(args.port, token, args.domain)
    
    if url:
        print_setup_instructions(url)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping ngrok tunnel...")
            try:
                from pyngrok import ngrok
                ngrok.kill()
                print("✅ Tunnel closed.")
            except:
                pass
    else:
        print("\n❌ Failed to establish ngrok tunnel.")
        sys.exit(1)


if __name__ == '__main__':
    main()
