import reflex as rx
from estel_app.utils_dibuix.constants import *
from PIL import Image, ImageDraw
from typing import List, Any

from estel_app.pages.llista_posicions import State_LlistaPos

# clase Estat
class EstatDibuixarPosicio(State_LlistaPos):
    coordinates: tuple[int, int] = (0, 0)
    def update_coordinates(self, clientX, clientY):
        self.coordinates = (clientX, clientY)
        print(clientX, clientY)

    # Inicialment tenim l'estel gran triat
    estel: str = "gran"
    # Inicialment no hi ha cap punta seleccionada
    puntesTriades: List[bool] = [True,True,True,True,True,True]
    # COLOR per la posició triada
    color: str = "#00ff00"
    # TRAM a iluminar (l'origen és 1)
    tram = [10,140]
    # REPETIR tram
    flagRepetir: bool = False
    # ESPAI sense iluminar entre repeticions del tram
    espai = 10

    def setTram(self, value):
        if value[0]!= self.tram[0]: self.tram[0]=value[0]
        if value[1]!= self.tram[1]: self.tram[1]=value[1]


    def setEspai(self, value):
        self.espai=value[0]

    @rx.var
    def tram_complert(self) -> list[int]:
        # Retorna el tram complert depenent de l'estel seleccionat
        if self.tram[1] > self.t_max*2: self.tram[1]=self.t_max*2
        return [1,self.t_max * 2]

    # Amplada del cuadrat que inclou l'estel
    # usem les dimensions de l'estel gran
    w = r2_G * 2
    imatge = Image.new("RGBA", (w, w), (255,0,0,0))

    def triarPunta(self, punta:int):
        self.puntesTriades[punta] = not self.puntesTriades[punta]

    def triarRepetir(self):
        self.flagRepetir = not self.flagRepetir

    @rx.var
    def t_max(self) -> int:
        if self.estel == "gran":
            return T_maxG
        return T_maxP
    
    @rx.var
    def dibuix_estel(self) -> Image:
        return self.imatge
        gruix = 5
        c = self.w/2
        # Calcular trams a iluminar
        trams = self.calcularIntervals()

        draw = ImageDraw.Draw(self.imatge)
        draw.rectangle([0, 0, self.w, self.w], fill=(0,0,0,0))
        for punta in range(0,6):
            if self.puntesTriades[punta]:
                # Hem de dibuixar la punta
                for brac in range(0,2):
                    for p in trams[brac]:
                        p1 = MT_G[2*punta+brac].dot([p[0],0,1])
                        p2 = MT_G[2*punta+brac].dot([p[1],0,1])
                        draw.line([(c+p1[0],c-p1[1]),(c+p2[0],c-p2[1])], fill=self.color, width= gruix)
        return self.imatge

    # Per fer click a una punta per seleccionar-la o no
    def triarPuntaG(self, punta: int):
        self.puntesTriadesG[punta] = not self.puntesTriadesG[punta]

    # Per pasar interval a llums reals
    #@rx.var
    def calcularIntervals(self) -> tuple[List,List]:
        t1=self.tram[0]
        t2=self.tram[1]
        b= self.espai if self.flagRepetir else 999

        tmax=self.t_max
        brac0=[]
        brac1=[]
        #return ([[25.0, 197]],[[0.0, 186]])
        i=t1
        iant= i
        j= t2 if t2<tmax else tmax
        # factor pel canvi d'escala del dibuix
        f = d_G / self.t_max # s'usen les dimensions de l'estel gran
        while i<=tmax :
            brac0.append([(i-1)*f,(j-1)*f])
            iant = i
            i =j+1 if j<t2 else j+b+1 
            j= i+t2-t1
            j= j if j<tmax else tmax
        # Posem a nou origen del braç
        if t1>tmax:
            # l'interval comença en el segon braç
            i = t1-tmax
            j = i + t2-t1
        else: 
            if t2-t1 > tmax-iant :
                # No he fet tot l'interval
                i = 1
                j = (t2-t1)-(tmax-iant)
            else :
                i = b - (tmax - (iant+(t2-t1))) + 1
                j = i + t2-t1
        j= j if j<tmax else tmax
        while i<=tmax :
            brac1.append([(i-1)*f,(j-1)*f])
            i= j+b+1
            j= i+t2-t1
            j= j if j<tmax else tmax
        #print(brac0)
        #print(brac1)
        return (brac0, brac1)


# Per capturar les coordenades al clicar damunt l'estel
#custom_event_chain = rx.EventChain(
#    events=[EstatDibuixarPosicio.update_coordinates("${ev.nativeEvent.offsetX}", "${ev.nativeEvent.offsetY}")]
#)
#custom_handler = rx.vars.BaseVar(
#    _var_name=f"ev => {rx.utils.format.format_event_chain(custom_event_chain)}",
#    _var_type=rx.EventChain,
#)



