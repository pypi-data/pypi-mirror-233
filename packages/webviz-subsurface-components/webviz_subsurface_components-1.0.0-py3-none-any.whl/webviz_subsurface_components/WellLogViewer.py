# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WellLogViewer(Component):
    """A WellLogViewer component.


Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- axisMnemos (dict; optional):
    Names for axes.

- axisTitles (dict; optional):
    Log mnemonics for axes.

- colorTables (list of boolean | number | string | dict | lists; required):
    Prop containing color table data.

- domain (list of numbers; optional):
    Initial visible interval of the log data.

- horizontal (boolean; optional):
    Orientation of the track plots on the screen. Default is False.

- maxContentZoom (number; optional):
    The maximum zoom value.

- options (dict; optional)

    `options` is a dict with keys:

    - checkDatafileSchema (boolean; optional):
        Validate JSON datafile against schema.

    - hideTrackLegend (boolean; optional):
        Hide legends of the track. Default is False.

    - hideTrackTitle (boolean; optional):
        Hide titles of the track. Default is False.

    - maxContentZoom (number; optional):
        The maximum zoom value.

    - maxVisibleTrackNum (number; optional):
        The maximum number of visible tracks.

- primaryAxis (string; optional):
    Primary axis id: \" md\", \"tvd\", \"time\".

- readoutOptions (dict; optional)

    `readoutOptions` is a dict with keys:

    - allTracks (boolean; optional):
        Show not only visible tracks.

    - grouping (string; optional):
        How group values. \"\" | \"track\".

- selection (list of numbers; optional):
    Initial selected interval of the log data.

- template (dict; required):
    Prop containing track template data.

- viewTitle (string | dict; optional):
    Set to True for default titles or to array of individual well log
    titles.

- welllog (dict; required):
    An object from JSON file describing well log data.

- wellpick (dict; optional):
    Well picks data."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'webviz_subsurface_components'
    _type = 'WellLogViewer'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, welllog=Component.REQUIRED, template=Component.REQUIRED, colorTables=Component.REQUIRED, horizontal=Component.UNDEFINED, domain=Component.UNDEFINED, selection=Component.UNDEFINED, wellpick=Component.UNDEFINED, primaryAxis=Component.UNDEFINED, axisTitles=Component.UNDEFINED, axisMnemos=Component.UNDEFINED, maxContentZoom=Component.UNDEFINED, viewTitle=Component.UNDEFINED, options=Component.UNDEFINED, readoutOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'axisMnemos', 'axisTitles', 'colorTables', 'domain', 'horizontal', 'maxContentZoom', 'options', 'primaryAxis', 'readoutOptions', 'selection', 'template', 'viewTitle', 'welllog', 'wellpick']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisMnemos', 'axisTitles', 'colorTables', 'domain', 'horizontal', 'maxContentZoom', 'options', 'primaryAxis', 'readoutOptions', 'selection', 'template', 'viewTitle', 'welllog', 'wellpick']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'colorTables', 'template', 'welllog']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(WellLogViewer, self).__init__(**args)
