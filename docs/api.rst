Piano Video API
==================

Inspired by `Blender <https://blender.org>`__.

*Version 0*

**THIS API IS SUBJECT TO CHANGE WITHOUT PREVIOUS NOTICE.
The API will be considered stable when v1 is released.**

Piano Video has a Python API in the form of a module,
which allows you to extend Piano Video.

If you wish to learn how to write an add-on, please read
the `API Tutorial <api-tutorial.html>`__ page instead, which contains
step-by-step instructions for creating your first add-on.


``pv.context``
--------------

Contains the current state of the GUI, such as the current settings
and registered UI sections.


``pv.props``
------------

Property classes for display on the GUI.
When creating a property, you will be initializing
it inside of a `pv.types.PropertyGroup`_

``pv.props.Property``
^^^^^^^^^^^^^^^^^^^^^
    The base property class. You will usually NOT use this.

    When initializing **any** property, the first three arguments are:

    :param idname: The identifier name for the prop.
        Must be unique out of all props in the parent PropertyGroup.
    :param label: The text that shows up next to this prop in the GUI.
    :param description: Description of this property.
        Shows up in the tooltip.

``pv.props.BoolProp``
^^^^^^^^^^^^^^^^^^^^^
    A Boolean (true/false) property.

    ``BoolProp.__init__(self, idname, label, description, default)``
        :param default: Default boolean value.
        :type default: ``bool``

``pv.props.IntProp``
^^^^^^^^^^^^^^^^^^^^
    An integer property.

    The value is stored as a signed 64 bit integer
    in binary scene formats.

    ``IntProp.__init__(self, idname, label, description, default, min, max, step)``
        :param default: Default integer value.
        :type default: ``int``
        :param min: Optional, minimum value this prop can go to.
        :param max: Optional, maximum value this prop can go to.
        :param step: The value step size. Offset from default.

``pv.props.FloatProp``
^^^^^^^^^^^^^^^^^^^^^^
    A float property.

    The value is stored as a signed 64 bit float
    in binary scene formats.

    ``IntProp.__init__(self, idname, label, description, default, min, max, step)``
        :param default: Default float value.
        :type default: ``float``
        :param min: Optional, minimum value this prop can go to.
        :param max: Optional, maximum value this prop can go to.
        :param step: The value step size. Offset from default.

``pv.props.StringProp``
^^^^^^^^^^^^^^^^^^^^^^^
    A string property.

    ``StringProp.__init__(self, idname, label, description, default, max_len, password, subtype``
        :param default: Default string value.
        :type default: ``str``
        :param max_len: Maximum length this string can be.
        :param password: Whether to display this string as asterisks.
            This will hide sensitive information on the GUI,
            but **it's value can still be accessed through
            the API.**
        :param subtype:
            - ``""`` (empty string): no special subtype.
            - ``"FILE_PATH"``: Asks the user to choose a file.
            - ``"DIR_PATH"``: Asks the user to choose a directory.

``pv.props.EnumProp``
^^^^^^^^^^^^^^^^^^^^^
    A enumerate property. Displayed as a dropdown list.

    ``EnumProp.__init__(self, idname, label, description, default, items)``
        :param default: Default item ID (read below)
        :type default: ``str``
        :param items: This is a list that contains each dropdown "choice".
            Every choice is a tuple of three values:
            ``(item_id, item_label, item_description)``


``pv.types``
------------

Classes that can be registered onto the GUI.

``pv.types.PropertyGroup``
^^^^^^^^^^^^^^^^^^^^^^^^^^
    A collection of properties under a common group idname.

    When using, create a new class that inherits from this class.
    Define the idname and the list of props as class members.

    After you register this class, you can access the PropertyGroup
    with ``pv.context.scene.<group_idname>``.
    Access a member prop's **value**, not the prop itself,
    with ``pv.context.scene.<group_idname>.<prop_idname>``

    :type: ``type``
    :idname: ``str``, the group idname of this PropertyGroup.
    :props: ``List[pv.props.Property]``, a list of contained
        properties.

``pv.types.Scene``
^^^^^^^^^^^^^^^^^^
    The scene class, which contains all settings for a project.

    :type: ``type``
    :pgroups: ``List[pv.types.PropertyGroup]``


``pv.utils``
------------

Utilities for PV, such as registering and unregistering a class.
