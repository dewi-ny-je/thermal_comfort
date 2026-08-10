"""template conftest."""
import pytest
from pytest_homeassistant_custom_component.common import (
    assert_setup_component,
    async_mock_service,
)

from homeassistant.setup import async_setup_component

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Auto enable custom integration."""
    yield


@pytest.fixture
def calls(hass):
    """Track calls to a mock service."""
    return async_mock_service(hass, "test", "automation")


@pytest.fixture
def source_states():
    """Source sensor states to seed before the integration is set up.

    Parametrize ``source_states`` with a mapping of entity id to state to give a
    test the readings it computes from. A value may also be a
    ``(state, attributes)`` tuple when the test needs the source entity to carry
    a device class or a unit of measurement.
    """
    return {}


@pytest.fixture
async def start_ha(hass, source_states, domains, config, caplog):
    """Do setup of integration."""
    for entity_id, state in source_states.items():
        attributes = None
        if isinstance(state, tuple):
            state, attributes = state
        hass.states.async_set(entity_id, state, attributes)
    for domain, count in domains:
        with assert_setup_component(count, domain):
            assert await async_setup_component(
                hass,
                domain,
                config,
            )
        await hass.async_block_till_done()
    await hass.async_start()
    await hass.async_block_till_done()


@pytest.fixture
async def caplog_setup_text(caplog):
    """Return setup log of integration."""
    yield caplog.text
