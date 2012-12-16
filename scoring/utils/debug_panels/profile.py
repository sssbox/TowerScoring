from debug_toolbar.panels import DebugPanel
from django.template.loader import render_to_string
import sys, tempfile, pstats
from cStringIO import StringIO
import logging
try:
    import cProfile as profile
except:
    import profile

class ProfileDebugPanel(DebugPanel):
    has_content = True
    name = 'Profile'

    def __init__(self, *args, **kwargs):
        super(ProfileDebugPanel, self).__init__(*args, **kwargs)
        self.profiler = None
        self.view_func = None
        self.output = None

    def title(self):
        return 'Profile'

    def url(self):
        return ''

    def nav_title(self):
        """Title showing in toolbar"""
        return 'Profiling'

    def nav_subtitle(self):
        """Subtitle showing until title in toolbar"""
        return " "

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.REQUEST.has_key('prof'):
            logging.debug('Profiling view')
            self.view_func = view_func
            self.profiler = profile.Profile()
            return self.profiler.runcall(view_func, request, *view_args, **view_kwargs)

    def process_response(self, request, response):
        if request.REQUEST.has_key('prof') and self.view_func is None:
            logging.debug('Profiler disabled - No view function to profile')
            self.output = '<p>This view cannot be profiled.</p>'

    def content(self):
        if self.profiler is not None:
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out

            self.tmpfile = tempfile.mktemp()
            self.profiler.dump_stats(self.tmpfile)
            stats = pstats.Stats(self.tmpfile)

            stats.sort_stats('time')
            stats.print_stats(.1)

            sys.stdout = old_stdout
            self.output = '<pre>%s</pre>' % out.getvalue()
        return render_to_string('debug_toolbar/panels/profile.html', {'content': self.output})
