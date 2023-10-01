
from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import OK

from wx import MessageDialog
from wx import NewIdRef
from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from codeallybasic.Singleton import (Singleton)

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface
from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugintypes.PluginDataTypes import ToolsPluginMap
from pyutplugins.plugintypes.PluginDataTypes import InputPluginMap
from pyutplugins.plugintypes.PluginDataTypes import OutputPluginMap
from pyutplugins.plugintypes.PluginDataTypes import PluginList
from pyutplugins.plugintypes.PluginDataTypes import PluginIDMap

from pyutplugins.ioplugins.IODTD import IODTD
from pyutplugins.ioplugins.IOGML import IOGML
from pyutplugins.ioplugins.IOJava import IOJava
from pyutplugins.ioplugins.IOPdf import IOPdf
from pyutplugins.ioplugins.IOPython import IOPython
from pyutplugins.ioplugins.IOWxImage import IOWxImage
from pyutplugins.ioplugins.IOXml import IOXml
from pyutplugins.ioplugins.IOMermaid import IOMermaid

from pyutplugins.toolplugins.ToolArrangeLinks import ToolArrangeLinks
from pyutplugins.toolplugins.ToolAscii import ToolAscii
from pyutplugins.toolplugins.ToolOrthogonalLayoutV2 import ToolOrthogonalLayoutV2
from pyutplugins.toolplugins.ToolSugiyama import ToolSugiyama
from pyutplugins.toolplugins.ToolTransforms import ToolTransforms


TOOL_PLUGIN_NAME_PREFIX: str = 'Tool'
IO_PLUGIN_NAME_PREFIX:   str = 'IO'


class PluginManager(Singleton):
    """
    Is responsible for:

    * Identifying the plugin loader files
    * Creating tool and Input/Output Menu ID References
    * Providing the callbacks to invoke the appropriate methods on the
    appropriate pyutplugins to invoke there functionality.

    Plugin Loader files have the following format:

    ToolPlugin=packageName.PluginModule
    IOPlugin=packageName.PluginModule

    By convention prefix the plugin tool module name with the characters 'Tool'
    By convention prefix the plugin I/O module with the characters 'IO'

    """
    IO_PLUGINS:   PluginList = PluginList([IOMermaid, IODTD, IOGML, IOJava, IOPdf, IOPython, IOWxImage, IOXml])
    TOOL_PLUGINS: PluginList = PluginList([ToolArrangeLinks, ToolAscii, ToolOrthogonalLayoutV2, ToolSugiyama, ToolTransforms])

    # noinspection PyAttributeOutsideInit
    def init(self,  *args, **kwargs):
        """
        Expects a pluginAdapter parameter in kwargs

        Args:
            *args:
            **kwargs:
        """

        self.logger: Logger = getLogger(__name__)

        self._pluginPreferences: PluginPreferences = PluginPreferences()
        # These are lazily built
        self._toolPluginsMap:   ToolsPluginMap   = ToolsPluginMap()
        self._inputPluginsMap:  InputPluginMap   = InputPluginMap()
        self._outputPluginsMap: OutputPluginMap  = OutputPluginMap()

        self._inputPluginClasses:  PluginList = cast(PluginList, None)
        self._outputPluginClasses: PluginList = cast(PluginList, None)

        self._pluginAdapter: IPluginAdapter = kwargs['pluginAdapter']

    @property
    def inputPlugins(self) -> PluginList:
        """
        Get the input pyutplugins.

        Returns:  A list of classes (the pyutplugins classes).
        """
        if self._inputPluginClasses is None:
            # noinspection PyAttributeOutsideInit
            self._inputPluginClasses = PluginList([])
            for plugin in PluginManager.IO_PLUGINS:
                pluginClass = cast(type, plugin)
                classInstance = pluginClass(None)
                if classInstance.inputFormat is not None:
                    self._inputPluginClasses.append(plugin)
        return self._inputPluginClasses

    @property
    def outputPlugins(self) -> PluginList:
        """
        Get the output pyutplugins.

        Returns:  A list of classes (the pyutplugins classes).
        """
        if self._outputPluginClasses is None:
            # noinspection PyAttributeOutsideInit
            self._outputPluginClasses = PluginList([])
            for plugin in PluginManager.IO_PLUGINS:
                pluginClass = cast(type, plugin)
                classInstance = pluginClass(None)
                if classInstance.outputFormat is not None:
                    self._outputPluginClasses.append(plugin)

        return self._outputPluginClasses

    @property
    def toolPlugins(self) -> PluginList:
        """
        Get the tool pyutplugins.

        Returns:    A list of classes (the pyutplugins classes).
        """
        return PluginManager.TOOL_PLUGINS

    @property
    def toolPluginsMap(self) -> ToolsPluginMap:
        if len(self._toolPluginsMap.pluginIdMap) == 0:
            self._toolPluginsMap.pluginIdMap = self.__mapWxIdsToPlugins(PluginManager.TOOL_PLUGINS)
        return self._toolPluginsMap

    @property
    def inputPluginsMap(self) -> InputPluginMap:
        if len(self._inputPluginsMap.pluginIdMap) == 0:
            self._inputPluginsMap.pluginIdMap = self.__mapWxIdsToPlugins(self.inputPlugins)
        return self._inputPluginsMap

    @property
    def outputPluginsMap(self) -> OutputPluginMap:
        if len(self._outputPluginsMap.pluginIdMap) == 0:
            self._outputPluginsMap.pluginIdMap = self.__mapWxIdsToPlugins(self.outputPlugins)
        return self._outputPluginsMap

    def doToolAction(self, wxId: int):
        """
        Args:
            wxId:   The ID ref of the menu item
        """
        pluginMap: PluginIDMap = self.toolPluginsMap.pluginIdMap

        # TODO: Fix this later for mypy
        clazz: type = pluginMap[wxId]   # type: ignore
        # Create a plugin instance
        pluginInstance: ToolPluginInterface = clazz(pluginAdapter=self._pluginAdapter)

        # Do plugin functionality
        BeginBusyCursor()
        try:
            pluginInstance.executeTool()
            self.logger.debug(f"After tool plugin do action")
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
        EndBusyCursor()

    def doImport(self, wxId: int):
        """
        Args:
            wxId:       The ID ref of the menu item
        """
        idMap:        PluginIDMap    = self.inputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(pluginAdapter=self._pluginAdapter)
        self._doIOAction(methodToCall=plugInstance.executeImport)

    def doExport(self, wxId: int):
        """
        Args:
            wxId:       The ID ref of the menu item
        """
        idMap:        PluginIDMap  = self.outputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(pluginAdapter=self._pluginAdapter)
        self._doIOAction(methodToCall=plugInstance.executeExport)

    def _doIOAction(self, methodToCall: Callable):
        """
        Args:
            methodToCall:
        """

        try:
            wxYield()
            methodToCall()
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            booBoo: MessageDialog = MessageDialog(parent=None,
                                                  message=f'An error occurred while executing the selected plugin - {e}',
                                                  caption='Error!', style=OK | ICON_ERROR)
            booBoo.ShowModal()

    def __mapWxIdsToPlugins(self, pluginList: PluginList) -> PluginIDMap:

        pluginMap: PluginIDMap = cast(PluginIDMap, {})

        nb: int = len(pluginList)

        for x in range(nb):
            wxId: int = NewIdRef()

            pluginMap[wxId] = pluginList[x]

        return pluginMap
