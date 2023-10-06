# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SubsurfaceViewer(Component):
    """A SubsurfaceViewer component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; required)

- bounds (boolean | number | string | dict | list; optional)

- cameraPosition (dict; optional)

    `cameraPosition` is a dict with keys:

    - maxZoom (number; optional)

    - minZoom (number; optional)

    - rotationOrbit (number; required)

    - rotationX (number; required)

    - target (list of numbers; required)

    - zoom (number; required)

- checkDatafileSchema (boolean; optional):
    Validate JSON datafile against schema.

- colorTables (list of dicts; optional)

    `colorTables` is a list of dicts with keys:

    - colorAbove (list of 3 elements: [number, number, number]; optional)

    - colorBelow (list of 3 elements: [number, number, number]; optional)

    - colorNaN (list of 3 elements: [number, number, number]; optional)

    - colors (list of list of 4 elements: [number, number, number, number]s; required)

    - description (string; optional)

    - discrete (boolean; required)

    - name (string; required)

- coordinateUnit (a value equal to: 'mm', 'cm', 'm', 'km', 'in', 'ft-us', 'ft', 'mi', 'mm2', 'cm2', 'm2', 'ha', 'km2', 'in2', 'ft2', 'ac', 'mi2', 'mcg', 'mg', 'g', 'kg', 'oz', 'lb', 'mt', 't', 'mm3', 'cm3', 'ml', 'l', 'kl', 'm3', 'km3', 'tsp', 'Tbs', 'in3', 'fl-oz', 'cup', 'pnt', 'qt', 'gal', 'ft3', 'yd3', 'mm3/s', 'cm3/s', 'ml/s', 'cl/s', 'dl/s', 'l/s', 'l/min', 'l/h', 'kl/s', 'kl/min', 'kl/h', 'm3/s', 'm3/min', 'm3/h', 'km3/s', 'tsp/s', 'Tbs/s', 'in3/s', 'in3/min', 'in3/h', 'fl-oz/s', 'fl-oz/min', 'fl-oz/h', 'cup/s', 'pnt/s', 'pnt/min', 'pnt/h', 'qt/s', 'gal/s', 'gal/min', 'gal/h', 'ft3/s', 'ft3/min', 'ft3/h', 'yd3/s', 'yd3/min', 'yd3/h', 'C', 'F', 'K', 'R', 'ns', 'mu', 'ms', 's', 'min', 'h', 'd', 'week', 'month', 'year', 'Hz', 'mHz', 'kHz', 'MHz', 'GHz', 'THz', 'rpm', 'deg/s', 'rad/s', 'm/s', 'km/h', 'm/h', 'knot', 'ft/s', 's/m', 'min/km', 's/ft', 'Pa', 'hPa', 'kPa', 'MPa', 'bar', 'torr', 'psi', 'ksi', 'b', 'Kb', 'Mb', 'Gb', 'Tb', 'B', 'KB', 'MB', 'GB', 'TB', 'lx', 'ft-cd', 'ppm', 'ppb', 'ppt', 'ppq', 'V', 'mV', 'kV', 'A', 'mA', 'kA', 'W', 'mW', 'kW', 'MW', 'GW', 'VA', 'mVA', 'kVA', 'MVA', 'GVA', 'VAR', 'mVAR', 'kVAR', 'MVAR', 'GVAR', 'Wh', 'mWh', 'kWh', 'MWh', 'GWh', 'J', 'kJ', 'VARh', 'mVARh', 'kVARh', 'MVARh', 'GVARH', 'deg', 'rad', 'grad', 'arcmin', 'arcsec'; optional)

- coords (dict; optional)

    `coords` is a dict with keys:

    - multiPicking (boolean; optional)

    - pickDepth (number; optional)

    - visible (boolean; optional)

- editedData (dict; optional)

    `editedData` is a dict with strings as keys and values of type
    dict with keys:


- getTooltip (dict; optional):
    Override default tooltip with a callback.

    `getTooltip` is a dict with keys:


- layers (boolean | number | string | dict | list; optional)

- legend (dict; optional)

    `legend` is a dict with keys:

    - cssStyle (dict; optional)

        `cssStyle` is a dict with strings as keys and values of type
        dict with keys:


    - horizontal (boolean; optional)

    - visible (boolean; optional)

- lights (dict; optional)

    `lights` is a dict with keys:

    - ambientLight (dict; optional)

        `ambientLight` is a dict with keys:

        - color (list of 3 elements: [number, number, number]; optional)

        - intensity (number; required)

    - directionalLights (list of dicts; optional)

        `directionalLights` is a list of 1 elements: [dict with keys:

        - color (list of 3 elements: [number, number, number]; optional)

        - direction (list of 3 elements: [number, number, number]; required)

        - intensity (number; required)]

    - headLight (dict; optional)

        `headLight` is a dict with keys:

        - color (list of 3 elements: [number, number, number]; optional)

        - intensity (number; required)

    - pointLights (list of dicts; optional)

        `pointLights` is a list of 1 elements: [dict with keys:

        - color (list of 3 elements: [number, number, number]; optional)

        - intensity (number; required)

        - position (list of 3 elements: [number, number, number]; required)]

- resources (dict; optional)

    `resources` is a dict with keys:


- scale (dict; optional)

    `scale` is a dict with keys:

    - cssStyle (dict; optional)

        `cssStyle` is a dict with strings as keys and values of type
        dict with keys:


    - incrementValue (number; optional)

    - visible (boolean; optional)

    - widthPerUnit (number; optional)

- selection (dict; optional):
    Range selection of the current well.

    `selection` is a dict with keys:

    - selection (list of 2 elements: [number, number]; required)

    - well (string; required)

- toolbar (dict; optional)

    `toolbar` is a dict with keys:

    - visible (boolean; optional)

- triggerHome (number; optional):
    If changed will reset camera to default position.

- triggerResetMultipleWells (number; optional)

- views (dict; optional)

    `views` is a dict with keys:

    - layout (list of 2 elements: [number, number]; required):
        Layout for viewport in specified as [row, column].

    - marginPixels (number; optional):
        Number of pixels used for the margin in matrix mode. Defaults
        to 0.

    - showLabel (boolean; optional):
        Show views label.

    - viewports (list of dicts; required):
        Layers configuration for multiple viewports.

        `viewports` is a list of dicts with keys:

        - id (string; required):

            Viewport id.

        - isSync (boolean; optional)

        - layerIds (list of strings; optional):

            Layers to be displayed on viewport.

        - name (string; optional):

            Viewport name.

        - rotationOrbit (number; optional)

        - rotationX (number; optional)

        - show3D (boolean; optional):

            If True, displays map in 3D view, default is 2D view (False).

        - target (list of 2 elements: [number, number]; optional)

        - zoom (number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'webviz_subsurface_components'
    _type = 'SubsurfaceViewer'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, resources=Component.UNDEFINED, layers=Component.UNDEFINED, bounds=Component.UNDEFINED, views=Component.UNDEFINED, coords=Component.UNDEFINED, scale=Component.UNDEFINED, coordinateUnit=Component.UNDEFINED, toolbar=Component.UNDEFINED, legend=Component.UNDEFINED, colorTables=Component.UNDEFINED, editedData=Component.UNDEFINED, checkDatafileSchema=Component.UNDEFINED, onMouseEvent=Component.UNDEFINED, getCameraPosition=Component.UNDEFINED, isRenderedCallback=Component.UNDEFINED, onDragStart=Component.UNDEFINED, onDragEnd=Component.UNDEFINED, triggerHome=Component.UNDEFINED, triggerResetMultipleWells=Component.UNDEFINED, selection=Component.UNDEFINED, getTooltip=Component.UNDEFINED, cameraPosition=Component.UNDEFINED, lights=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'bounds', 'cameraPosition', 'checkDatafileSchema', 'colorTables', 'coordinateUnit', 'coords', 'editedData', 'getTooltip', 'layers', 'legend', 'lights', 'resources', 'scale', 'selection', 'toolbar', 'triggerHome', 'triggerResetMultipleWells', 'views']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'bounds', 'cameraPosition', 'checkDatafileSchema', 'colorTables', 'coordinateUnit', 'coords', 'editedData', 'getTooltip', 'layers', 'legend', 'lights', 'resources', 'scale', 'selection', 'toolbar', 'triggerHome', 'triggerResetMultipleWells', 'views']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SubsurfaceViewer, self).__init__(children=children, **args)
