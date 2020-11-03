class shader:

    def __shadowed(self,object,I,S,objectList):
        

        M = object.getT()
        E = 0.001
        I = M*(I+S.scalarMultiply(E))
        S = M*S
        
        

        for shadowObject in objectList:
            Minv = shadowObject.getTinv()
            Iinv = Minv*I
            Sinv = Minv*S

            Sinv.normalize()

            if shadowObject.intersection(Iinv,Sinv) != -1.0:
                return True

        return False

    def __init__(self,intersection,direction,camera,objectList,light):

        
        self.__color = (0,0,0)

        k = intersection[0]
        tnot = intersection[1]
        object = objectList[k]
        Minv = object.getTinv()

        Ts = Minv*light.getPosition()
        Te = Minv*camera.getE()
        Td = Minv*direction

        I = Te+(Td.scalarMultiply(tnot))

        S = (Ts.removeRow(3) - I.removeRow(3)).normalize().insertRow(3, 0.0)
        N = object.normalVector(I)
        R = S.scalarMultiply(-1.0) + N.scalarMultiply(2.0*(S.dotProduct(N)))
        V = (Te.removeRow(3)-I.removeRow(3)).normalize().insertRow(3, 0.0)

        #compute local elements of shading
        Id = (N.transpose()*S).get(0,0)
        Is = (R.transpose()*V).get(0,0)
        if Id < 0.0: Id = 0.0
        if Is < 0.0: Is = 0.0
        r = object.getReflectance()
        c = object.getColor()
        Li = light.getIntensity()

        if self.__shadowed(object, I, S, objectList):
            f = r[0]

        else:
            f = r[0] + r[1]*Id + r[2]*Is**r[3]

        self.__color = ((int(c[0]*Li[0]*f), int(c[1]*Li[1]*f), int(c[2]*Li[2]*f)))

        

    def getShade(self):
        return self.__color