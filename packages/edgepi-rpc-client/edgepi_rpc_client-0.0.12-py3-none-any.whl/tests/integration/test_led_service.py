"""LEDService integration tests"""
import pytest
from edgepi_rpc_client.services.led.client_led_service import ClientLEDService
from edgepi_rpc_client.services.led.led_pb_enums import LEDPins

@pytest.fixture(name='led_service')
def fixture_test_led_service():
    """Inits new led serviceclient for testing"""
    return ClientLEDService('tcp://localhost:5555')

@pytest.mark.parametrize(
    'led_pin',
    [
        (LEDPins.LED1),
        (LEDPins.LED2),
        (LEDPins.LED3),
        (LEDPins.LED4),
        (LEDPins.LED5),
        (LEDPins.LED6),
        (LEDPins.LED7),
        (LEDPins.LED8)
    ]
)
def test_toggle_led(led_service, led_pin):
    """Test for toggle_led"""
    response = led_service.toggle_led(led_pin)

    assert response == f'Successfully toggled {led_pin} to the opposite state.'

@pytest.mark.parametrize(
    'led_pin',
    [
        (LEDPins.LED1),
        (LEDPins.LED2),
        (LEDPins.LED3),
        (LEDPins.LED4),
        (LEDPins.LED5),
        (LEDPins.LED6),
        (LEDPins.LED7),
        (LEDPins.LED8)
    ]
)
def test_turn_led_on(led_service, led_pin):
    """Test for turn_led_on"""
    response = led_service.turn_led_on(led_pin)

    assert response == f'Successfully turned on {led_pin}.'

@pytest.mark.parametrize(
    'led_pin',
    [
        (LEDPins.LED1),
        (LEDPins.LED2),
        (LEDPins.LED3),
        (LEDPins.LED4),
        (LEDPins.LED5),
        (LEDPins.LED6),
        (LEDPins.LED7),
        (LEDPins.LED8)
    ]
)
def test_turn_led_off(led_service, led_pin):
    """Test for turn_led_off"""
    response = led_service.turn_led_off(led_pin)

    assert response == f'Successfully turned off {led_pin}.'
