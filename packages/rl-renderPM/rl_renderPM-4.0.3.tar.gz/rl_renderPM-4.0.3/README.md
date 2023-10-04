``rl_renderPM`` is a package containing the ReportLab accelerator module

``_renderPM``

which can be used to speedup the ``reportlab.graphics.renderPM`` functions.

The python bitmap render module ``reportlab.graphics.renderPM`` can either use ``rlPyCairo``, ``pycairo`` and ``freetype-py``
or ``rl_renderPM`` + built in ``freetype`` libraries.

The choice is made by overriding the ``reportlab.rl_settings`` module value ``_renderPMBackend``
using one of the settings files ``reportlab/local_reportlab_settings.py``, ``reportlab_settings.py`` or  ``~/.reportlab_settings``, which are searched for in that order.

The default value of ``renderPMBackend`` is ``'rlPyCairo'``, but it can be set to ``'_renderPM'`` to use this extension
which is based on an older library ``libart_lgpl``. 