# Per seleccionar el color de la posició a iluminar
class ColorPicker(rx.Component):
    library = "react-colorful"
    tag = "HexColorPicker"
    color: rx.Var[str]
    def get_event_triggers(self) -> dict[str, any]:
        return {
            **super().get_event_triggers(),
            "on_change": lambda e0: [e0],
        }

color_picker = ColorPicker.create

@rx.page(route="/llumsEncesos", title="llums encesos")
def llumsEncesos() -> rx.Component:
    p: int = 40 # % en tamany de l'estel
    return rx.vstack(

            rx.center(
                rx.vstack(
                    #rx.heading("Puntes a iluminar:", color="white", padding_top="60px", font_size=TAMANY_FONT_SECCIONS),
                    rx.radio(["gran", "petita"], direction="row", spacing="8", size="3", value=EstatDibuixarPosicio.estel,
                            on_change=EstatDibuixarPosicio.set_estel, padding_top="0px", padding_bottom="10px"),
                    rx.vstack(
                        rx.flex(
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[5], on_change=EstatDibuixarPosicio.triarPunta(5), border="2px solid #ffffff", color_scheme="bronze"),
                            rx.spacer(),
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[0], on_change=EstatDibuixarPosicio.triarPunta(0), border="2px solid #ffffff", color_scheme="bronze"),
                            rx.spacer(),
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[1], on_change=EstatDibuixarPosicio.triarPunta(1), border="2px solid #ffffff", color_scheme="bronze"),
                            width= "100%",
                            padding_right= "30px",
                            padding_left= "30px",
                        ),
                        rx.image(src=EstatDibuixarPosicio.dibuix_estel, width="500px", height="auto"),
                        rx.flex(
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[4], on_change=EstatDibuixarPosicio.triarPunta(4), border="2px solid #ffffff", color_scheme="bronze"),
                            rx.spacer(),
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[3], on_change=EstatDibuixarPosicio.triarPunta(3), border="2px solid #ffffff", color_scheme="bronze"),
                            rx.spacer(),
                            rx.checkbox(checked=EstatDibuixarPosicio.puntesTriades[2], on_change=EstatDibuixarPosicio.triarPunta(2), border="2px solid #ffffff", color_scheme="bronze"),
                            width= "100%",
                            padding_right= "30px",
                            padding_left= "30px",
                            padding_bottom= "20px"
                        ),
                    ),
                    # COLOR
                    rx.hstack(
                        rx.heading("Color:", color="white", font_size=TAMANY_FONT_SECCIONS),
                        color_picker(color=EstatDibuixarPosicio.color, on_change=EstatDibuixarPosicio.set_color),
                        rx.box(width = "70px", height="70px", border_radius="10px", background_color=EstatDibuixarPosicio.color)
                    ),
                    # TRAM
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Tram:", color="white", font_size=TAMANY_FONT_SECCIONS),
                            rx.text("(el tram complert és tota una punta)", font_size=TAMANY_FONT_SECCIONS/1.2),
                            align="baseline",
                            color="white"
                        ),
                        rx.heading(f"{EstatDibuixarPosicio.tram[0]}-{EstatDibuixarPosicio.tram[1]}", size="5", color="white"),
                        rx.slider(min=1, max=EstatDibuixarPosicio.t_max*2, step=1,
                            default_value=EstatDibuixarPosicio.tram,
                            on_change=EstatDibuixarPosicio.setTram),
                            #on_value_commit=EstatDibuixarPosicio.set_tram),
                    ),
                    # REPETIR
                    rx.vstack(
                        rx.vstack(
                            rx.checkbox("Repetir tram", checked=EstatDibuixarPosicio.flagRepetir, on_change=EstatDibuixarPosicio.triarRepetir()),
                            rx.cond(EstatDibuixarPosicio.flagRepetir,
                                    rx.hstack(
                                        rx.heading(f"{EstatDibuixarPosicio.espai}", size="5"),
                                        rx.slider(min=1, max=EstatDibuixarPosicio.t_max, step=1,
                                                default_value=[EstatDibuixarPosicio.espai],
                                                on_change=EstatDibuixarPosicio.setEspai, width="200px"),
                                        width="300px",
                                        align="baseline",
                                        padding_top="20px"
                                    ),
                                    rx.text("")),
                            width="300px",
                            padding="20px",
                            color="white"
                        ),
                    ),


                    rx.hstack(
                        #rx.link(rx.button("tornar"), href="/"), 
                        rx.button("guardar"),
                        padding_top= "40px",
                        padding_bottom= "100px"
                    ),

                    align="center",
                    spacing="5",
                    font_size="1em"
                ),
            ),
            align="center",
            spacing="5",
            font_size="1em",
            background_color= "#000000"
        )
    

