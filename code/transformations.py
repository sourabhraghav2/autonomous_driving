import  math

class TransformCor:
    def __init__(self,win_par,translation=0,invert=False,rotation=0):
        self.translation=translation
        self.rotation=rotation
        self.invert=invert
        self.window_height=win_par[0]
        self.window_width = win_par[1]

    def transform(self, input):
        result=input
        if self.invert:
            # print('invert: x=',result[0] ,'  y=',result[1])
            result = result[0], self.window_height - result[1]
        if self.translation:
            result = result[0] + self.translation, result[1] + self.translation
            # print('translation')

            # print('inverted')
        # if self.rotation!=0:
            #Not working as of Now
            #result=result[0]* math.cos(dtr(self.rotation))- result[1]*math.sin(dtr(self.rotation)),result[1] * math.cos(dtr(self.rotation)) + result[0] * math.sin(dtr(self.rotation))
            # print('rotated')
        return result

