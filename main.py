
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

from Poly_package import Poly_package

import numpy as np








class MatplotlibInterface:

    def __init__(self):
        # ============================================================
        # Main window
        # ============================================================
        self.fig = plt.figure(figsize=(14, 7))

        try:
            self.fig.canvas.manager.set_window_title(
                "Matplotlib Interface"
            )
        except AttributeError:
            pass

        # ============================================================
        # Two plots
        # ============================================================
        self.ax1 = self.fig.add_axes([0.02, 0.30, 0.31, 0.62])
        self.ax2 = self.fig.add_axes([0.34, 0.30, 0.31, 0.62])

        self.configure_plot(self.ax1, "Revêtement/plan pré-image")
        self.configure_plot(self.ax2, "Plan initial")

        self.E_highlight =self.ax1.scatter([],[],color ='red',s=80)
        self.E_scatter = self.ax1.scatter([],[],color ='blue',label="Z(P-x0)")
        self.x0_scatter= self.ax2.scatter([],[],color ='blue',label="x0")
        self.V_scatter =self.ax2.scatter([],[],color="black",label="valeurs singulières")

        self.path_line,=self.ax2.plot([],[],color ='lightcoral',label ='chemin')
        self.releve_line, = self.ax1.plot([],[],color ='lightcoral',label ='relevé')
        self.path_highlight,=self.ax2.plot([],[],color ='green')
        self.releve_highlight, = self.ax1.plot([],[],color ='green')

        self.ax1.legend(loc="upper right")
        self.ax2.legend(loc="upper right")

        # ============================================================
        # Section 1
        # ============================================================
        self.section1_position = [0.69, 0.52, 0.28, 0.40]

        self.section1_panel = self.fig.add_axes(
            self.section1_position
        )

        self.section1_panel.set_xticks([])
        self.section1_panel.set_yticks([])

        self.section1_panel.text(
            0.5,
            0.88,
            "Programme de visite",
            ha="center",
            va="center",
            fontsize=16,
        )

        self.section1_panel.text(
            0.05,
            0.68,
            "Valeurs singulières",
            ha="left",
            va="center",
            fontsize=13,
        )

        self.section1_panel.text(
            0.05,
            0.30,
            "Nombre de tours",
            ha="left",
            va="center",
            fontsize=13,
        )

        initial_values = [0,0,0,0]

        self.section1_row1 = []
        self.section1_row2 = []

        counter_start_x = 0.755
        counter_spacing = 0.051

        for index, value in enumerate(initial_values):
            counter_x = counter_start_x + index * counter_spacing

            row1_counter = self.create_small_counter(
                x=counter_x,
                y=0.685,
                initial_value=value, is_bounded=True
            )

            row2_counter = self.create_small_counter(
                x=counter_x,
                y=0.550,
                
                initial_value=value,is_bounded=False
            )

            self.section1_row1.append(row1_counter)
            self.section1_row2.append(row2_counter)

        # ============================================================
        # Section 2
        #
        # Its horizontal centre is exactly the same as Section 1.
        # ============================================================
        section1_x, _, section1_width, _ = self.section1_position

        section2_width = 0.18
        section2_x = (
            section1_x
            + section1_width / 2
            - section2_width / 2
        )

        self.section2 = self.create_large_counter(
            position=[section2_x, 0.31, section2_width, 0.16],
            title="Point de départ",
            initial_value=0,
        )

        # ============================================================
        # Bottom-left mutable mathematical text display
        # ============================================================
        left_display_axes = self.fig.add_axes(
            [0.01, 0.08, 0.45, 0.15]
        )

        left_display_axes.set_xticks([])
        left_display_axes.set_yticks([])

        self.left_display_text = left_display_axes.text(
            0.5,
            0.5,
            r"$P=X^4$",
            ha="center",
            va="center",
            fontsize=20,
            transform=left_display_axes.transAxes,
        )

        # ============================================================
        # Bottom buttons
        # ============================================================
        button1_axes = self.fig.add_axes(
            [0.49, 0.185, 0.15, 0.08]
        )

        button2_axes = self.fig.add_axes(
            [0.49, 0.100, 0.15, 0.08]
        )

        self.button1 = Button(
            button1_axes,
            "Changer de polynome",
        )

        self.button2 = Button(
            button2_axes,
            "Animer",
        )

        self.button1.on_clicked(self.button1_clicked)
        self.button2.on_clicked(self.button2_clicked)

        # ============================================================
        # Bottom-right mutable mathematical text display
        # ============================================================
        right_display_axes = self.fig.add_axes(
            [0.68, 0.08, 0.29, 0.17]
        )

        right_display_axes.set_xticks([])
        right_display_axes.set_yticks([])

        self.right_display_text = right_display_axes.text(
            0.5,
            0.5,
            r"$\sigma=(1\,2\,3)(4\,5)$",
            ha="center",
            va="center",
            fontsize=20,
            transform=right_display_axes.transAxes,
        )
        self.iP=0
        self.poly_pack=Poly_package(0)
        self.config_poly()

        self.animation =None

    # ================================================================
    # Plot configuration
    # ================================================================
    @staticmethod
    def configure_plot(ax, title):
        ax.set_title(
            title,
            fontsize=16,
            pad=12,
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        ax.set_aspect(
            "equal",
            adjustable="box",
        )

        ax.set_xticks([])
        ax.set_yticks([])
    @staticmethod
    def scale_axis(ax,R):
        
        R= 1.25*R #add padding

        ax.set_xlim(-R, R)
        ax.set_ylim(-R, R)

        ax.set_box_aspect(1)
        ax.set_aspect("equal", adjustable="box")    
    @staticmethod
    def autoscale_axis(ax, *point_arrays):
        non_empty_arrays = [
            points
            for points in point_arrays
            if len(points) > 0
        ]

        if not non_empty_arrays:
            return

        points = np.vstack(non_empty_arrays)

        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)

        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2

        x_span = xmax - xmin
        y_span = ymax - ymin

        # Use the same span horizontally and vertically
        span = max(x_span, y_span, 1.0)

        padding = 0.15 * span
        half_width = span / 2 + padding

        ax.set_xlim(
            x_center - half_width,
            x_center + half_width,
        )

        ax.set_ylim(
            y_center - half_width,
            y_center + half_width,
        )

        ax.set_box_aspect(1)
        ax.set_aspect("equal", adjustable="box")
    def set_points(self,E,V,x0):

        E_xy = np.asarray(
            [(z.real, z.imag) for z in E],
            dtype=float,
        ).reshape(-1, 2)

        V_xy = np.asarray(
            [(z.real, z.imag) for z in V],
            dtype=float,
        ).reshape(-1, 2)

        x0_xy = np.asarray(
            [[x0.real, x0.imag]],
            dtype=float,
        )

        self.E_highlight.set_offsets(E_xy[0:1])
        self.E_scatter.set_offsets(E_xy)
        self.V_scatter.set_offsets(V_xy)
        self.x0_scatter.set_offsets(x0_xy)

        self.autoscale_axis(self.ax1, E_xy)
        
        self.fig.canvas.draw_idle()
    # ================================================================
    # Small counters used in Section 1
    # ================================================================
    def create_small_counter(
        self,
        x,
        y,
        initial_value, is_bounded
    ):
        value_width = 0.031
        counter_height = 0.070
        button_width = 0.016
        button_gap = 0.004

        value_axes = self.fig.add_axes([
            x,
            y,
            value_width,
            counter_height,
        ])

        value_axes.set_xticks([])
        value_axes.set_yticks([])

        value_text = value_axes.text(
            0.5,
            0.5,
            str(initial_value),
            ha="center",
            va="center",
            fontsize=12,
        )

        button_x = x + value_width + button_gap
        button_height = counter_height / 2

        up_axes = self.fig.add_axes([
            button_x,
            y + button_height,
            button_width,
            button_height,
        ])

        down_axes = self.fig.add_axes([
            button_x,
            y,
            button_width,
            button_height,
        ])

        up_button = Button(up_axes, "▲")
        down_button = Button(down_axes, "▼")

        self.maxval_section1=10
        counter = {
            "value": initial_value,
            "value_text": value_text,
            "up_button": up_button,
            "down_button": down_button,
        }

        up_button.on_clicked(
            lambda event, c=counter:
            self.change_counter(c, 1,self.maxval_section1,True,is_bounded)
        )

        down_button.on_clicked(
            lambda event, c=counter:
            self.change_counter(c, -1,self.maxval_section1,True,is_bounded)
        )

        return counter

    # ================================================================
    # Large counter used in Section 2
    # ================================================================
    def create_large_counter(
        self,
        position,
        title,
        initial_value,
    ):
        x, y, width, height = position

        panel_axes = self.fig.add_axes(position)
        panel_axes.set_xticks([])
        panel_axes.set_yticks([])

        panel_axes.text(
            0.5,
            0.78,
            title,
            ha="center",
            va="center",
            fontsize=13,
        )

        counter_width = width * 0.68
        counter_height = height * 0.34

        # Centres the complete counter inside the panel.
        counter_x = x + (width - counter_width) / 2
        counter_y = y + height * 0.10

        value_width = counter_width * 0.68
        button_width = counter_width * 0.25
        gap = counter_width * 0.07

        value_axes = self.fig.add_axes([
            counter_x,
            counter_y,
            value_width,
            counter_height,
        ])

        value_axes.set_xticks([])
        value_axes.set_yticks([])

        value_text = value_axes.text(
            0.5,
            0.5,
            str(initial_value),
            ha="center",
            va="center",
            fontsize=13,
        )

        button_x = counter_x + value_width + gap
        button_height = counter_height / 2

        up_axes = self.fig.add_axes([
            button_x,
            counter_y + button_height,
            button_width,
            button_height,
        ])

        down_axes = self.fig.add_axes([
            button_x,
            counter_y,
            button_width,
            button_height,
        ])

        up_button = Button(up_axes, "▲")
        down_button = Button(down_axes, "▼")

        self.maxval_section2 =10

        counter = {
            "value": initial_value,
            "value_text": value_text,
            "up_button": up_button,
            "down_button": down_button,
        }

        up_button.on_clicked(
            lambda event, c=counter:
            self.change_counter(c, 1,self.maxval_section2)
        )

        down_button.on_clicked(
            lambda event, c=counter:
            self.change_counter(c, -1,self.maxval_section2)
        )

        return counter

    # ================================================================
    # Counter modification
    # ================================================================
    def change_counter(self, counter, change,maxval,causes_sigma_update=False,is_bounded=True):
        counter["value"] += change
        # limit values
        if is_bounded:
            counter["value"] = min(maxval,max(
                0,
                counter["value"],
            ))

        counter["value_text"].set_text(
            str(counter["value"])
        )
        if causes_sigma_update:
            self.set_right_text(self.poly_pack.get_permut_representation(self.get_counter_values()[0]))
        E_xy = np.asarray(
                    [(z.real, z.imag) for z in self.poly_pack.E],
                    dtype=float,
                ).reshape(-1, 2)
        i = self.section2["value"]
        self.E_highlight.set_offsets(E_xy[i:i+1])

        self.fig.canvas.draw_idle()
    def get_counter_values(self):
        """Returns path instructions and starting point index"""
        instructions= []
        for i in range(len(self.section1_row1)):
            instructions.append((self.section1_row1[i]["value"],self.section1_row2[i]["value"]))
        
        return instructions, self.section2["value"]
    # ================================================================
    # Mutable text displays
    # ================================================================
    def set_left_text(self, text):
        self.left_display_text.set_text(str(text))
        self.fig.canvas.draw_idle()

    def set_right_text(self, text):
        self.right_display_text.set_text(str(text))
        self.fig.canvas.draw_idle()

    # ================================================================
    # Button callbacks
    # ================================================================
    def button1_clicked(self, event):
  
        self.iP+=1
        self.poly_pack=Poly_package(self.iP)
        self.config_poly()
        self.reset_anim()

    def button2_clicked(self, event):


        instructions,start=self.get_counter_values()

        if all(a[1]==0 for a in instructions ):return

        
        
        
        path_curve,t_values,lifted_curve =self.poly_pack.curves(instructions,start)
        N=len(path_curve)
        def update(frame):
            self.releve_line.set_data(lifted_curve[:frame].real,lifted_curve[:frame].imag)
            self.path_line.set_data(path_curve[:frame].real,path_curve[:frame].imag)
            a=max(0,frame-10)
            b = max(0,frame-20)
            self.path_highlight.set_data(path_curve[a:frame].real,path_curve[a:frame].imag)
            self.releve_highlight.set_data(lifted_curve[b:frame].real,lifted_curve[b:frame].imag)
            return (self.releve_line,)

        # Store it as self.animation, not as a local variable
        if self.animation is not None:
            self.animation.event_source.stop()
        self.animation = FuncAnimation(
            self.fig,
            update,
            frames=range(1, len(lifted_curve) + 1),
            interval=2,
            blit=False,
            repeat=False,
            cache_frame_data=False,
        )


        self.fig.canvas.draw_idle()
    def reset_anim(self):
        if self.animation is not None:
            self.animation.event_source.stop()
        self.path_highlight.set_data([],[])
        self.releve_highlight.set_data([],[])
    def show(self):
        plt.show()

    def config_poly(self):
        self.maxval_section1 =len(self.poly_pack.V)-1
        self.maxval_section2= len(self.poly_pack.E)-1

        self.path_line.set_data([],[])
        self.releve_line.set_data([],[])
        self.set_points(self.poly_pack.E,self.poly_pack.V,self.poly_pack.x0)
        self.scale_axis(self.ax2,np.abs(self.poly_pack.x0))

        self.set_left_text(self.poly_pack.representation)
        self.set_right_text(r"$\sigma=\mathrm{id}$")
        
        self.change_counter(self.section2,0,0)
        for i in range(len(self.section1_row1)):
            self.change_counter(self.section1_row1[i],0,0)
            self.change_counter(self.section1_row2[i],0,0)
            


        

if __name__ == "__main__":
    application = MatplotlibInterface()
    application.show()
