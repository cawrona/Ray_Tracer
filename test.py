def __shadowed(self,object,I,S,objectList):
        """
        return: True if the ray is shadowed, false otherwise       
        """
        M = object.getT()
        # Convert I and S vector to world coordinates and move I off
        # the surface so it will not intersect the object it is on
        I = M * (I + S.scalarMultiply(0.001))
        S = M * S

        for shadowObject in objectList:
            # Convert vectors from world coordinates to the new object's coordinates
            Minv = shadowObject.getTinv()
            Iinv = Minv * I
            Sinv = Minv * S
            # If this object is between the light source and the object then it is shadowed
            if shadowObject.intersection(Iinv, Sinv) != -1.0:
                return True

        return False
