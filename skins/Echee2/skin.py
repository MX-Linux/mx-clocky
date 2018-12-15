
import math
from skins import cpu_x, mem_x

class SkinDrawing:

    #!editable sets
    cpu_start = -90 #!46
    cpu_end = 224
    mem_start = 30
    mem_end = 180
    cpu_dial_x = 41
    cpu_dial_y = 33 +88 #was:33 +100 /100-x=>100
    mem_dial_x = 72 #!75
    mem_dial_y = 13 +90 #was:13 +100 /100-x=>100
    skin_xy = 0, 68 #was:0, 80 /80-h=x

    def __init__(self, window):
        self.__window = window
        self.__window.height = 170

    def redraw_back(self, ctx):
        ctx.save()
        ctx.translate(*self.skin_xy)
        self.__window.render(ctx, 'cpumeter')
        ctx.restore()

    def redraw_fore(self, ctx):
        #!get radians
        _cpu = cpu_x()
        _cpu_start = self.cpu_start *(math.pi /180)
        _cpu_end = self.cpu_end *(math.pi /180)        
        #!org /100
        _cpu_r = ((_cpu_end -_cpu_start)/50 *_cpu) +_cpu_start -math.pi 
        _mem = mem_x()
        _mem_start = self.mem_start *(math.pi /180)
        _mem_end = self.mem_end *(math.pi /180)
        _mem_r = ((_mem_end-_mem_start) /100 *_mem) +_mem_start -math.pi
        #!draw context
        ctx.save()
        ctx.translate(self.cpu_dial_x, self.cpu_dial_y)
        ctx.scale(0.8, 0.8)
        ctx.rotate(_cpu_r)
        self.__window.render(ctx, 'clock-hour-hand')
        ctx.restore()
        ctx.save()
        ctx.translate(self.mem_dial_x, self.mem_dial_y)
        ctx.scale(0.4, 0.4)
        ctx.rotate(_mem_r) 
        self.__window.render(ctx, 'clock-hour-hand')
        ctx.restore()
        ctx.save()
        ctx.translate(*self.skin_xy)
        self.__window.render(ctx, 'cpumeter-dot')
        ctx.restore()
