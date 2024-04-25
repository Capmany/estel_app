import math as m
import numpy as np
from typing import List

TAMANY_FONT_HEADER: int = 20
TAMANY_FONT_SECCIONS: int = 18

T_maxG = 72
T_maxP = 48

# Paràmetres dels estels
factor = 4
d_G = 50 * factor
r1_G = 22 * factor
r2_G = 68 * factor

#d_G = 72
#r1_G = 32
#r2_G = 98

d_P = 32 * factor
r1_P = 16 * factor
r2_P = 45 * factor

alfa_G = m.acos((r1_G/2)/d_G)
alfa_P = m.acos(r1_P/(2*d_P))
beta_G = (4*m.pi/3) - (2*alfa_G)


# Càlcul matrius de transformacions de coordenades
# estel gran
MT_G = []
# punta 0
a = alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_G*m.cos(np.pi/3)],[r1_G*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = -alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[0],[r2_G]])), axis=1), [[0,0,1]]), axis=0))
# punta 1
a = alfa_G-np.pi/3
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_G*m.cos(np.pi/3)],[r1_G*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = -alfa_G-np.pi/3
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r2_G*m.cos(m.pi/6)],[r2_G*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 2
a = alfa_G-2*np.pi/3
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_G],[0]])), axis=1), [[0,0,1]]), axis=0))
a = 4*np.pi/3-alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r2_G*m.cos(m.pi/6)],[-r2_G*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 3
a = alfa_G-np.pi
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_G*m.cos(np.pi/3)],[-r1_G*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = np.pi-alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[0],[-r2_G]])), axis=1), [[0,0,1]]), axis=0))
# punta 4
a = alfa_G-4*np.pi/3
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_G*m.cos(np.pi/3)],[-r1_G*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = 2*np.pi/3-alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r2_G*m.cos(m.pi/6)],[-r2_G*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 5
a = alfa_G+np.pi/3
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_G],[0]])), axis=1), [[0,0,1]]), axis=0))
a = np.pi/3-alfa_G
MT_G.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r2_G*m.cos(m.pi/6)],[r2_G*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))

# estel petit
MT_P = []
# punta 0
a = alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_P*m.cos(np.pi/3)],[r1_P*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = -alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[0],[r2_P]])), axis=1), [[0,0,1]]), axis=0))
# punta 1
a = alfa_P-np.pi/3
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_P*m.cos(np.pi/3)],[r1_P*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = -alfa_P-np.pi/3
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r2_P*m.cos(m.pi/6)],[r2_P*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 2
a = alfa_P-2*np.pi/3
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_P],[0]])), axis=1), [[0,0,1]]), axis=0))
a = 4*np.pi/3-alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r2_P*m.cos(m.pi/6)],[-r2_P*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 3
a = alfa_P-np.pi
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[r1_P*m.cos(np.pi/3)],[-r1_P*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = np.pi-alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[0],[-r2_P]])), axis=1), [[0,0,1]]), axis=0))
# punta 4
a = alfa_P-4*np.pi/3
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_P*m.cos(np.pi/3)],[-r1_P*m.sin(np.pi/3)]])), axis=1), [[0,0,1]]), axis=0))
a = 2*np.pi/3-alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r2_P*m.cos(m.pi/6)],[-r2_P*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))
# punta 5
a = alfa_P+np.pi/3
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r1_P],[0]])), axis=1), [[0,0,1]]), axis=0))
a = np.pi/3-alfa_P
MT_P.append(np.concatenate((np.concatenate((np.array([[np.cos(a), -np.sin(a)],[np.sin(a),np.cos(a)]]),np.array([[-r2_P*m.cos(m.pi/6)],[r2_P*m.sin(m.pi/6)]])), axis=1), [[0,0,1]]), axis=0))


