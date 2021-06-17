API Tutorial
============

A basic understanding of Python is required.


Installation
------------

The module is provided on PyPI, and can be installed with Pip.
However, you do NOT need to install the module, as it is contained
in every release.

``pip install piano-video``

.. code-block:: python

    import pv
    print(pv.__version__)


Piano Video Structure
---------------------

The whole Piano Video program is made up of three parts:

1. The GUI: This is the part that opens the display and shows
everything to you on a screen.

2. The API: This is the Python module that allows you to easily
customize and add features to Piano Video.

3. The Add-ons: These are scripts that use the API module.
The add-ons give Piano Video all of it's functionality, including
core features like MIDI parsing.

Piano Video has built-in add-ons, such as MIDI parsing and
rendering the blocks. These add-ons are enough for general
use. If you would like to customize the program, such as
creating your own blocks, you would write your own add-on
in Python using API.


Writing an Add-on
-----------------

Now, let's go through the process of writing an add-on, step-by-step.

Setting Up Your Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need a text editor to write and save your file.
Open a new file, and save it as a ``.py`` file.
Make sure you do not put any spaces in the file name.

Part 1: Operators
^^^^^^^^^^^^^^^^^

An operator can be thought of as a function.
You can display operators on the UI, and they will show up as a button.
When the user presses the button, a block of code you define will
be run.

----

To write an operator, we need to define a new class which extends off
of a predefined class in the ``pv`` module:

.. code-block:: python

    import pv


    class TUTORIAL_OT_MyOperator(pv.types.Operator):
        pass


    def register():
        pass

    def unregister():
        pass

When writing an add-on for Piano Video, we recommend you name
all class names in the format ``GROUP_TYPE_Name``.
In this case, the group is ``TUTORIAL``, the type is ``OT``
(stands for Operator Type), and the name is ``MyOperator``.

The ``register`` and ``unregister`` functions will be run
by the GUI. These functions are where we tell Piano Video that
we are adding our class to the GUI. We will fill them out in a moment.

----

Next, we need to define a few parameters for the operator:

.. code-block:: python

    # This code block and many others below leaves
    # out sections for conciseness, but you should
    # still have them.

    class TUTORIAL_OT_MyOperator(pv.types.Operator):
        idname = "tutorial.my_operator"
        name = "My Operator"
        description = "A test operator."

Let's look at what each variable means:

- ``idname`` is the unique ID of the operator. We can
  access the operator by it's idname. More info about this later.

- ``name`` is the text that is shown when you display the operator
  on the GUI.

- ``description`` is a short message that explains what this operator
  does.

----

Next, let's define the code that will be run when a user clicks on the operator.

.. code-block:: python

    class TUTORIAL_OT_MyOperator(pv.types.Operator):
        ...

        def execute(self):
            print("Hello world!")
            return "FINISHED"

The ``execute`` method will be run when the operator is clicked.
It **must** return a string, and we recommend ``"FINISHED"`` for
a successful run, and ``"CANCELLED"`` for an incomplete run.

You may be wondering how any operator will be useful, if it can only return
a string. The answer is operators are designed to modify the scene while running,
instead of returning a result.

If you need to use the return value, you should use ``pv.types.Function``
instead. **TODO write docs**

----

Last, let's write the register and unregister functions.

.. code-block:: python

    class TUTORIAL_OT_MyOperator(pv.types.Operator):
        ...


    classes = (
        TUTORIAL_OT_MyOperator,
    )

    def register():
        for cls in classes:
            pv.utils.register_class(cls)

    def unregister():
        for cls in classes:
            pv.utils.unregister_class(cls)

We use ``pv.utils.register_class`` to add the class onto the GUI,
and ``pv.utils.unregister_class`` to remove it from the GUI.
If you wish to write more operators, you would define more classes
and add them to the ``classes`` tuple.

**Debug Tip**: If you are getting an error message similar to this,

``TypeError: 'type' object is not iterable``

make sure you add the comma after your class name:

.. code-block:: python

    classes = (
        TUTORIAL_OT_MyOperator,
    )

----

Now, let's install the add-on into Piano video!
Before we can do that, there are a few more things to do:

.. code-block:: python

    pv_info = {
        "name": "My Test Add-on",
        "description": "A test",
        "author": "<your name>",
    }

    import pv

    ...

We need to add a ``pv_info`` variable to the top. This is a dictionary
that carries information about the add-on. The add-on can only be installed
if it has a pv_info variable.

Now we are ready to install the add-on.
We do this with a shell command:

.. code-block:: bash

    >>> pv addons inst
    Enter file path: file.py

Make sure you replace ``file.py`` with your actual file name.

Now, if you list the add-ons, you should see your add-on installed!

``pv addons list``

Currently, our add-on doesn't change the UI in any noticable way.
We are going to go over modifying the UI in the next section.

Part 2: User Interface
^^^^^^^^^^^^^^^^^^^^^^

We will use the operator class you defined in this section, so make
sure you don't delete it!

In this section, we will be looking at how to extend the Properties
section of the UI:

.. image:: https://raw.githubusercontent.com/HuangPatrick16777216/piano_video/main/docs/images/properties.png
    :width: 200

----

First, let's look at UI Sections. They are the tabs on the left side.

.. image:: https://raw.githubusercontent.com/HuangPatrick16777216/piano_video/main/docs/images/ui_sections.png
    :width: 50

Like the operators, we will define a new class that extends off of a
predefined UI Section class:

.. code-block:: python

    class TUTORIAL_UT_Section(pv.types.UISection):
        idname = "tutorial"
        label = "Tutorial"
        description = "A UI section"

Let's look at what each parameter means:

- ``idname``: A unique ID for this section.
- ``label``: This is the "name" of the panel that the user will see.
- ``description``: A longer description of what the panel does.

Now, we can also add this class to the classes tuple:

.. code-block:: python

    classes = (
        TUTORIAL_OT_MyOperator,
        TUTORIAL_UT_Section,
    )

To install this add-on, we first need to uninstall the other one
(remember, we installed it in the Operator section). Uninstalling
and the installing can be tedious, so we can fix that problem by
making a link install. Piano Video will read from the path we give
it instead of copying the file.

To make a link install, first we need to uninstall the previous one.
Type ``pv addons list`` and locate which add-on is the test one.

.. image:: https://raw.githubusercontent.com/HuangPatrick16777216/piano_video/main/docs/images/addons.png
    :width: 250

To uninstall it, type ``pv addons rm <num>``, where num is the add-on
number.

To make a link install, type ``pv addons link`` and enter your file path.

After linking the add-on, you can start the GUI with ``pv``. You should
see a blank section, which was added by the add-on!

.. image:: https://raw.githubusercontent.com/HuangPatrick16777216/piano_video/main/docs/images/blank_section.png

The good thing about linking an add-on is when we make a change to the file,
we don't have to re-install the add-on!
