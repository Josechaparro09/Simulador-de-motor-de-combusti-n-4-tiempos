import math
import matplotlib.pyplot as plt
from tkinter import * 

def motor_cinematica(Bore, stroke, con_rod, cr, start_crank, end_crank):

	#Parámetros geométricos

	a = stroke/2		# Radio del muñón del cigüeñal
	R = con_rod/a 		# Constante

	#Cálculo de volumen

	V_s = (math.pi/4)*pow(Bore,2)*stroke		# volumen barrido

	V_c = V_s/(cr-1)	# volumen de liquidacion


	sc = math.radians(start_crank)
	ec = math.radians(end_crank)

	num_values = 50

	dtheta = (ec-sc)/(num_values-1)
	V = []

	for i in range(0,num_values):
		
		theta = sc + i*dtheta

		term1 = 0.5*(cr-1)
		term2 = R+1-math.cos(theta)
		term3 = pow(R,2)-pow(math.sin(theta),2)
		term3 = pow(term3,0.5)

		V.append ((1+term1*(term2-term3))*V_c)
	return V


def generar(_p1,_t1,_gm,_t3,_br,_st,_crod,_cr):
	
    # parámetros iniciales
    P1 =_p1	 # presion en estado-1
    t1 = _t1	 # temperatura en estado-1
    gamma = _gm
    t3 = _t3
        
    #parametros geometricos
    Bore = _br
    stroke = _st
    con_rod = _crod
    cr = _cr

    #calculo del volumen
    V_s = (math.pi/4)*pow(Bore,2)*stroke		# swept volume
    V_c = V_s/(cr-1)	# clearance volume
    V1 = V_c + V_s	
        
    # el punto de estado 2
    V2 = V_c

    # P2V2^gamma = P1V1^gamma
    P2 = P1*pow(V1,gamma)/pow(V2,gamma)

    # P2V2/t2 = P1V1/t1 | rhs = P1V1/t1 | P2V2/t2 = rhs | t2 = P2V2/rhs

    rhs = P1*V1/t1
    t2 = P2*V2/rhs
    V_compression = motor_cinematica(Bore,stroke,con_rod,cr,180,0)
    constant = P1*pow(V1,gamma)
    P_compression = []

    for V in V_compression:
        P_compression.append(constant/pow(V,gamma))

    # el punto de estado 3
    V3 = V2
    # P3V3/t3 = P2V2/t2 | rhs = P2V2/t2 | P2 = rhs*t3/V3
    rhs = P2*V2/t2
    P3 = rhs*t3/V3

    V_expansion = motor_cinematica(Bore,stroke,con_rod,cr,0,180)
    constant = P3*pow(V3,gamma)
    P_expansion = []

    for V in V_expansion:
        P_expansion.append(constant/pow(V,gamma))

    # el punto de estado 4
    V4 = V1
    # P4V4^gamma=P3V3^gamma
    P4 = P3*pow(V3,gamma)/pow(V4,gamma)
    # P4V4/t4 = rhs
    t4 = P4*V4/rhs

    #Rendimiento térmico del ciclo Otto
    #eficiencia termica = ther_eff
    Ther_eff = (1 - ((t4-t1)/(t3-t2)))*100
    print(Ther_eff)
    #UI

    #trazado del diagrama P_V desde el ciclo otto

    plt.grid()
    plt.plot([V2,V3],[P2,P3])
    plt.plot(V_compression,P_compression)
    plt.plot(V_expansion,P_expansion)
    plt.plot([V4,V1],[P4,P1])
    plt.xlabel('Volumen')
    plt.ylabel('presion')
    plt.title('Motor de combustion 4 tiempos')
    plt.show()


root = Tk()
parametros_frame = Frame(root)
parametros_frame.pack()
l1 = Label(parametros_frame, text="Presión en estado 1:").grid(row=0, column=0)
P1_entry = Entry(parametros_frame)
P1_entry.grid(row=0, column=1)

l2 = Label(parametros_frame, text="Temperatura en estado 1:").grid(row=1, column=0)
t1_entry = Entry(parametros_frame)
t1_entry.grid(row=1, column=1)

l3 =Label(parametros_frame, text="Relación de especificación de calor:").grid(row=2, column=0)
gamma_entry = Entry(parametros_frame)
gamma_entry.grid(row=2, column=1)

l4 =Label(parametros_frame, text="Temperatura en estado 3").grid(row=3, column=0)
t3_entry = Entry(parametros_frame)
t3_entry.grid(row=3, column=1)

l1 =Label(parametros_frame, text="Diámetro del cilindro):").grid(row=4, column=0)
Bore_entry = Entry(parametros_frame)
Bore_entry.grid(row=4, column=1)

l5 =Label(parametros_frame, text="Longitud de carrera):").grid(row=5, column=0)
stroke_entry = Entry(parametros_frame)
stroke_entry.grid(row=5, column=1)

l6 =Label(parametros_frame, text="Longitud de la biela):").grid(row=6, column=0)
con_rod_entry = Entry(parametros_frame)
con_rod_entry.grid(row=6, column=1)

l7 =Label(parametros_frame, text="Relacion de compresion").grid(row=7, column=0)
cr_entry = Entry(parametros_frame)
cr_entry.grid(row=7, column=1)
gif = PhotoImage(file="Motor.gif")

gif_label = Label(root, image=gif)
gif_label.pack()

def getDatos():
    P1 = float(P1_entry.get())
    t1 = float(t1_entry.get())
    gamma = float(gamma_entry.get())
    t3 = float(t3_entry.get())
    Bore = float(Bore_entry.get())
    stroke = float(stroke_entry.get())
    con_rod = float(con_rod_entry.get())
    cr = 12
    generar(P1,t1,gamma,t3,Bore,stroke,con_rod,cr)

obtener_valores_button = Button(root, text="Calcular", command=lambda:getDatos())
obtener_valores_button.pack()


mainloop()

	
