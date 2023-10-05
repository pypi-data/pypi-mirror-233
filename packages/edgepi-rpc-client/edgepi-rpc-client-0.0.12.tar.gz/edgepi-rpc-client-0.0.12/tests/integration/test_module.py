import subprocess
import os
import pytest
from tempfile import TemporaryDirectory

def test_rpc_client_install():
    """Test client import"""
    
    # Build the wheel
    subprocess.check_call(["pip3", "install", "build"])
    subprocess.check_call(["python", "-m", "build"])

    # Locate the wheel in the dist directory
    wheel_file = next((file for file in os.listdir("dist") if file.endswith(".whl")), None)
    assert wheel_file, "Wheel file not found"

    with TemporaryDirectory() as tempdir:
        # Install the wheel inside temp directory
        subprocess.check_call(["pip3", "install", os.path.join("dist", wheel_file), "--target", tempdir])

        # Add the temporary directory to sys.path so that we can import from there
        import sys
        sys.path.insert(0, tempdir)

        # Check imports
        # pylint: disable=import-outside-toplevel, unused-import
        from edgepi_rpc_client.services.led.client_led_service import ClientLEDService
        from edgepi_rpc_client.services.led.led_pb_enums import LEDPins

        # Clean up sys.path
        sys.path.remove(tempdir)
