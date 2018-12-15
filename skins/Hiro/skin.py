
from skins import cpu_x, mem_x

class SkinDrawing:

    #!editable sets
    _font = "Zero Twos 5" # font name
    _time = "" # %I %H 12/24 hour, %M minute, %S seconds
    _date = "" # %a %A %d day, %b %B %m month, %y %Y year
    _iface = "ppp0" # eth0, wlan0, ppp0
    _bgc = 0.14, 0.14, 0.14, 1.0 # background color
    _fgc = 0.64, 0.8, 1.0, 1.0  # text color

    def __init__(self, window):
        self.__window = window
        self.__window.height = 128
            
    def redraw_back(self, ctx):
        ctx.set_source_rgba(*self._bgc)
        self.__window.draw_rounded_rectangle(ctx, 1, 0,
            self.__window.width -2, self.__window.height -2, 2, True)

    def redraw_fore(self, ctx):
        x, y = 0, 100
        w, h = self.__window.width, 100

        _txt = self.__window.dtime.strftime("%A %d %B")
        ctx.set_source_rgba(0.7, 0.7, 0.7, 1.0)
        self.__window.draw_text(ctx, self._font, _txt, x, y, w, 0, 1)

        _cx, _mx = cpu_x(), mem_x()
        _txt = "cpu %s%% : mem %s%%" % (_cx, _mx)
        ctx.set_source_rgba(*self._fgc)
        self.__window.draw_text(ctx, self._font, _txt, x, y +9, w, 0, 1)

        x, y = 6, 120
        if _cx < 2 or _cx > 100: _cx = 2
        ctx.set_source_rgba(0.4, 0.4, 0.4, 1.0) #!empty
        self.__window.draw_line(ctx, x, y, w-(x*2), 0, 1)
        ctx.set_source_rgba(*self._fgc) #!fill
        self.__window.draw_line(ctx, x, y, int(_cx *(w-(x*2)) /100), 0, 1)
        #self.__window.draw.draw_rounded_rectangle(ctx, x=_hp, y=_py -1,
        #     w=self.width-(_hp*2), h=2, r=1)
