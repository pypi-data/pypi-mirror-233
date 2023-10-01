"""IPX800V5 X-Display."""
from enum import Enum

from .const import EXT_XDISPLAY as ext_type
from .extension import Extension
from .ipx800 import IPX800


class XDisplayScreenType(Enum):
    """Types of X-Display screen."""

    Thermostat = 1
    Light = 2
    Home = 3
    Cover = 4
    Date = 5
    NightLight = 6
    Temperature = 7
    Humidity = 8
    Luminosity = 9


class XDisplayScreen:
    """Represent an X-Display screen."""

    def __init__(self, id: int, id_type: int, name: str):
        self._id = id
        self._id_type = id_type
        self._name = name

    @property
    def id(self) -> int:
        """Return the name of a X-Display screen."""
        return self._id

    @property
    def name(self) -> str:
        """Return the name of a X-Display screen."""
        return self._name

    @property
    def type(self) -> str:
        """Return the name of a X-Display screen."""
        return XDisplayScreenType(self._id_type).name


class XDisplay(Extension):
    """Represent an X-Display."""

    def __init__(self, ipx: IPX800, ext_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number)
        self.io_on_screen_id = self._config["ioOnScreen_id"]
        self.io_lock_screen_id = self._config["ioLockSet_id"]
        self.ana_current_screen_id = self._config["anaSelectScreen_id"]
        self._screens: list[XDisplayScreen] = []

    @property
    def autoOff(self) -> int:
        """Return the current delay before X-Display standby."""
        return self._config["autoOff"]

    @property
    def sensitive(self) -> int:
        """Return the current sensitivity of X-Display screen."""
        return self._config["sensitive"]

    @property
    def version(self) -> int:
        """Return the version of the X-Display."""
        return 2 if self._config["bVersion2"] is True else 1

    # Screens
    async def refresh_screens(self) -> None:
        screens: list[XDisplayScreen] = []
        for id in range(len([s for s in self._config["screenRef"] if s != 0])):
            screens.append(
                XDisplayScreen(
                    id=id,
                    id_type=self._config["screensType"][id],
                    name=await self._ipx.get_str(self._config["strScreenName_id"][id]),
                )
            )
        self._screens = screens

    @property
    def screens(self) -> list[XDisplayScreen]:
        """Return X-Display screens."""
        return self._screens

    @property
    async def current_screen_id(self) -> int:
        """Return the current screen reference."""
        return int(await self._ipx.get_ana(self.ana_current_screen_id))

    async def set_screen(self, id: int) -> None:
        """Set Screen."""
        if not 0 <= id <= 31:
            raise ValueError("Screen id must be between 0 and 31")
        await self._ipx.update_ana(self.ana_current_screen_id, id)

    # Screen ON/OFF
    @property
    async def screen_status(self) -> bool:
        """Return the current screen status."""
        return not await self._ipx.get_io(self.io_on_screen_id)

    async def screen_on(self) -> None:
        """Turn on the screen."""
        await self._ipx.update_io(self.io_on_screen_id, False)

    async def screen_off(self) -> None:
        """Turn off the screen."""
        await self._ipx.update_io(self.io_on_screen_id, True)

    async def screen_toggle(self) -> None:
        """Toggle the screen."""
        await self._ipx.update_io(self.io_on_screen_id, True, "toggle")

    # Screen LOCK
    @property
    async def screen_lock_status(self) -> bool:
        """Return the current screen lock status."""
        return await self._ipx.get_io(self.io_lock_screen_id)

    async def screen_lock(self) -> None:
        """Lock the screen."""
        await self._ipx.update_io(self.io_lock_screen_id, True)

    async def screen_unlock(self) -> None:
        """Unlock the screen."""
        await self._ipx.update_io(self.io_lock_screen_id, False)

    async def screen_toggle_lock(self) -> None:
        """Toggle the screen lock."""
        await self._ipx.update_io(self.io_lock_screen_id, True, "toggle")
